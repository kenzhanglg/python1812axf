$(function () {
    $('#alipay').click(function () {

        request_data = {
            'orderid':$(this).attr('data-orderid')
        }
        //发起支付请求
        $.get('/axf/pay/',request_data,function (response) {
            console.log(response)
            if (response.status == 1){
                window.open(response.alipayurl,target='_self')
            }
        })
    })

})