
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