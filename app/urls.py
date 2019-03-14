from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^market/$', views.market, name='marketbase'),
    url(r'^market/(?P<childid>\d+)/(?P<sortid>\d+)/$', views.market,
        name='market'),
    # url(r'^market/$', views.market, name='market'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^checkemail/$', views.checkemail, name='checkemail'),  # 账号验证
    url(r'^addcart/$', views.addcart, name='addcart'),  # 添加到购物车中
    url(r'^subcart/$', views.subcart, name='subcart'),  # 删除购物车中

    url(r'^changecartselect/$', views.changecartselect,
        name='changecartselect'),  # 购物车商品选中状态
    url(r'^changecartall/$', views.changecartall, name='changecartall'),  # 全选/取消全选

    url(r'^generateorder/$', views.generateorder, name='generateorder'),    # 生成订单
    url(r'orderlist/$', views.orderlist, name='orderlist'), # 订单列表
    url(r'^orderdetail/(?P<identifier>[\d.]+)/$', views.orderdetail, name='orderdetail'),  # 订单详情

    url(r'^returnurl/$', views.returnurl, name='returnurl'),#
    url(r'^appnotifyurl/$', views.appnotifyurl, name='appnotifyurl'),#
    url(r'^pay/$', views.pay, name='pay'),#

]