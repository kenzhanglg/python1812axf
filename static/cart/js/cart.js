$(function () {
    $('.cart').width(innerWidth)

    total()
    //购物车选中处理
    $('.confirm-wrapper').click(function () {
        var $span = $(this).find('span')
        request_data = {
            'cartid': $(this).attr('data-cartid')
        }

        $.get('/axf/changecartselect/', request_data, function (response) {
            console.log(response)
            if (response.status == 1) {
                if (response.isselect) {
                    $span.removeClass('no').addClass('glyphicon' +
                        ' glyphicon-ok')
                } else {
                    $span.removeClass('glyphicon glyphicon-ok').addClass('no')
                }
                total()
            }
        })
    })


    //全选/取消全选
    $('.cart .all').click(function () {
        var isall = $(this).attr('data-all')
        $span = $(this).find('span')
        //点击取反
        isall = (isall == 'false') ? true : false

        //记录  isall是true还是fales
        $(this).attr('data-all', isall)

        if (isall) {
            $span.removeClass('no').addClass('glyphicon glyphicon-ok')
        } else {
            $span.removeClass('glyphicon glyphicon-ok').addClass('no')
        }
        request_data = {
            'isall': isall
        }
        //ajax请求
        $.get('/axf/changecartall/', request_data, function (response) {
            console.log(response)
            console.log(isall)

            if (response.status == 1) {
                $('.confirm-wrapper').each(function () {
                    if (isall) {//全选
                        $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                    } else { //取消全选
                        $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
                    }
                })
                total()
            }
        })
    })

    // 计算总数金额
    function total() {
        var sum = 0

        $('.cart li').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon').length){
                var price = $content.find('.price').attr('data-price')
                var num = $content.find('.num').attr('data-number')
                sum += price * num
            }
        })

        //显示
        $('.bill .total b').html(sum)
        console.log(sum)
    }

})
