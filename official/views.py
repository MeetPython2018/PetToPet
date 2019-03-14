from django.shortcuts import render, reverse, redirect
from verify.models import User
from petstate.models import Tweet, Comment, Heart
from django.http import JsonResponse


# Create your views here.

# 主页路径处理函数
def index(request):
    if request.method == 'GET':
        tel = request.session.get('tel', None)
        if tel:
            real_true = User.objects.filter(tel=tel).first()
            if real_true.cate and real_true.key:
                flag = 1
            else:
                flag = 0
            Ema = real_true.email
            deal_email = Ema.split('@')
            data = Tweet.objects.all().order_by('-id')
            for item in data:
                uname = User.objects.filter(id=item.a_id).first()
                item.uname = uname
                url = item.img.url
                true_url = url.split("%7C")
                item.img = true_url
                for i in range(1, len(true_url)):
                    true_url[i] = '/media/'+true_url[i]
                item.length = len(true_url)
            # 查询点赞情况
            tel = request.session.get('tel', None)
            user_id = User.objects.get(tel=tel)
            about_heart = Heart.objects.all()
            arr_heart = set()
            # arr_user = set()
            for i in about_heart:
                demo1 = i.msg_id
                # demo2 = i.users_id
                arr_heart.add(demo1)
                # arr_user.add(demo2)
            for item in data:
                uid = Heart.objects.filter(msg_id=item.id).all()
                arr_user = set()
                for son in uid:
                    arr_user.add(son.users_id)
                # print(arr_user)
                item.true_heart = arr_heart
                item.true_user = arr_user
                item.art_user_img = item.a_id
                art_user_img = User.objects.filter(id=item.a_id).first()
                item.art_user_img= art_user_img.img
                print(item.art_user_img)
            # 登录用户头像的获取
            dl_user = User.objects.filter(tel=tel).first()
            return render(request, 'official/index.html', {'flag': flag, 'username': real_true.username, 'email': deal_email[0], 'data': data, "user_id": user_id.id,'dl_user':dl_user})
        else:
            return redirect(reverse("verify:login"))


# 动态点赞处理函数
def forecas(request):
    if request.is_ajax():
        msg_id = request.POST.get("msg_id", None)
        tel = request.session.get('tel', None)
        user_id = User.objects.get(tel=tel)
        heart = Heart.objects.filter(msg_id=int(msg_id)).all()
        heart_num = int(len(heart)) + 1
        print(msg_id, type(msg_id), user_id)
        YorN = Heart.objects.filter(msg_id=int(msg_id), users_id=int(user_id.id))
        print(YorN)
        if not YorN:
            Tweet.objects.filter(id=int(msg_id)).update(heart_num=heart_num)
            obj = Heart(msg_id=int(msg_id), users_id=int(user_id.id))
            obj.save()
            return JsonResponse({"statue": 'ok'})
        else:
            return JsonResponse({"statue": 'error'})
    if request.method == 'GET':
        return render(request,'official/forecas.html')
    # if request.method == 'POST':
    #     dis = request.POST.get('dis')
    #     roomnum = request.POST.get('roomnum')
    #     halls = request.POST.get('halls')
    #     floor = request.POST.get('floor')
    #     area = request.POST.get('area')
    #     subway = request.POST.get('subway')
    #     school = request.POST.get('school')
    #     print(dis, roomnum, halls, floor, area, subway, school)
    #     print(type(subway), type(school))
    #     yuce = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     if dis == '1':
    #         yuce[0] = 1
    #     elif dis == '2':
    #         yuce[1] = 1
    #     elif dis == '3':
    #         yuce[2] = 1
    #     elif dis == '4':
    #         yuce[3] = 1
    #     elif dis == '5':
    #         yuce[4] = 1
    #     if floor == 'low':
    #         yuce[5] = 1
    #     elif dis == 'middle':
    #         yuce[6] = 1
    #     yuce[7] = int(roomnum)
    #     yuce[8] = int(halls)
    #     yuce[9] = int(area)
    #     yuce[10] = int(subway)
    #     yuce[11] = int(school)
    #     print(yuce)
    #     df1 = pd.read_csv('house_price.csv')
    #     df2 = pd.get_dummies(df1[['dist', 'floor']])  # 虚拟变量,将汉字项转变为数字
    #     del df2['dist_chaoyang']                      # 他们每一种中的分类之间的关系很大，需要删除一列
    #     del df2['floor_high']
    #     del df1['dist']
    #     del df1['floor']
    #     pd.set_option('display.max_columns', 20)       # 输出的最大列数，避免省略
    #     df = pd.concat([df2, df1], axis=1)
    #     X = df.iloc[:, :-1]
    #     y = df['price']
    #     print(X.head(1))
    #     reg = LinearRegression()
    #     reg = reg.fit(X, y)
    #     price = reg.predict(np.array(yuce).reshape(1, -1))
    #     print(price)
    #     price = int(price[0])
    #     return render(request, 'official/forecas.html', {'price': price})


# 评论处理逻辑
def lev_message(request, item_id):
    if request.is_ajax():
        tel = request.session.get('tel', None)
        user_id = User.objects.get(tel=tel)
        msg_id = item_id
        con = request.POST.get('con', None)
        pl = Comment.objects.filter(msg_id=item_id).all()
        pl_num = int(len(pl))+1
        Tweet.objects.filter(id=int(item_id)).update(pl_num=pl_num)
        obj = Comment(con=con, msg_id=int(msg_id), users_id=int(user_id.id))
        obj.save()
        return JsonResponse({"statue": 'ok'})
    if request.method == 'GET':
        data = Tweet.objects.filter(id=item_id).first()
        a_id = data.a_id
        uname = User.objects.filter(id=a_id).first()
        return render(request, 'official/lev_message.html', {"data": data, 'uname': uname.username})


# 查看评论处理逻辑
def see_msg(request, item_id):
    if request.method == 'GET':
        data = Tweet.objects.filter(id=item_id).first()
        a_id = data.a_id
        uname = User.objects.filter(id=a_id).first()
        url = data.img.url
        true_url = url.split("%7C")
        data.img = true_url
        for i in range(1, len(true_url)):
            true_url[i] = '/media/' + true_url[i]
        data.length = len(true_url)
        command = Comment.objects.filter(msg_id=item_id).all()
        for item in command:
            print(item.users_id)
            demo = User.objects.filter(id=item.users_id).first()
            PL_user_name = demo.username
            item.users_id = PL_user_name
        return render(request, 'official/see_msg.html', {"data": data, 'uname': uname.username,'command':command})


# 个人信息设置处理函数
def set_info(request, items):
    if request.method == 'GET':
        tel = request.session.get('tel', None)
        real_true = User.objects.filter(tel=tel).first()
        Ema = real_true.email
        deal_email = Ema.split('@')
        data = Tweet.objects.filter(a_id=real_true.id).order_by('-id')
        for item in data:
            uname = User.objects.filter(id=item.a_id).first()
            item.uname = uname
            url = item.img.url
            true_url = url.split("%7C")
            item.img = true_url
            for i in range(1, len(true_url)):
                true_url[i] = '/media/' + true_url[i]
            item.length = len(true_url)
        # 查询点赞情况
        user_id = User.objects.get(tel=tel)
        about_heart = Heart.objects.filter(users_id=user_id)
        arr_heart = set()
        for i in about_heart:
            demo1 = i.msg_id
            # demo2 = i.users_id
            arr_heart.add(demo1)
            # arr_user.add(demo2)
        for item in data:
            uid = Heart.objects.filter(msg_id=item.id).all()
            arr_user = set()
            for son in uid:
                arr_user.add(son.users_id)
            print(arr_user)
            item.true_heart = arr_heart
            item.true_user = arr_user
        # 用户头像获取
        dl_user = User.objects.filter(tel=tel).first()
        return render(request, 'official/set_info.html', {'username': real_true.username, 'data': data, 'email': deal_email[0], "user_id": user_id.id, "items": items,"dl_user":dl_user})



import os,base64


# 个人信息设置
def about_me(request):
    if request.method == 'GET':
        tel = request.session.get('tel', None)
        real_true = User.objects.filter(tel=tel).first()
        dl_user = User.objects.filter(tel=tel).first()
        return render(request, 'official/about_me.html', {'username': real_true.username,"dl_user":dl_user})
    if request.method == 'POST':
        img_data = request.POST.get('img_data', None)
        nan = img_data.split(",")
        img_name = request.session.get('tel', None)

        file = open(os.path.join('upload/user_img/images/' + img_name+'.png'), 'wb')
        print(file)
        file.write(base64.b64decode(nan[1]))
        file.close()
        a_id = User.objects.filter(tel=img_name).first()

        User.objects.filter(id=int(a_id.id)).update(img='/user_img/images/' + img_name+'.png')
        return JsonResponse({"statue": 'ok'})