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
	
		cabs = Cab.objects.get(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)	
		p_cabs = PostCab.objects.get(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)
		
		total_cabs = cab + p_cabs
		D_name = []
		Price = []
		type_cab = []
		cab_id = []
		if b_cab.OneWay == True and b_cab.Sharing == True:
			for cab in p_cabs:
				D_pcab = p_cabs.user
				D_pcabuserp = UserProfile.objects.get(user = D_pcab)
				D_name.append(D_pcabuserp.name)
				Price.append(p_cabs.price)
				# price_pcab = p_cabs.price
				# type_c = cab.Type 
				type_cab.append(p_cabs.type)
				cab_id.append(p_cab.cab_id) # not for display to users only for returning in the post request to backend
				# pcab_id = p_cabs.id # not for display to users only for returning in the post request to backend

			for cab in cabs:

				D_name.append(cab.DriverName)
				Price.append(distance*cab.price)
				# price_pcab = p_cab.price
				type_cab.append(cab.Type) 
				cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
				# pcab_id = p_cab.id # not for display to users only for returning in the post request to backend

			resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id}

		elif b_cab.OneWay == True and b_cab.Sharing == False:
			D_name.append(cab.DriverName)
			Price.append(distance*cab.price)
			# price_pcab = p_cab.price
			type_cab.append(cab.Type) 
			cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend

			resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id}
		
		else:
			days = request.POST['Days']
			D_name.append(cab.DriverName)
			Price.append(distance*cab.price)
			# price_pcab = p_cab.price
			type_cab.append(cab.Type) 
			cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
			
			resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id}
		return JsonResponse(resp)

@login_required
@csrf_exempt
def booknow(request, user):
	user_p = UserProfile.objects.get(user = request.user)
	#if book now in request.POST, partho will return id of the cab booked to the backend
	cab_id = request.POST['cab_id']
	# pcab_id = request.POST['pcab_id']
	if not cab_id.startswith('p'): #(pcab_id == null):
	#try:	
		cab_b = Cab.objects.get(pk = cab_id)
	#except ObjectDoesNotExist:
	else:
		cab_b = PostCab.objects.get(pk = cab_id)

	user_p.bookedcabs.add(cab_b) 
	#request.session['feedback'] = cab_b
	key = request.user.id
	cache.set(key,
		{'booked': True})

	resp = {'status': 'success', 'message': 'Your cab has been booked'}

@login_required
@csrf_exempt
def postcab(request):
	user_p = UserProfile.objects.get(user = request.user)
	postcab = PostCab()
	postcab.From = request.POST['From']
	postcab.To = request.POST['To']
	postcab.Date = request.POST['Date']
	postcab.Time = request.POST['Time']
	postcab.Type = request.POST['Type']
	postcab.Smoking = request.POST['Smoking']
	postcab.Pet = request.POST['Pet']
	postcab.Music = request.POST['Music']
	postcab.SeatsAvail = request.POST['Seats']
	postcab.user = request.user
	postcab.price = request.POST['price']
	postcab.save()
	postcab.cab_id = 'p' + postcab.id
	postcab.save()

	resp = {'status': 'Done'}
	return JsonResponse(resp)

@login_required
def feedback(request):
	travelled = cache.get(request.user.id)  #request.session['feedback']
	# if travelled is not None:
	rating = request.POST['rating']
	num_rate = cab_b.num_rate
	new_rating = (num_rate*cab_b.rating + int(rating))/(num_rate+1)
	num_rate+=1
	cache.delete(request.user.id)

	return HttpResponseRedirect('../dashboard/')





