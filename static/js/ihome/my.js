function logout() {
    $.get("/ihome/logout/", function(data){
        if(data.code == '200'){
            location.href = "/ihome/index/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/ihome/user_info/',
        dataType: 'json',
        type: 'GET',
        success: function(data){
            console.log(data)
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src','/static/media/' + data.data.avatar)
        }
    })
})