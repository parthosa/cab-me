$(document).ready(function(){


$('#register-form .submit').click(function(ev){
	ev.preventDefault();
	var data = {
		'Name':$(this).closest('form').find('input[name="Name"]').val(),
		'Email':$(this).closest('form').find('input[name="Email"]').val(),
		'Contact':$(this).closest('form').find('input[name="Contact"]').val(),
		'Password':$(this).closest('form').find('input[name="Password"]').val(),
		'Password_confirm':$(this).closest('form').find('input[name="Password_confirm"]').val(),

	}
	sendDataAjax(data,'/accounts/register/','#message_box')
})

$('#login-form .submit').click(function(ev){
	ev.preventDefault();
	var data = {
		'email':$(this).closest('form').find('input[name="email"]').val(),
		'password':$(this).closest('form').find('input[name="password"]').val(),

	}
	sendDataAjax(data,'/accounts/login/','#message_box')
})

$('#verify_otp .submit').click(function(ev){
	ev.preventDefault();
	var data = {
		'otp':$(this).closest('form').find('input[name="otp"]').val(),

	}
	sendDataAjax(data,'/accounts/verify_otp/','#message_box')
})
})


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            	break;
            }
        }
    }
    return cookieValue;
}


function sendDataAjax(data,url,updateElement='') {
	data['csrfmiddlewaretoken']=getCookie('csrftoken');
	$(updateElement).html('Please Wait');
	$.ajax({
		type:'POST',
		url:url,
		data:data,
		success:function (response) {
			$(updateElement).html(response.message)

			if(url=='/accounts/register/' && response.status == 1){
				$('#register-form').hide();
				$('#verify_otp').show();
			}
			else if(url == '/accounts/login/' && response.status == 1){
				location.href='/accounts/login_success'
			}
			else if(url == '/accounts/verify_otp/' && response.status == 1){
				location.href='/accounts/register_success'
			}
		}
	});
}