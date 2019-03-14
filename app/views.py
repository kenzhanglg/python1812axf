import hashlib
import random
import time
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, \
    Goods, User, Cart, Order, OrderGoods


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

    #获取购物车信息
    token = request.session.get('token')
    userid = cache.get(token)

    if userid:
        user = User.objects.get(pk=userid)
        carts = user.cart_set.all()
        response_str['carts'] = carts

    return render(request,'market/market.html',context=response_str)

def cart(request):
    # carts = Cart.objects.all()
    token = request.session.get('token')
    userid = cache.get(token)
    if userid: #有登录才显示
        user = User.objects.get(pk=userid)
        carts = user.cart_set.filter(number__gt=0)

        return render(request,'cart/cart.html',context={"carts":carts})
    #没有登录就登录
    else:
        return render(request,'cart/no-login.html')

def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    response_data = {
        'user' : None,

    }
    if userid:
        user = User.objects.get(pk = userid)
        response_data['user'] = user
        orders = user.order_set.all()
        # 待付款
        response_data['waitpay'] = orders.filter(status=0).count()
        # 待发货
        response_data['paydone'] = orders.filter(status=1).count()

    return render(request,'mine/mine.html',context={
        'response_data':response_data})

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
        users = User.objects.filter(email=email)
        back = request.COOKIES.get('back')
        # print(back)

        if users.exists():
            user = users.first()
            if user.password == genrate_password(password):
                token = genrate_token()
                #状态保持
                cache.set(token, user.id, 60 * 60 * 24 * 3)
                #传递给客户端
                request.session['token'] = token
                # 根据back
                if back == 'mine':
                    return redirect('axf:mine')
                else:
                    return redirect('axf:marketbase')

            else:
                return render(request, 'mine/login.html', context={
                    'user_prr': '密码错误'})
        else:
            return render(request, 'mine/login.html',context={
                'user_err':'用户不存在'})

def logout(request):
    request.session.flush()
    return redirect('axf:mine')

def checkemail(request):
    email = request.GET.get('email')
    #去数据库中查找
    users = User.objects.filter(email=email)
    if users.exists():  #帐号被占用
        response_data = {
            'status':0,  #1可用  0不可用
            'msg':'帐号被占用'
        }
    else:  #帐号可用
        response_data = {
            'status': 1,  # 1可用  0不可用
            'msg': '帐号可用'
        }
    #返回JSON 数据
    return JsonResponse(response_data)

def addcart(request):
    #获取token
    token = request.session.get('token')
    #响应数据
    response_data = {}
    # 缓存
    if token:
        userid = cache.get(token)
        if userid:
            user = User.objects.get(pk=userid)
            goodsid = request.GET.get('goodsid')
            goods = Goods.objects.get(pk = goodsid)
            carts = Cart.objects.filter(user=user).filter(goods=goods)
            if carts.exists():
                cart = carts.first()
                cart.number = cart.number + 1
                cart.save()
            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()
            response_data['status'] = 1
            response_data['number'] = cart.number
            response_data['msg'] = '添加{} 购物车成功,数量为：{}'.format(
                cart.goods.productlongname,cart.number)
            return JsonResponse(response_data)
    response_data['status'] = -1
    response_data['msg'] = '请登录后操作'
    return JsonResponse(response_data)


def subcart(request):
    #商品
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk = goodsid)

    #用户
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    response_data = {
        'status':1,
        'msg':'删除商品成功',
        'number':cart.number,
    }

    return JsonResponse(response_data)


def changecartselect(request):
    cartid = request.GET.get('cartid')
    # print(cartid)
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    response_data = {
        'msg':'修改状态成功',
        'status':1,
        'isselect':cart.isselect,
    }

    return JsonResponse(response_data)


def changecartall(request):
    isall = request.GET.get('isall')

    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)
    carts = user.cart_set.all()
    
    if isall == 'false':
        isall = False
    else:
        isall = True

    for cart in carts:
        cart.isselect = isall
        cart.save()

    response_data = {
        'msg':'全选/取消全选 成功',
        'status':1,

    }
    return JsonResponse(response_data)


def genrate_identifier():
    temp = str(time.time()) + str(random.randrange(1000,10000))
    return temp


def generateorder(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    order = Order()
    order.user = user
    order.identifier = genrate_identifier()
    order.save()

    carts = user.cart_set.filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.number = cart.number
        orderGoods.goods = cart.goods
        orderGoods.save()

        #从购物车删除
        cart.delete()
    return render(request,'order/orderdetail.html',context={
        'order':order})


def orderlist(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)
    orders = user.order_set.all()

    return render(request,'order/orderlist.html',context={
        'orders':orders})


def orderdetail(request,identifier):
    order = Order.objects.filter(identifier=identifier).first()
    return render(request,'order/orderdetail.html',context={
        'order':order})