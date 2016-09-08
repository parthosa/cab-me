from django.shortcuts import render
from .models import *
from registration.models import *
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def bookcab(request, user):
	if request.POST:
		b_cab = BookCab()
		b_cab.From = request.POST['From']
		b_cab.To = request.POST['To']
		b_cab.Date = request.POST['Date']
		b_cab.Time = request.POST['Time']
		b_cab.OneWay = request.POST['OneWay']
		b_cab.Sharing = request.POST['Sharing']
	
	cab = Cab.objects.get(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)	
	p_cab = PostCab.objects.get(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)
	D_name = cab.DriverName
	D_pcab = p_cab.users
	Price = distance*7
	price_pcab = p_cab.price
	type_c = cab.Type 
	type_pcab = p_cab.type
	cab_id = cab.id # not for display to users only for returning in the post request to backend
	pcab_id = p_cab.id # not for display to users only for returning in the post request to backend
	resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_c, 'Driver_user': D_pcab, 'Price_posted': price_pcab, 'posted_cab_type': type_pcab, 'cab_id': cab_id, 'pcab_id': pcab_id}

	return JsonResponse(resp)

@login_required
def booknow(request, user):
	user_p = UserProfile.objects.get(user = request.user)
	#if book now in request.POST, partho will return id of the cab booked to the backend
	cab_id = request.POST['cab_id']
	pcab_id = request.POST['pcab_id']
	if (pcab_id == null):
	#try:	
		cab_b = Cab.objects.get(pk = cab_id)
	#except ObjectDoesNotExist:
	else:
		cab_b = PostCab.objects.get(pk = pcab_id)

	user_p.bookedcabs.add(cab_b) 


	

