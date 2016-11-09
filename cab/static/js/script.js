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

	$('input[name="way-opts"]').on('change',function(){
		if($(this).val()=='One Way'){
			$(this).closest('.form-data').find('.return-date-data').attr('disabled','')
		}
		else
			$(this).closest('.form-data').find('.return-date-data').removeAttr('disabled','false')
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
			'One Way':$(this).closest('.form-data').find('input[name="way-opts"]:checked').val(),
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Return-Date':$(this).closest('.form-data').find('.return-date-data').val(),
			'Class':$(this).closest('.form-data').find('.cab-class').val()

		}
		console.log(data);
		// $.ajax({
		// 	type:'POST',
		// 	url:'../bookcab/',
		// 	data:data,
		// 	success:function(response){
		// 		console.log(response);
		// 		location.reload();
		// 	}
		// })

		sendData(data,'../bookcab/');
	});

	$('#post-cab-form button.form-submit').click(function(){
		var data={
			'One Way':$(this).closest('.form-data').find('input[name="way-opts"]:checked').val(),
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Return-Date':$(this).closest('.form-data').find('.return-date-data').val(),
			'Class':$(this).closest('.form-data').find('.cab-class').val()

		}
		console.log(data);
		// $.ajax({
		// 	type:'POST',
		// 	url:'../postcab/',
		// 	data:data,
		// 	success:function(response){
		// 		console.log(response);
		// 	}
		// })
		sendData(data,'../postcab/');

	});
});


function sendData(data,url){
	var xhr=new XMLHttpRequest();
	var formData = new FormData();

	for(key in data){
		formData.append(key,data[key])
	}

	xhr.addEventListener('error',function(){
		alert('Please Try Again');
	})

	xhr.open('POST',url);
	xhr.send(formData);
}