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

	$('#post-cab-form button.form-submit').click(function(){
		var data={
			'OneWay':($(this).closest('.form-data').find('input[name="way-opts"]:checked').val()=="One Way")?'True':'False',
			'From':$(this).closest('.form-data').find('.from-data').val(),
			'To':$(this).closest('.form-data').find('.to-data').val(),
			'Date':$(this).closest('.form-data').find('.date-data').val(),
			'Date_return':($(this).closest('.form-data').find('.return-date-data').val().length==0)?$(this).closest('.form-data').find('.date-data').val():$(this).closest('.form-data').find('.return-date-data').val(),
			'Class':$(this).closest('.form-data').find('.cab-class').val()

		}
		console.log(data);
		
		sendData(data,'../postcab/');

	});
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


// Routes Page

var places=location.search.substr(1).split('-');
var place1=places[0][0].toUpperCase() + places[0].substring(1);
var place2=places[1][0].toUpperCase() + places[1].substring(1);
$('.place1').html(place1);
$('.place2').html(place2);
    $('.map-wrapper')
      .gmap3({
        mapTypeId : google.maps.MapTypeId.ROADMAP,
        navigationControl: false,
        scrollwheel: false,
        streetViewControl: false
      })
      .route({
        origin:$('.place1').html(),
        destination:$('.place2').html(),
        travelMode: google.maps.DirectionsTravelMode.DRIVING
      })
      .directionsrenderer(function (results) {
        if (results) {
        	$('.map-distance').html(results.routes["0"].legs["0"].distance.text);
        	$('.map-duration').html(results.routes["0"].legs["0"].duration.text);
          return {
            panel: $("<div></div>").addClass("gmap3").insertAfter($(".smap-wrapper")), // accept: string (jQuery selector), jQuery element or HTML node targeting a div
            directions: results
          }
        }
      })


$.ajax({
	type:'POST',
	url:'/static/routes.json',
	success:function(response){
		var data=JSON.parse(response).response;
		data.map(function(ele,i){
			console.log(ele);
				if(ele.place1==place1&&ele.place2==place2){
					ele.cabs.map(function(cabE){
						console.log(cabE);

						var cabItem=$('.cab-item:nth-of-type(1)').clone();
						cabItem.show();
						cabItem.css({
							display:'flex'
						})
						cabItem.find('.vehicle-type').html(cabE.vehicle);
						cabItem.find('.km-rate').html(cabE.kmRate);
						cabItem.find('.other-charges').html(cabE.otherCharges);
						cabItem.find('.min-km-day').html(cabE.minKmDay);
						$('.cab-list').append(cabItem);
					})

					ele.places.map(function(placeE){
						var placesList=$('.places-list li:nth-of-type(1)').clone();
						placesList.show();
						placesList.find('.other-place').html(placeE);
						$('.places-list').append(placesList);
					})
				}
		})
	}
})

$(document).on('click','.places-list li',function () {
	var p1=$(this).find('.place1').html().toLowerCase();
	var p2=$(this).find('.other-place').html().toLowerCase();
	location.href=location.href.substr(0,location.href.indexOf('?'))+'?'+p1+'-'+p2;
})