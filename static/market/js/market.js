$(function () {

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


})