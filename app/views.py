import hashlib
import random
import time

from django.core.cache import cache
from django.shortcuts import render, redirect
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, \
    Goods, User


def home(request):
    #轮播图数据
    wheels = Wheel.objects.all()
    #导航
    navs = Nav.objects.all()
    #每日必购
    mustbuys = Mustbuy.objects.all()
    #商品部分
    shops = Shop.objects.all()
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass_list = shops[3:7]
    shopcommends = shops[7:11]
    #主体内容
    mainshows = Mainshow.objects.all()


    response_dir = {
        'wheels':wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead':shophead,
        'shoptabs': shoptabs,
        'shopclass_list': shopclass_list,
        'shopcommends': shopcommends,
        'mainshows':mainshows,
    }

    return render(request,'home/home.html',context=response_dir)

# def market(request,categoryid=104749,):
def market(request,childid='0',sortid='0'):

    foodtypes = Foodtype.objects.all()
    #商品信息
    # goods_list = Foodtype.objects.all()[0:10]
    #默认打开热销榜
    #点击左侧分类，显示对应分类商品信息  传参数
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    index= int(request.COOKIES.get('index','0'))
    categoryid = foodtypes[index].typeid
    # goods_list = Goods.objects.filter(categoryid=categoryid)
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(childcid=childid)

    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')


    childtypenames = foodtypes[index].childtypenames
    childtype_list = []
    for item in childtypenames.split('#'):
        item_arr = item.split(':')
        temp_arr = {
            'name':item_arr[0],
            'id':item_arr[1],
        }
        childtype_list.append(temp_arr)




    response_str = {
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'childtype_list':childtype_list,
        'childid':childid,
    }
    return render(request,'market/market.html',context=response_str)

def cart(request):
    return render(request,'cart/cart.html')

def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:
        user = User.objects.get(pk = userid)
    return render(request,'mine/mine.html',context={'user':user})

def genrate_token():
    temp = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf-8'))
    return md5.hexdigest()

def genrate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()

def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')

    elif request.method == 'POST':
        user = User()
        user.email = request.POST.get('email')
        user.password = genrate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.save()

        token = genrate_token()

        cache.set(token,user.id,60*60*24*3)

        request.session['token'] = token

        return redirect('axf:mine')

def login(request):
    if request.method == 'GET':
        return render(request,'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = User.objects.filter(email=email).filter(password=password)
        if users.exists():
            user = users.first()
            token = genrate_token()
            cache.set(token, user.id, 60 * 60 * 24 * 3)
            request.session['token'] = token
            return redirect('axf:mine')
        else:
            return render(request, 'mine/login.html')

def logout(request):
    request.session.flush()
    return redirect('axf:mine')
