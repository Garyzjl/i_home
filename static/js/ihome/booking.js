function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24);
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var house_id = location.search.split('=')[1]
    $.ajax({
        url: '/ihome/house_detail/?house_id=' + house_id,
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data)
            $('.house-text h3').text(data.data.title)
            $('.house-text p span').text(data.data.price)
            $('.house-info img').attr('src', data.data.images[0])
        },
        error: function(){
            alert('error')
        }
    });
    $('.submit-btn').click(function(e){
        e.preventDefault();
        var start_date = $('#start-date').val();
        var end_date = $('#end-date').val();
        $.ajax({
            url: '/ihome/my_booking/',
            type: 'POST',
            dataType: 'json',
            data: {'house_id': house_id, 'start_date': start_date, 'end_date': end_date},
            success: function(data){
                alert('提交成功')
                location.href = '/ihome/orders/'
            },
            error: function(){
                alert('error')
            }
        });
    })

})
