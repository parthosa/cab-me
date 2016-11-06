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

	$('input[name="way-opts"').on('change',function(){
		if($(this).val()=='One Way'){
			$(this).closest('.form-data').find('.return-date-data').attr('disabled','')
		}
		else
			$(this).closest('.form-data').find('.return-date-data').removeAttr('disabled','false')

	})

	$('#outstation-form button.form-submit').click(function(){
		var data={
			'From':$
		}
	})
})