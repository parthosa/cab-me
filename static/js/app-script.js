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
	sendDataAjax(data,'/accounts/app/login/','#message_box')
})

$('#verify_otp .submit').click(function(ev){
	ev.preventDefault();
	var data = {
		'otp':$(this).closest('form').find('input[name="otp"]').val(),

	}
	sendDataAjax(data,'/accounts/verify_otp/','#message_box')
})


$('#get_additional_info .submit').click(function(ev){
	ev.preventDefault();
	var data = {
		'phone':$(this).closest('form').find('input[name="phone"]').val(),
		'Email':$(this).closest('form').find('input[name="email"]').val(),

	}
	sendDataAjax(data,'/accounts/social/contact/','#message_box')
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
				$('form').hide();
				$('#verify_otp').show();
			}
			else if(url == '/accounts/app/login/' && response.status == 1){
				location.href='/accounts/login_success'
			}
			else if(url == '/accounts/verify_otp/' && response.status == 1){
				location.href='/accounts/register_success'
			}
			else if(url == '/accounts/app/social/facebook/login/' && response.status == 1){
				$('form').hide();
				$('#get_additional_info').show();
			}
			else if(url == '/accounts/social/contact/' && response.status ==1){
				$('form').hide();
				$('#verify_otp').show();
			}
		}
	});
}


// FACEBOOK LOGIN

function Login()
{

	FB.login(function(response) {
		if (response.authResponse) 
		{
			getUserInfo();
		} else 
		{
			console.log('User cancelled login or did not fully authorize.');
		}
	},{scope: 'email,user_photos,user_videos'});

}

function getUserInfo() {
	var data;
	FB.api('/me', function(response) {
		console.log(response)
		data = {
			'Name': response.name,
			'fbid': response.id
		} 		

		sendDataAjax(data,'/accounts/app/social/facebook/login/')
      // var str="<b>Name</b> : "+response.name+"<br>";
      //     str +="<b>Link: </b>"+response.link+"<br>";
      //     str +="<b>Username:</b> "+response.username+"<br>";
      //     str +="<b>id: </b>"+response.id+"<br>";
      //     str +="<b>Email:</b> "+response.email+"<br>";
      //     str +="<input type='button' value='Get Photo' onclick='getPhoto();'/>";
      //     str +="<input type='button' value='Logout' onclick='Logout();'/>";
      //     document.getElementById("status").innerHTML=str;

  });
}
function getPhoto()
{
	FB.api('/me/picture?type=normal', function(response) {

		var str="<br/><b>Pic</b> : <img src='"+response.data.url+"'/>";
		document.getElementById("status").innerHTML+=str;

	});

}
function Logout()
{
	FB.logout(function(){document.location.reload();});
}