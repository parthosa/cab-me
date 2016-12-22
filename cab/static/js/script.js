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
			'OneWay':'True',
			'Sharing':'False',
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Date_return':$(this).closest('.form-data').find('.return-date-data').val(),
			'Class':$(this).closest('.form-data').find('.cab-class').val(),


		}
		
		sendData(data,'../bookcab/');
	});

//	$('#post-cab-form button.form-submit').click(function(){
//		var data={
//			'OneWay':($(this).closest('.form-data').find('input[name="way-opts"]:checked').val()=="One Way")?'True':'False',
//			'From':$(this).closest('.form-data').find('.from-data').val(),
//			'To':$(this).closest('.form-data').find('.to-data').val(),
//			'Date':$(this).closest('.form-data').find('.date-data').val(),
//			'Date_return':($(this).closest('.form-data').find('.return-date-data').val().length==0)?$(this).closest('.form-data').find('.date-data').val():$(this).closest('.form-data').find('.return-date-data').val(),
//			'Class':$(this).closest('.form-data').find('.cab-class').val()
//
//		}
//		console.log(data);
//		
//		sendData(data,'../postcab/');
//
//	});
});


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


//
