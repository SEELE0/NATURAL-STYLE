import time
from PIL import Image
import matplotlib.pyplot as plt
import torch as ch
import torch.nn.functional as functional
import torch.optim as optim
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from robustness import datasets, model_utils
from robustness.tools import helpers
import os


os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
device = ch.device("cuda" if ch.cuda.is_available() else "cpu")
imsize = 256 if ch.cuda.is_available() else 128


def image_loader(image_name):
    loader = transforms.Compose([
        transforms.Resize(imsize),
        transforms.ToTensor()])

    image = Image.open(image_name)
    image = loader(image).unsqueeze(0)[:, :3, :, :]
    return image.to(device, ch.float)


def imshow(tensor, title=None):
    unloader = transforms.ToPILImage()
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)


dataset = datasets.RestrictedImageNet('')


class resnet(nn.Module):
    def __init__(self):
        super(resnet, self).__init__()
        dataset = datasets.RestrictedImageNet('')
        model_kwargs = {
            "arch": 'resnet50',
            'dataset': dataset,
            'resume_path': './RestrictedImageNet.pt',
            'parallel': False
        }
        model, ckpt = model_utils.make_and_restore_model(**model_kwargs)
        self.model = model.model
        # for param in self.parameters():
        #     param.requires_grad = False


robust_resnet = resnet().model
vgg = models.vgg19(pretrained=True).features


class ContentLoss(nn.Module):

    def __init__(self, feature_maps, ):
        super(ContentLoss, self).__init__()
        self.feature_maps = {key: val.detach() for key, val in feature_maps.items()}

    def forward(self, input, layer_name):
        return functional.mse_loss(input[layer_name], self.feature_maps[layer_name])


def gram_matrix(input):
    a, b, c, d = input.size()  # a=batch size(=1)
    # b=number of feature maps
    # (c,d)=dimensions of a f. map (N=c*d)

    features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL

    G = ch.mm(features, features.t())  # compute the gram product

    # we 'normalize' the values of the gram matrix
    # by dividing by the number of element in each feature maps.
    return G.div(a * b * c * d)


class StyleLoss(nn.Module):

    def __init__(self, feature_maps):
        super(StyleLoss, self).__init__()
        self.feature_maps = {key: gram_matrix(val).detach() for key, val in feature_maps.items()}

    def forward(self, input, layer_name):
        G = gram_matrix(input[layer_name])
        return functional.mse_loss(G, self.feature_maps[layer_name])


class ResNetStyleTransferModel(nn.Module):
    """This class is used to wrap a ResNet model for style transfer"""

    def __init__(self, model, mean, std):
        super(ResNetStyleTransferModel, self).__init__()
        self.normalize = helpers.InputNormalize(mean, std)
        self.model = model  # Resnet50 model

    def forward(self, x):
        layers = {}

        x = self.normalize(x)

        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        layers['conv_1'] = x
        x = self.model.layer2(x)
        layers['conv_2'] = x
        x = self.model.layer3(x)
        layers['conv_3'] = x
        x = self.model.layer4(x, fake_relu=True)
        layers['conv_4'] = x

        return layers


class VGGStyleTransferModel(nn.Module):
    """This class is used to wrap a VGG model for style transfer"""

    def __init__(self, model, mean, std):
        super(VGGStyleTransferModel, self).__init__()
        self.normalize = helpers.InputNormalize(mean, std)
        self.model = model  # VGG model

    def forward(self, x):
        layers = {}

        x = self.normalize(x)

        i = 0
        for layer in self.model.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                # The in-place version doesn't play very nicely with the ContentLoss
                # and StyleLoss we insert below. So we replace with out-of-place
                # ones here.
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
                layer = nn.AvgPool2d(kernel_size=2, stride=2)
            elif isinstance(layer, nn.BatchNorm2d):
                name = 'bn_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))
            x = layer(x)

            if isinstance(layer, nn.Conv2d):
                layers[name] = x
            if i == 13:  # This is the last layer we usually use for style transfer
                break
        return layers


def get_input_optimizer(input_img, opt='Adam'):
    # this line to show that input is a parameter that requires a gradient
    if opt == 'Adam':
        optimizer = optim.Adam([input_img.requires_grad_()], lr=0.01)
    elif opt == 'LBFGS':
        optimizer = optim.LBFGS([input_img.requires_grad_()])
    else:
        raise RuntimeError('Unrecognized optimizer: {}'.format(opt))
    return optimizer


def style_transfer(st_model, content_img, style_img, start_from_content=True,
                   n_iters=[0, 2000], style_weight=1e9, content_weight=1,
                   content_layers=['conv_3'], style_layers=['conv_1', 'conv_2', 'conv_3', 'conv_4'],
                   opt='Adam',
                   verbose=True,
                   ):
    st_model.eval().cuda()

    if isinstance(content_img, str):
        content_img = image_loader(content_img)

    if isinstance(style_img, str):
        style_img = image_loader(style_img)

    content_feature_maps = st_model(content_img)
    content_feature_maps = {key: val.detach() for key, val in content_feature_maps.items()}

    style_feature_maps = st_model(style_img)
    style_feature_maps = {key: val.detach() for key, val in style_feature_maps.items()}

    content_loss_func = ContentLoss(content_feature_maps)
    style_loss_func = StyleLoss(style_feature_maps)

    if start_from_content:
        input_img = content_img.clone()
    else:
        input_img = ch.randn(content_img.data.size(), device=device)

    optimizer = get_input_optimizer(input_img, opt=opt)

    run = [0]
    start_time = time.time()
    while run[0] <= n_iters[-1]:
        def closure():
            # correct the values of updated input image
            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            input_feature_maps = st_model(input_img)

            style_score = 0
            content_score = 0

            for sl in style_layers:
                _l = style_loss_func(input_feature_maps, sl) * style_weight
                style_score += _l
                # print(_l)
            for cl in content_layers:
                content_score += content_loss_func(input_feature_maps, cl) * content_weight
                # print(content_score)

            # style_score *= style_weight
            # content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            if run[0] in n_iters:
                print("run {}:".format(run))
                print('Style Loss : {:4f} Content Loss: {:4f} time elapsed: {} seconds'.format(
                    style_score.item(), content_score.item(), time.time() - start_time))
                if verbose:
                    plt.figure(figsize=(8, 8))
                    # imshow(input_img, title='run {}:'.format(run))


            run[0] += 1

            return style_score + content_score

        optimizer.step(closure)

    # a last correction...
    input_img.data.clamp_(0, 1)

    return input_img



def style(net,input,output):
    unloader = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(332)
    ])
    if net=='resnet':
        out = style_transfer(
            ResNetStyleTransferModel(robust_resnet, dataset.mean, dataset.std),
            input, output, style_weight=1e9, content_weight=1,
            start_from_content=True, n_iters=[200], opt='LBFGS')
    else:
        out = style_transfer(
            VGGStyleTransferModel(vgg, dataset.mean, dataset.std),
            input, output, style_weight=4e6, content_weight=1,
            start_from_content=True, n_iters=[200], content_layers=['conv_10'],
            style_layers=['conv_1', 'conv_3', 'conv_5', 'conv_9', 'conv_13'], opt='LBFGS')
    x = out.cpu().clone()
    img_tensor = x.squeeze(0)
    img = unloader(img_tensor)
    img.save('photo/photo_transfer/'+input.split('/')[-1][:-4]+'.png')
if __name__ == '__main__':
    style('vgg','photo/photos/2007_002088.jpg','photo/photo_type/_s.jpg')

