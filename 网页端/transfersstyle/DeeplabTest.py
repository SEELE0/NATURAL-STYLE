import argparse
import os

import cv2
import numpy as np
import time

from modeling.deeplab import *
from dataloaders import custom_transforms as tr
from PIL import Image
from torchvision import transforms
from dataloaders.utils import *
from torchvision.utils import make_grid, save_image


def deeplab(input):
    model_s_time = time.time()
    model = DeepLab(num_classes=21,
                    backbone='mobilenet',
                    output_stride=16,
                    sync_bn=False,
                    freeze_bn=False)

    ckpt = torch.load("checkpoint/model_best.pth.tar", map_location='cpu')
    model.load_state_dict(ckpt['state_dict'])
    model = model.cuda()
    model_u_time = time.time()
    model_load_time = model_u_time - model_s_time
    print("model load time is {}".format(model_load_time))

    composed_transforms = transforms.Compose([
        tr.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        tr.ToTensor()])
    ###
    s_time = time.time()
    image = Image.open(input).convert('RGB')
    target = Image.open(input).convert('L')
    sample = {'image': image, 'label': target}
    tensor_in = composed_transforms(sample)['image'].unsqueeze(0)
    model.eval()
    tensor_in = tensor_in.cuda()
    with torch.no_grad():
        output = model(tensor_in)
    grid_image = make_grid(decode_seg_map_sequence(torch.max(output[:3], 1)[1].detach().cpu().numpy()), 3,
                           normalize=False, range=(0, 255))
    save_image(grid_image, 'photo/photo_cut/cut_mask/' + "{}_mask.png".format(input.split('/')[-1][:-4]))
    u_time = time.time()
    img_time = u_time - s_time
    print("image:{} time: {} ".format(input.split('/')[-1][:-4], img_time))
    ####
    mask = cv2.imread('photo/photo_cut/cut_mask/' + "{}_mask.png".format(input.split('/')[-1][:-4]))
    main = cv2.imread(input)
    img_info = mask.shape
    image_height = img_info[0]
    image_weight = img_info[1]
    dst_back = np.full((image_height, image_weight, 3), 255, np.uint8)
    dst_main = np.full((image_height, image_weight, 3), 255, np.uint8)
    for i in range(image_height):
        for j in range(image_weight):
            (b, g, r) = mask[i][j]
            (a, c, d) = main[i][j]
            if ((b, g, r) == (0, 0, 0)):
                dst_back[i][j] = (a, c, d)
            else:
                dst_main[i][j] = (a, c, d)
    cv2.imwrite("photo/photo_cut/cut_back/" + "{}_back.png".format(input.split('/')[-1][:-4]), dst_back)
    cv2.imwrite("photo/photo_cut/cut_main/" + "{}_main.png".format(input.split('/')[-1][:-4]), dst_main)
    cv2.waitKey(0)


if __name__ == "__main__":
    deeplab("photo/photo_cut/cuts/2007_002088.jpg")
