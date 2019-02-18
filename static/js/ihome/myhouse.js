$(document).ready(function(){
    $.ajax({
        url: '/ihome/auth_info/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            if(data.data.id_name !== null){
                $('.auth-warn').hide()
                $('#houses-list').show()
            }else{
                $(".auth-warn").show()
                $('#houses-list').hide()
            }
        }
    });

    $.get('/ihome/my_house/', function(data){
        console.log(data)
        for(i in data.data){
            html = '<li>'
            html += '        <a href="' + '/ihome/detail/' + '?house_id=' + data.data[i].id + '">'
            html += '            <div class="house-title">'
            html += '                <h3>房屋ID:' + data.data[i].id + '——' + data.data[i].title + '</h3>'
            html += '            </div>'
            html += '            <div class="house-content">'
            html += '                <img src="' + data.data[i].image + '">'
            html += '                <div class="house-text">'
            html += '                    <ul>'
            html += '                        <li>位于：' + data.data[i].area + '</li>'
            html += '                        <li>价格：￥' + data.data[i].price + '/晚</li>'
            html += '                        <li>发布时间：' + data.data[i].create_time + '</li>'
            html += '                    </ul>'
            html += '                </div>'
            html += '            </div>'
            html += '        </a>'
            html += '    </li>'
            $('#houses-list').append(html)
        }
    })
})