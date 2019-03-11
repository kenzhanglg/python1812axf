$(function () {
    $('.register').width(innerWidth)

    // 邮箱验证(失去焦点blur，即是输入完成后验证)
    $('#email input').blur(function () {

        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); //正则表达式

        // 空，不需要验证处理
        if($(this).val() == '') return

        //格式是否正确
        if (reg.test($(this).val())) { //符合
            request_data = {
                'email':$(this).val()
            }
            // jQuery.get( url [, data ] [, success(data, textStatus, jqXHR) ] [, dataType ] )
            //ajax 请求
            // attr() 方法设置或返回被选元素的属性值。
            $.get('/axf/checkemail',request_data,function (response) {
                if(response.status){  //可用
                    $('#email-t').attr('data-content', '恭喜你账号是可用').popover('hide')
                    $('#email').removeClass('has-error').addClass('has-success')
                    $('#email>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
                }else{  //不可用
                    $('#email-t').attr('data-content', response.msg).popover('show')
                    $('#email').removeClass('has-success').addClass('has-error')
                    $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
                }

            })

        }else{  //不符合正则匹配
            $('#email-t').attr('data-content', '数据格式不正确').popover('show')
                    $('#email').removeClass('has-success').addClass('has-error')
                    $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')

        }
    })


        // 密码验证
    $('#password input').blur(function () {
        var reg = new RegExp("^[a-zA-Z0-9_]{6,10}"); //正则表达式
        // 空，不需要验证处理
        if($(this).val() == '') return
        //格式是否正确
        if (reg.test($(this).val())) {
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else{  //不可用
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    //验证第二次密码
    $('#password-d input').blur(function () {
        if($(this).val() == '') return

        var f_val = $('#password input').val()
        var d_val = $('#password-d input').val()

        //两次输入的密码是否相同
        if(f_val == d_val){//相同
            // $("#password-t").attr('data-content', '密码正确').popover('hide')
            $("#password-t").popover('hide')
            $('#password-d').removeClass('has-error').addClass('has-success')
            $('#password-d>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else{ //不相同
            $("#password-t").popover('show')
            $('#password-d').removeClass('has-success').addClass('has-error')
            $('#password-d>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    //验证昵称
    $('#name input').blur(function () {
        if ($(this).val() == '') return

        if ($(this).val().length>=3 && $(this).val().length<=10 ){ //符合
            $('#name').removeClass('has-error').addClass('has-success')
            $('#name>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }  else{
            $('#name').removeClass('has-success').addClass('has-error')
            $('#name>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    //注册按钮
    $('#subButton').click(function () {
        var isregister  = true
        $('.register .form-group').each(function () {
            if (!$(this).is('.has-success')){
                isregister = false
            }
        })

        if (isregister){ //允许注册
            $('.register form').submit()
        }
    })


})