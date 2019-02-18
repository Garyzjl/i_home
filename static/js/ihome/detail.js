function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    $(".book-house").show();

    var url = location.search
    var house_id = url.split('=')[1]
    $.ajax({
        url: '/ihome/house_detail/?house_id='+ house_id,
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data)
            for(i in data.data.images){
                    html = '<li class="swiper-slide"><img src="' + data.data.images[i] + '"></li>'
                    $('.swiper-wrapper').append(html)
            }
            var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction',
            })
            $('.house-price span').text(data.data.price)
            $('.house-title').text(data.data.title)
            $('.landlord-pic img').attr('src', '/static/media/' + data.data.user_avatar)
            $('.landlord-name').text(data.data.user_name)
            $('.text-center li').text(data.data.address)
            $('#rent_count span').text(data.data.room_count)
            $('#house_area span').text(data.data.acreage)
            $('#house_unit span').text(data.data.unit)
            $('#live_count span').text(data.data.capacity)
            $('#bed_config p').text(data.data.beds)
            $('#deposit span').text(data.data.deposit)
            $('#min_days span').text(data.data.min_days)
            if(data.data.max_days != '0'){
                $('#min_days span').text(data.data.max_days)
            }
            for(i in data.data.facilities){
                html = '<li><span class="' + data.data.facilities[i].css + '"></span>' + data.data.facilities[i].name + '</li>'
                $('.house-facility-list').append(html)
            }
            $('.book-house').attr('href', '/ihome/booking/?house_id=' + house_id)
//            $('.book-house').hide()

        },
        error: function(){
            alert('error')
        }
    });

})