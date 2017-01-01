$(document).ready(function(){

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
	    jsonPath : "data.json" ,
  });


	$('.cab-opts li').click(function() {
		$('.cab-opts li').removeClass('active');
		$(this).addClass('active');
		id=$(this).attr('id');
		$('.form-data').hide();
		$('#'+id+'-form').show();
	})

	$('input[name="OneWay"]').on('change',function(){
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


function sendDataAjax(data,url,updateElement) {
	data['csrfmiddlewaretoken']=getCookie('csrftoken');
	$(updateElement).html('');
	$.ajax({
		type:'POST',
		url:url,
		data:data,
		success:function (response) {
				$(updateElement).html(response.message);
		},
		error:function(response){
			console.error(response)
		}
	});
}


function lightbox_trigger(lightbox_name,show_temp){
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
	location.hash=block;
	$('.dashboard-details').hide();
	$('.' + block).show().css({
		'display':'flex'
	});
})

$('#edit_profile').click(function () {
	$('.personal-info .dashboard-info-input').addClass('editable');
	$(this).hide();
	$('#save_profile,#cancel_profile').show();
})

$('#cancel_profile').click(function () {
	$('.personal-info .dashboard-info-input').removeClass('editable');
	$('#edit_profile').show();
	$('#save_profile,#cancel_profile').hide();
})

$('#save_profile').click(function () {
	var dashboard=$('.personal-info');
	var data={
		name:dashboard.find('#name').val(),
		email:dashboard.find('#email').val(),
		phone:dashboard.find('#phone').val(),
	}
	sendData(data,'../updateProfile');
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
		$('form#login-form').show();
	}
	else{
		$('.form-inner form').hide();
		$('form#register-form').show();
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

if(location.pathname=="/dashboard/"){
	var tab = location.hash.substr(1);
	if(tab=="")
		tab="personal-info"
	location.hash=tab
	$('.inner-dash ul li').removeClass('active');
	$('.inner-dash ul li').map(function(i,e){
		if($(e).attr('data-block')==tab){
			$(e).addClass('active')
		}
	});

	$('.dashboard-details').hide();
	$('.'+tab).show();
}