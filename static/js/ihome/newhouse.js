function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get('/ihome/facility/', function(data){
        console.log(data)
        for (i in data.data){
            html = ' <li>'
            html += '    <div class="checkbox">'
            html += '         <label>'
            html += '              <input type="checkbox" name="facility" value="'+ data.data[i].id +'">' + data.data[i].name + ''
            html += '         </label>'
            html += '    </div>'
            html += '</li>'
            $('.clearfix').append(html)
        }
    });

    $.get('/ihome/area/', function(data){
        console.log(data)
        for (i in data.data){
            html = '<option value="' + data.data[i].id + '">' + data.data[i].name + '</option>'
            $('.form-control').append(html)
        }
    });

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/ihome/get_house/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                console.log(data)
                if(data.code == '200'){
                    $('#form-house-info').hide()
                    $('#form-house-image').show()
                    $('#house-id').attr('value', data.data.id)
                }
            }
        });
    });

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/ihome/house_image/',
            type: 'PATCH',
            dataType: 'json',
            success: function(data){
                console.log(data)
                if(data.data.length == 1){
                        html = '<img src="' + data.data[0] + '">'
                        $('.house-image-cons').append(html)
                }else{
                    $('.house-image-cons').children().remove()
                    for(i in data.data){
                        html = '<img src="' + data.data[i] + '">'
                        $('.house-image-cons').append(html)
                    }
                }
            },
            error: function(){
                alert('error')
            }
        });
    });
})