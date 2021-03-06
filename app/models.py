from django.db import models

#基础类
class BaseModel(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)

    class Meta:
        #抽象类
        abstract = True

#轮播图  模型类
class Wheel(BaseModel):
    class Meta:
        db_table = 'axf_wheel'

#导航
class Nav(BaseModel):
    class Meta:
        db_table = 'axf_nav'

#每日必购
class Mustbuy(BaseModel):
    class Meta:
        db_table = 'axf_mustbuy'

#部分商品
class Shop(BaseModel):
    class Meta:
        db_table = 'axf_shop'


#商品类表  模型类
class Mainshow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'axf_mainshow'

#分类
class Foodtype(models.Model):
    #分类id
    typeid = models.CharField(max_length=20)
    #分类名称
    typename = models.CharField(max_length=200)
    #子类（多个）
    childtypenames = models.CharField(max_length=255)
    #排序
    typesort = models.IntegerField()
    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    # 商品ID
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=200)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 商品长名字
    productlongname = models.CharField(max_length=200)
    # 是否精选
    isxf = models.IntegerField()
    # 是否买一送一
    pmdesc = models.IntegerField()
    # 商品规格
    specifics = models.CharField(max_length=100)
    # 商品价格
    price = models.DecimalField(max_digits=6,decimal_places=2)
    # 商品超市价格
    marketprice = models.DecimalField(max_digits=6,decimal_places=2)
    # 分类ID
    categoryid = models.IntegerField()
    # 子类ID
    childcid = models.IntegerField()
    # 子类名字
    childcidname = models.CharField(max_length=100)
    # 详情id
    dealerid = models.CharField(max_length=10)
    # 库存量
    storenums = models.IntegerField()
    # 销售量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'


#用户
class User(models.Model):
    #邮箱
    email = models.CharField(max_length=50,unique=True)
    #密码
    password = models.CharField(max_length=255)
    #昵称
    name = models.CharField(max_length=100)
    #头像
    img = models.CharField(max_length=50,default='axf.png')
    #等级
    rank = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_user'


# 购物车 模型类
class Cart(models.Model):
    # 用户[ 添加的这个商品属于哪个用户]
    user = models.ForeignKey(User)
    # 商品[添加哪个商品]
    goods = models.ForeignKey(Goods)
    # 选择数量
    number = models.IntegerField()
    # 是否选中
    isselect = models.BooleanField(default=True)
    #是否删除
    isdelete = models.BooleanField(default=False)

    class Meta():
        db_table = 'axf_cart'


class Order(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 订单号
    identifier = models.CharField(max_length=256)
    # 状态
    # 0 未付款
    # 1 已付款，未发货
    # 2 已发货，未收货
    # 3 已收货，未评级
    # 4 已评价
    # -1 过期.
    status = models.IntegerField(default=0)
    # 创建时间
    createtime = models.DateTimeField(auto_now_add=True)
    #更新时间
    updatetime = models.DateTimeField(auto_now=True)


class OrderGoods(models.Model):
    # 订单
    order = models.ForeignKey(Order)
    # 商品
    goods = models.ForeignKey(Goods)
    # 数量
    number = models.IntegerField()
