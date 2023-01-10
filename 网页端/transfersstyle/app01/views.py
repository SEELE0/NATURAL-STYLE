import os
import shutil
import numpy as np
import cv2
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
import style_transfer_by_torch
from resnet4 import style
from train_vgg_resnet import stylize, stylizes, stylized
from DeeplabTest import deeplab


def index(request):
    return render(request, 'index.html')


class landing(View):

    def get(self, request):
        return render(request, 'landing.html')

    def post(self, request):
        pass


class landing5(View):
    def get(self, request):
        return render(request, 'landing5.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)
        self.file_type = request.FILES.get('f2')
        with open('photo/photo_type/' + self.file_type.name, 'wb') as f:
            for i in self.file_type:
                f.write(i)
        self.file_list = request.POST.get('slct')  #############
        print(self.file_list)

        style(self.file_list,'photo/photos/' + self.file.name,'photo/photo_type/' + self.file_type.name)
        return render(request,'transfer.html',{'img_2': '/static/photo_transfer/'+self.file.name.split('/')[-1][:-4]+'.png','img_1': '/static/photos/' + self.file.name})
        # style_transfer_by_torch.main('photo/photos/' + self.file.name, 'photo/photo_type/' + self.file_type.name)
        # x = self.file.name.split('/')[-1][:-4]
        # y = self.file_type.name.split('/')[-1][:-4]
        # print('photo/photo_transfer/' + x + '_and_' + y + '.png')
        # return render(request, 'transfer.html', {'img_2': '/static/photo_transfer/' + x + '_and_' + y + '.png',
        #                                          'img_1': '/static/photos/' + self.file.name})


class landing4(View):
    def get(self, request):
        return render(request, 'landing4.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photo_cut/cuts/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)
        self.choice = request.POST.get('radio')
        deeplab('photo/photo_cut/cuts/' + self.file.name)
        if self.choice == "1":
            return render(request, 'transfer.html', {'img_1': '/static/photo_cut/cuts/' + self.file.name, 'img_2':'/static/photo_cut/cut_main/' + "{}_main.png".format(self.file.name[0:-4])})
        else:
            return render(request, 'transfer.html', {'img_1': '/static/photo_cut/cuts/' + self.file.name, 'img_2':'/static/photo_cut/cut_back/' + "{}_back.png".format(self.file.name[0:-4])})

        # return render(request, 'cut.html',
        #               {"img1": '/static/photo_cut/cut_main/' + "{}_main.png".format(self.file.name[0:-4]),
        #                "img2": '/static/photo_cut/cut_back/' + "{}_back.png".format(self.file.name[0:-4])})


class landing3(View):
    def get(self, request):
        return render(request, 'landing3.html')

    def post(self, request):
        pass


class Candy(View):
    def get(self, request):  ##########################################
        return render(request, 'Candy.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)
        # print(request.POST.get('radio'))
        print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Candy_Resnet.pth", 'photo/photos/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Candy_Vgg.pth", 'photo/photos/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Cubist(View):
    def get(self, request):
        return render(request, 'Cubist.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Cubist_Resnet.pth", 'photo/photos/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Cubist_Vgg.pth", 'photo/photos/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Mosaic(View):
    def get(self, request):
        return render(request, 'Mosaic.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Mosaic_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Mosaic_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Muse(View):
    def get(self, request):
        return render(request, 'Muse.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Muse_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Muse_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Rain(View):
    def get(self, request):
        return render(request, 'Rain.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Rain_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Rain_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Screem(View):
    def get(self, request):
        return render(request, 'Screem.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Screem_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Screem_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Shipwreck(View):
    def get(self, request):
        return render(request, 'Shipwreck.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Shipwreck_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Shipwreck_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Strarry(View):
    def get(self, request):
        return render(request, 'Strarry.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Strarry_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Strarry_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class Udnie(View):
    def get(self, request):
        return render(request, 'Udnie.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        with open('photo/photos/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)

        # print(self.file.name)
        if request.POST.get('radio') == 'ResNet':
            stylize("checkpoint/Udnie_Resnet.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})
        if request.POST.get('radio') == 'VGG':
            stylize("checkpoint/Udnie_Vgg.pth", 'photo/photo_main/' + self.file.name)
            return render(request, 'transfer.html',
                          {'img_2': "/static/photo_transfer/{}_transfer.png".format(self.file.name.split('/')[-1][:-4]),
                           'img_1': '/static/photos/' + self.file.name})


class monet(View):
    def get(self, request):
        return render(request, 'monet.html')

    def post(self, request):
        pass


class ukiyoe(View):
    def get(self, request):
        return render(request, 'ukiyoe.html')

    def post(self, request):
        pass



class vangogh(View):
    def get(self, request):
        return render(request, 'vangogh.html')

    def post(self, request):
        pass


class MOVIE(View):
    def get(self, request):
        return render(request, 'MOVIE.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        print(self.file.name)
        with open('video/video_main/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)
        self.file_list = request.POST.get('radio')#net
        # print(self.file_list)
        self.file_list_2 = request.POST.get('slct')#type

        # print(self.file_list_2)

        def save_img(path, video_name):
            video_path = path
            file_name = video_name.split('.')[0]
            folder_name = "video/video_temp/" + file_name
            os.makedirs(folder_name, exist_ok=True)
            vc = cv2.VideoCapture(video_path + video_name)
            fps = vc.get(cv2.CAP_PROP_FPS)  ##视频帧数
            print('fps:', fps)
            c = 0
            rval = vc.isOpened()
            while rval:
                c = c + 1
                rval, frame = vc.read()
                pic_path = folder_name + '/'
                if rval:
                    cv2.imwrite(pic_path + str(c) + '.png', frame)
                    cv2.waitKey(1)
                else:
                    break
            vc.release()
            print('save_success')
            print(folder_name)
            return fps

        def merge(inpath, outpath, fps):
            # path = 'images/outputs'
            path = inpath
            imgs = os.listdir(path)
            imgs.sort(key=lambda imgs: int(imgs[0:-4]))
            img = cv2.imread(path + '/' + imgs[0])
            h = img.shape[0]
            w = img.shape[1]
            # videoWriter = cv2.VideoWriter('images/outvoid/test2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))
            videoWriter = cv2.VideoWriter(outpath, cv2.VideoWriter_fourcc(*'H264'), fps, (w, h))
            for imgFile in imgs:
                img = cv2.imread(path + '/' + imgFile)
                videoWriter.write(img)

            videoWriter.release()

        fps = save_img('video/video_main/', self.file.name) // 1
        # "checkpoint/{0}_{1}.pth".format(self.file_list, "vgg"),
        stylizes("checkpoint/{0}_{1}.pth".format(self.file_list_2,self.file_list),
                 "video/video_temp/" + self.file.name.split('.')[0])
        # stylizes("checkpoint/b_resnet.pth","video/video_temp/" + self.file.name.split('.')[0])
        merge('video/video_transfer', 'video/video_result/' + self.file.name, fps)
        if os.path.exists("video/video_temp/" + self.file.name.split('.')[0]):
            shutil.rmtree("video/video_temp/" + self.file.name.split('.')[0])
        if os.path.exists("video/video_transfer"):
            shutil.rmtree("video/video_transfer")
        return render(request, "transfermovie.html", {'video': '/static/video_result/' + self.file.name})


class landing6(View):
    def get(self, request):
        return render(request, 'landing6.html')

    def post(self, request):
        self.file = request.FILES.get('f1')
        print(self.file.name)
        with open('photo/photo_cut/cuts/' + self.file.name, 'wb') as f:
            for i in self.file:
                f.write(i)
        self.file_list = request.POST.get('radio')#net
        self.file_list_2 = request.POST.get('slct')#type
        print(self.file_list,self.file_list_2)

        deeplab('photo/photo_cut/cuts/' + self.file.name)
        stylized("checkpoint/{1}_{0}.pth".format(self.file_list,self.file_list_2),
                 "photo/photo_cut/cut_back/{}_back.png".format(self.file.name[0:-4]),
                 'photo/photo_cut/cut_back_transfer/' + "{}_back_transfer.jpg".format(self.file.name[0:-4]))
        masked = cv2.imread('photo/photo_cut/cut_main/' + "{}_main.png".format(self.file.name[0:-4]))
        mained = cv2.imread('photo/photo_cut/cut_back_transfer/' + "{}_back_transfer.jpg".format(self.file.name[0:-4]))
        real_mask = cv2.imread('photo/photo_cut/cut_mask/' + "{}_mask.png".format(self.file.name[0:-4]))
        img_info = masked.shape
        image_height = img_info[0]
        image_weight = img_info[1]
        dst_back = np.full((image_height, image_weight, 3), 255, np.uint8)
        for i in range(image_height):
            for j in range(image_weight):
                (ra, rb, rc) = real_mask[i][j]
                (b, g, r) = masked[i][j]
                (a, c, d) = mained[i][j]
                if (ra, rb, rc) == (0, 0, 0):
                    dst_back[i][j] = (a, c, d)
                else:
                    dst_back[i][j] = (b, g, r)
        cv2.imwrite('photo/photo_cut/cut_transfer/' + "{}_transfer.png".format(self.file.name[0:-4]), dst_back)
        cv2.waitKey(0)
        return render(request, 'transfer.html',
                      {'img_2': '/static/photo_cut/cut_transfer/' + "{}_transfer.png".format(self.file.name[0:-4]),
                       'img_1': '/static/photos/' + self.file.name})