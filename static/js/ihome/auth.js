function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){

    $('#form-auth').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/ihome/real_auth/',
            type: 'PATCH',
            dataType: 'json',
            success: function(data){
                if(data.code == '200'){
                    location.reload()
                }
                if(data.code == '1005'){
                    $('.error-msg').text(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1006'){
                    $('.error-msg').text(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1007'){
                    $('.error-msg').text(data.msg)
                    $('.error-msg').show()
                }
            }
        })
    });

    $.ajax({
        url: '/ihome/auth_info/',
        type: 'GET',
        dataType: 'json',
        success: function(data){
            console.log(data)
            if(data.data.id_name){
                $('#real-name').val(data.data.id_name)
                $('#real-name').attr('readonly', 'readonly')
                $('#id-card').val(data.data.id_card)
                $('#id-card').attr('readonly', 'readonly')
                $('.btn-success').hide()
            }
        }
    });
})
