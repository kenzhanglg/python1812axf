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

#axf_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,marketprice1,img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3)
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

# insert into axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum) values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=255)
    productname = ''
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField()
    pmdesc = models.IntegerField()
    specifics = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=2)
    marketprice = models.FloatField()
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(max_length=200)
    dealerid = models.CharField(max_length=20)
    storenums = models.IntegerField()
    productnum = models.IntegerField()
    class Meta:
        db_table = 'axf_goods'
