import os
import re
import torch
from torchvision import transforms
import utils
from model import TransformerNet


def stylize(model, content_image):
    device = torch.device("cuda")
    # content_image = "photo/photos/2007_002105.jpg"
    # model = "checkpoint/b_resnet.pth"
    output_image = "photo/photo_transfer/{}_transfer.png".format(content_image.split('/')[-1][:-4])
    content_image = utils.load_image(content_image, scale=None)
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = TransformerNet().eval()
        state_dict = torch.load(model)
        # for k in list(state_dict.keys()):
        #     if re.search(r'in\d+\.running_(mean|var)$', k):
        #         del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        output = style_model(content_image).cpu()
        utils.save_image(output_image, output[0])


def stylized(model, content_image, output_image):
    device = torch.device("cuda")
    # content_image = "photo/photos/2007_002105.jpg"
    # model = "checkpoint/b_resnet.pth"
    # output_image = "photo/photo_transfer/{}_transfer.png".format(content_image.split('/')[-1][:-4])
    content_image = utils.load_image(content_image, scale=None)
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = TransformerNet().eval()
        state_dict = torch.load(model)
        # for k in list(state_dict.keys()):
        #     if re.search(r'in\d+\.running_(mean|var)$', k):
        #         del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        output = style_model(content_image).cpu()
        utils.save_image(output_image, output[0])


def stylizes(model, image_path):
    os.makedirs("video/video_transfer", exist_ok=True)
    device = torch.device("cuda")

    # output_image = "photo/photo_transfer/{}_transfer.png".format(content_image.split('/')[-1][:-4])
    for name in os.listdir(image_path):
        content_image = utils.load_image(image_path + '/' + name, scale=None)
        content_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.mul(255))
        ])
        content_image = content_transform(content_image)
        content_image = content_image.unsqueeze(0).to(device)

        with torch.no_grad():
            style_model = TransformerNet().eval()
            state_dict = torch.load(model)
            # for k in list(state_dict.keys()):
            #     if re.search(r'in\d+\.running_(mean|var)$', k):
            #         del state_dict[k]
            style_model.load_state_dict(state_dict)
            style_model.to(device)
            output = style_model(content_image).cpu()
            utils.save_image("video/video_transfer/" + name, output[0])


if __name__ == '__main__':
    stylize("checkpoint/b_resnet.pth", "photo/photo_cut/cuts/2007_002105.jpg")
