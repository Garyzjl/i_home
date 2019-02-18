//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });

    $.ajax({
        url: '/ihome/my_orders/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data)
            for(i in data.data){
                html = '<li order-id=>'
                html +='    <div class="order-title">'
                html +='        <h3>订单编号：' + data.data[i].order_id + '</h3>'
                html +='        <div class="fr order-operate">'
                html +='            <button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
                html +='        </div>'

                html +='    </div>'
                html +='    <div class="order-content">'
                html +='        <img src="' + data.data[i].image + '">'
                html +='        <div class="order-text">'
                html +='            <h3>订单</h3>'
                html +='            <ul>'
                html +='                <li>创建时间：' + data.data[i].create_date + '</li>'
                html +='                <li>入住日期：' + data.data[i].begin_date + '</li>'
                html +='                <li>离开日期：' + data.data[i].end_date + '</li>'
                html +='                <li>合计金额：' + data.data[i].amount + '元(共' + data.data[i].days + '晚)</li>'
                html +='                <li>订单状态：'
                html +='                    <span>' + data.data[i].status + '</span>'
                html +='                </li>'
                html +='                <li>我的评价：' + data.data[i].comment + '</li>'
                html +='                <li>拒单原因：' + data.data[i].comment + '</li>'
                html +='            </ul>'
                html +='        </div>'
                html +='    </div>'
                html +='</li>'
                $('.orders-list').append(html)
            }
        },
        error: function(){
            alert('error')
        }
    })
});