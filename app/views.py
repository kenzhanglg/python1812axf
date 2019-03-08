from django.shortcuts import render
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, \
    Goods


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
def market(request):

    foodtypes = Foodtype.objects.all()
    #商品信息
    # goods_list = Foodtype.objects.all()[0:10]
    #默认打开热销榜
    #点击左侧分类，显示对应分类商品信息  传参数
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    index= int(request.COOKIES.get('index','0'))
    categoryid = foodtypes[index].typeid
    goods_list = Goods.objects.filter(categoryid=categoryid)
    response_str = {
        'foodtypes':foodtypes,
        'goods_list':goods_list,

    }
    return render(request,'market/market.html',context=response_str)

def cart(request):
    return render(request,'cart/cart.html')

def mine(request):
    return render(request,'mine/mine.html')
