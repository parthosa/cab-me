

	$("#owl-demo-1").owlCarousel({
 
      slideSpeed : 500,
      autoPlay : 3000,
      pagination:false,
      singleItem:true
 
 
  });
	$("#owl-demo-2").owlCarousel({
 
      slideSpeed : 500,
      autoPlay : 7000,
      pagination:false,
      singleItem:true
 
 
  });

	$("#owl-demo-3").owlCarousel({
	    jsonPath : "/static/data.json" ,
  });


	$('.cab-opts li').click(function() {
		$('.cab-opts li').removeClass('active');
		$(this).addClass('active');
		id=$(this).attr('id');
		$('.form-data').hide();
		$('#'+id+'-form').show();
	})

	$('input[name=OneWay]').on('change',function(){
		console.log('change');
		if($(this).val()=='One Way'){
			$(this).closest('.form-data').find('.return-date-data').val('');
			$(this).closest('.form-data').find('.return-date-data').attr('disabled','')
		}
		else{
			$(this).closest('.form-data').find('.return-date-data').removeAttr('disabled','false')
		}
	});


	var cityList=[
		'Delhi',
		'Mumbai',
		'Kolkata',
		'Dehradun'
	];
	
	$('.from-data').autocomplete({
      source: function( request, response ) {
	        $.ajax( {
	          url: "../cab/cities/",
	          success: function( data ) {
	            response( data.cities );
	          }
	        } );
	    }
    }
    );
    $('.to-data').autocomplete({
      source: function( request, response ) {
	        $.ajax( {
	           url: "../cab/cities/",
	          success: function( data ) {
	            response( data.cities );
	          }
	        } );
	    }
    }
    );

    $('.date-data,.return-date-data').datepicker({
    	dateFormat: "dd/mm/yy"
    });


	$('#outstation-form button.form-submit').click(function(){
		var data={
			'OneWay':$(this).closest('.form-data').find('input[name=OneWay]:checked').val(),
			'Sharing':$(this).closest('.form-data').find('input[name=Sharing]:checked').val(),
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Date_return':$(this).closest('.form-data').find('.return-date-data').val(),
			'Class':$(this).closest('.form-data').find('.cab-class').val(),


		}
		
		sendData(data,'../bookcab/');
	});

	$('#post-cab-form button.form-submit').click(function(){
		var data={
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Rate':$(this).closest('.form-data').find('.rate-data').val(),
			'Smoking':$(this).closest('.form-data').find('input[name=smoking]:checked').val(),
			'Pet':$(this).closest('.form-data').find('input[name=pets]:checked').val(),
			'Music':$(this).closest('.form-data').find('input[name=music]:checked').val(),
			'Time':$(this).closest('.form-data').find('.time-hr-data').val() + ' '+ $(this).closest('.form-data').find('.time-min-data').val() +' '+$(this).closest('.form-data').find('.time-type-data').val(),
			'Seats':$(this).closest('.form-data').find('#post-cab-seats').val(),
			'Type':$(this).closest('.form-data').find('#post-cab-type').val()

		}
		
		response = sendDataAjax(data,'../postcab/','#post-cab-message');
		lightbox_trigger('post-cab-wrap',true);
	});


	$('#self-drive-form button.form-submit').click(function(){
		var data={
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Date_return':$(this).closest('.form-data').find('.return-date-data').val(),


		}
		
		sendData(data,'../self_drive/');
	});



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

function sendData(data,url){
	var form=document.createElement('form');
	form.method="POST";
	form.action=url;
	var input;
	for(key in data){
		input=document.createElement('input');
		input.name=key;
		input.value=data[key];
		input.type='hidden';
		form.appendChild(input)
	}
	form.submit();
}


function sendDataAjax(data,url,updateElement='') {
	data['csrfmiddlewaretoken']=getCookie('csrftoken');
	$(updateElement).html('');
	$.ajax({
		type:'POST',
		url:url,
		data:data,
		success:function (response) {
				if(url=='/accounts/login/'){
					if(response.status ==1){
						location.href='/dashboard/'
					}
					else if(response.status==0){
						$(updateElement+'.fail').html(response.message);
					}
				}
				else if(url=='/accounts/logout/'){
					if(response.status ==1)
						location.href='/main/'
					}
				else if(url=='/accounts/register/'){
					if(response.status == 1){
						$(updateElement+'.success').html(response.message);
						setTimeout(lightbox_trigger('verify_otp'),200);
					}
					else if(response.status == 0)
						$(updateElement+'.fail').html(response.message);
				}
				else if(url=='/accounts/reset_password/')
				{
					if(response.status == 1)
						$(updateElement+'.success').html(response.message);
					else if(response.status == 0)
						$(updateElement+'.fail').html(response.message);
				}
				else if(url == '/accounts/social/facebook/login/')
				{
					if(response.status == 2)
						lightbox_trigger('additional-info')
					else
						location.pathname='/dashboard/'
					$(updateElement).html(response.message);

					// var data;
					//  FB.api('/me', function(response) {
					//  	data = {
					// 		'Email': response.email,
					// 		'Name': response.name,
					// 		'fbid': response.id
					// 	}
					// });
					// console.log(data)
				}
				else if(url == '/accounts/social/contact/' && response.status == 1)
				{
					lightbox_trigger('verify_otp')
					$(updateElement).html(response.message);

				}
				
				else if(url == '/accounts/verify_otp/' && response.status == 1)
				{
					setTimeout(function(){
						lightbox_trigger('login-reg')
					},1000);
					$(updateElement).html(response.message);
				}
				else if(url.includes('/refferal/invite')){
					if(response.status == 1){
						$(updateElement+'.success').html(response.message);
						setTimeout(lightbox_trigger('verify_otp'),200);
					}
					else if(response.status == 0)
						$(updateElement+'.fail').html(response.message);
				}
				else{
					$(updateElement).html(response.message);
				}
				
		},
		error:function(response){
			console.error(response)
		}
	});
}


function lightbox_trigger(lightbox_name,show_temp=false){
	$('.lightbox-inner').hide();
	$('.lightbox-wrapper').fadeIn();
	if(show_temp==true){
		$('.temp').show().css({
			display:'flex'
		});
		setTimeout(function () {
			$('.temp').hide();
			$('.'+lightbox_name).show();
		},1000);
	}
	else{
		$('.'+lightbox_name).show();

	}

}

//  select cab from search page 

$('.cab-select-submit').click(function(){
	var data={
		'cab_id':$(this).closest('.search-results').attr('cab-id')
	};
	sendData(data,'../summary/');
})


// final submit
$('#final-submit').click(function () {
	var data={
			'cab_id':$('.summary-headers').attr('cab-id'),
			'Sharing':$(this).closest('.form-data').find('input[name=Sharing]:checked').val(),
			'Phone':$(this).closest('.form-data').find('.phone-data').val(),
			'Pickup Time':$(this).closest('.form-data').find('.time-hr-data').val() + ' '+ $(this).closest('.form-data').find('.time-min-data').val() +' '+$(this).closest('.form-data').find('.time-type-data').val(),
			'Pickup Address':$(this).closest('.form-data').find('.pickup-address-data').val(),
		}	
	sendData(data,'../booknow/');
})


$('#sign-in-trigger').click(function () {
	$('.message-login').html('');
	$('input').val('');
	lightbox_trigger('login-reg',false);
})

$('#sign-in').click(function (ev) {
	ev.preventDefault();
	var data={
		email:$(this).closest('#login-form').find('input[name=email]').val(),
		password:$(this).closest('#login-form').find('input[name=password]').val()
	}
	sendDataAjax(data,'/accounts/login/','.message-login');
})


$('#sign-up').click(function (ev) {
	ev.preventDefault();
	var data={
		Name:$(this).closest('#register-form').find('input[name=name]').val(),
		Contact:$(this).closest('#register-form').find('input[name=phone]').val(),
		Email:$(this).closest('#register-form').find('input[name=email]').val(),
		Password:$(this).closest('#register-form').find('input[name=password]').val(),
		Password_confirm:$(this).closest('#register-form').find('input[name=password_confirm]').val()
	}
	sendDataAjax(data,'/accounts/register/','.message-login');
})


$('#refer-sign-up').click(function (ev) {
	ev.preventDefault();
	var data={
		Name:$(this).closest('#register-form').find('input[name=name]').val(),
		Contact:$(this).closest('#register-form').find('input[name=phone]').val(),
		Email:$(this).closest('#register-form').find('input[name=email]').val(),
		Password:$(this).closest('#register-form').find('input[name=password]').val(),
		Password_confirm:$(this).closest('#register-form').find('input[name=password_confirm]').val()
	}
	sendDataAjax(data,location.pathname,'.message-login');
})




$('#reset-pass').click(function(ev){
	ev.preventDefault();
	var data={
		Email:$(this).closest('#forgot-pass-form').find('input[name=email]').val(),
	}
	sendDataAjax(data,'/accounts/reset_password/','.message-login');

})

	
$('.lightbox-wrapper .close,.lightbox-overlay').click(function () {
	$('.lightbox-wrapper').fadeOut();
})


$('.inner-dash ul li').click(function () {
	$('.inner-dash ul li').removeClass('active');
	$(this).addClass('active');
	var block=$(this).attr('data-block');

	if(block == 'earn-money')
		sendDataAjax({},'/refferal/get_invite_url/','#invite_message')
	location.hash=block;
	$('.dashboard-details').hide();
	$('.' + block).show().css({
		'display':'flex'
	});
})

var dashboard=$('.personal-info');
var profileData;
$('#edit_profile').click(function () {
	
	profileData={
		name:dashboard.find('#name').val(),
		email:dashboard.find('#email').val(),
		phone:dashboard.find('#phone').val(),
	}
	$('.personal-info .dashboard-info-input:not(#phone)').removeAttr('readonly');
	$('.personal-info .dashboard-info-input:not(#phone)').addClass('editable');
	$(this).hide();
	$('#save_profile,#cancel_profile').show();
})

$('#cancel_profile').click(function () {

	dashboard.find('#name').val(profileData.name),
	dashboard.find('#email').val(profileData.email),
	dashboard.find('#phone').val(profileData.phone),

	$('.personal-info .dashboard-info-input').removeClass('editable');
	$('#edit_profile').show();
	$('#save_profile,#cancel_profile').hide();
})

$('#save_profile').click(function () {
	profileData={
		name:dashboard.find('#name').val(),
		email:dashboard.find('#email').val(),
	}
	sendData(profileData,'../updateProfile');
})

$('#save_password').click(function () {
	var dashboard=$('.change-pass');
	var data={
		current_password:dashboard.find('#current_password').val(),
		new_password:dashboard.find('#new_password').val(),
		confirm_password:dashboard.find('#confirm_password').val(),
	}
	sendData(data,'../updatePassword');
})

//  login reg form
$('.login-reg .headers li').click(function () {
	$('.login-reg .headers li').removeClass('active');
	$(this).addClass('active');
	if($(this).html()=='Sign In'){
		$('.form-inner form').hide();
		$('form#login-form').show().css('display','flex');
	}
	else{
		$('.form-inner form').hide();
		$('form#register-form').show().css('display','flex');
	}
})


$('.forgot-pass').click(function(){
	$('.login-reg .headers li').removeClass('active');
	$('.form-inner form').hide();
	$('#forgot-pass-form').show().css({
		display:'flex'
	});
})

$('#view_bookings').click(function(){
	location.href="/dashboard/#booking-history"
})


$('#social-info-submit').click(function(ev){
	ev.preventDefault();
	var data = {
			'phone':$(this).closest('form').find('input[name=phone]').val(),
			'Email':$(this).closest('form').find('input[name=email]').val(),
	}
	sendDataAjax(data,'/accounts/social/contact/','.message.fail')
})


$('#otp-submit').click(function(ev){
	ev.preventDefault();
	var data = {
			'otp':$(this).closest('form').find('input[name=otp]').val(),
	}
	sendDataAjax(data,'/accounts/verify_otp/','.message.fail')
})



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

        sendDataAjax(data,'/accounts/social/facebook/login/')
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