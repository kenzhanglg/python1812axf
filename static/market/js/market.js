$(function () {

    $('.market').width(innerWidth)

    // var index = localStorage.getItem('index')
    // console.log(index)
    // $('.type-slider li').eq(index).addClass('active')

    var index = $.cookie('index')
    console.log(index)
    // $('.type-slider li').eq(index).addClass('active')
    if (index){ // 有点击，有下标
        $('.type-slider li').eq(index).addClass('active')
    } else {
        $('.type-slider li:first').addClass('active')
    }

    $('.type-slider li').click(function () {
        // $(this).addClass('active')
        // localStorage.setItem('index',$(this).index())
        $.cookie('index', $(this).index(), {expires: 3, path: '/'})

    })

       // 子类
    var categoryShow = false
    $('#category-bt').click(function () {
        // console.log(categoryShow)
        // if (categoryShow){  // 隐藏
        //     categoryShow = false
        //     $('.category-view').hide()
        // } else { // 显示
        //     categoryShow = true
        //     $('.category-view').show()
        // }

        // 取反
        categoryShow = !categoryShow
        categoryShow ? categoryViewShow() : categoryViewHide()
        console.log('子类点击')
    })

    function categoryViewShow() {
        $('.category-view').show()
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        sortViewHide()
        sortShow = false
    }

    function categoryViewHide() {
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    // 排序
    var sortShow = false
    $('#sort-bt').click(function () {
        sortShow = !sortShow
        sortShow ? sortViewShow() : sortViewHide()
        console.log('排序点击')
    })

    function sortViewShow() {
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        categoryViewHide()
        categoryShow = false
    }

    function sortViewHide() {
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    // 灰色蒙层
    $('.bounce-view').click(function () {
        sortViewHide()
        sortShow = false

        categoryViewHide()
        categoryShow = false
    })

/////////////////////////////////////////////////
    //隐藏处理
    // $('.bt-wrapper>.glyphicon-minus').hide()
    // $('.bt-wrapper>i').hide()
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num){
            $(this).prev().show()
            $(this).show()
        }else {
            $(this).prev().hide()
            $(this).hide()
        }
    })



    //点击加操作
    $('.bt-wrapper>.glyphicon-plus').click(function () {
        request_data = {
            'goodsid':$(this).attr('data-goodsid')
        }

        //保存 当前操作按钮对象
        var $that = $(this)

        $.get('/axf/addcart/',request_data,function (response) {
            console.log(response)
            if (response.status == -1){
                //未登录
                $.cookie('back', 'market', {expires: 3, path: '/'})
                window.open('/axf/login/','_self')
            }else if (response.status == 1){//操作成功
                //设置个数
                $that.prev().html(response.number)

                //设置显示
                $that.prev().show()
                $that.prev().prev().show()
            }
        })
    })


    //点击减操作
    $('.bt-wrapper>.glyphicon-minus').click(function () {
        request_data = {
            'goodsid':$(this).attr('data-goodsid')
        }

        var $that = $(this)
        $.get('/axf/subcart/',request_data,function (response) {
            console.log(response)
             if (response.status == 1){//操作成功
                if (response.number){
                    $that.next().html(response.number)
                }else{
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })

})