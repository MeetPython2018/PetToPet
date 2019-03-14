from django.shortcuts import render, HttpResponse, reverse, redirect,render_to_response
import os
from django.conf import settings
from .models import Tweet
from verify.models import User
from official.models import Category, Keyword
import time
import random
from PIL import Image
from util.myutil import authuser

# Create your views here.


def write_TW(request):
    if request.method == 'GET':
        return render(request, 'petstate/write_TW.html')
    if request.method == 'POST':
        obj = dict()
        txt = request.POST.get('textarea')
        files = request.FILES.getlist('image', None)
        # for item in files:
        #     print(item, type(item))
        # tel = request.session.get('tel', None)
        # if not files:
        #     obj['error'] = '没有上传的文件'
        # else:
        #     for f in files:
        #         fname = f.name
        #         demo_name = fname.split('.')
        #         fn = time.strftime('%Y%m%d%H%M%S')
        #         fn = fn + '_%d' % random.randint(0, 100)  # 定义文件名，年月日时分秒随机数
        #         demo_name[0] = fn
        #         fname = demo_name[0] + '.' + demo_name[1]
        #         f.name = fname
        #         destination = open(os.path.join('upload/tweet/images/' + fname), 'wb')
        #         for chunk in f.chunks():
        #             destination.write(chunk)
        #         destination.close()
        #         print(f.name)
        #     a_id = User.objects.filter(tel=tel).first()
        #     oo = Tweet(con=txt, c_id=1, k_id=1, a_id=int(a_id.id), img=request.FILES.get('image', None))
        #     oo.save()
        tel = request.session.get('tel', None)
        if not files:
            obj['error'] = '没有上传的文件'
        else:
            real_url = []
            for f in files:
                fname = f.name
                demo_name = fname.split('.')
                fn = time.strftime('%Y%m%d%H%M%S')
                fn = fn + '_%d' % random.randint(0, 100)  # 定义文件名，年月日时分秒随机数
                demo_name[0] = fn
                fname = demo_name[0] + '.' + demo_name[1]
                real_url.append(fname)
                destination = open(os.path.join('upload/tweet/images/' + fname), 'wb')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
                img = Image.open('upload/tweet/images/' + fname)
                print(img.size)
                # cropped = img.crop((0, 0, 512, 128))  # (left, upper, right, lower)
                # cropped.save("./data/cut/pil_cut_thor.jpg")
            dirs = settings.MEDIA_ROOT + '/tweet/images/'
            folder = os.path.exists(dirs)
            if not folder:             # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(dirs)      # 创建文件时如果路径不存在会创建这个路径
            try:
                img_name = []
                for url in real_url:
                    img_name.append(url)
                img_url = ''
                for i in img_name:
                    url = '/tweet/images/'+i+'|'
                    img_url += url
                img_url = img_url[0:-1]
                a_id = User.objects.filter(tel=tel).first()
                oo = Tweet(con=txt, c_id=1, k_id=1, a_id=int(a_id.id), img=img_url)
                oo.save()
            except Exception as e:
                obj['error'] = e
        return redirect(reverse("official:index"))


@authuser
def intensify(request):
    if request.method == 'GET':
        cate = Category.objects.all()
        return render(request, 'petstate/intensify.html', {'cate': cate})
    if request.method == 'POST':
        cate = request.POST.get('cate', None)
        tel = request.session.get('tel', None)
        request.session['cate'] = cate
        User.objects.filter(tel=tel).update(cate=str(cate))
        return redirect(reverse("petstate:intensify_son"))

@authuser
def intensify_son(request):
    if request.method == 'GET':
        cate = request.session.get('cate', None)
        key = Keyword.objects.filter(c_id=cate).all()
        return render(request, 'petstate/intensify_son.html', {'cate': cate, 'key': key})
    if request.method == 'POST':
        key = request.POST.get('key', None)
        tel = request.session.get('tel', None)
        User.objects.filter(tel=tel).update(key=str(key))
        return redirect(reverse('petstate:write_TW'))
