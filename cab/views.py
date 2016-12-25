from django.shortcuts import render
from .models import *
from registration.models import *
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
from django.core.exceptions import ObjectDoesNotExist


def index(request):
	if request.user.id == None:
		return render(request, 'cab/index.html')
		print request.user
	elif request.user.username == 'admin':
		context = {'name': 'admin'}
		return render(request, 'cab/index.html', context)
	else:
		user = request.user
		print user.username
		customer = UserProfile.objects.get(email_id = user.username)
		name = customer.name
		context = {'name': name}
		return render(request, 'cab/index.html', context)

def hotels(request):
	return render(request, 'cab/hotels.html')

def flights(request):
	return render(request, 'cab/flights.html')

def bus(request):
	return render(request, 'cab/bus.html')


def search(request):
	return render(request, 'cab/search.html')

@csrf_exempt
def summary(request):
	print request.POST['cab_id']
	return render(request, 'cab/summary.html')

def blog(request):
	return render(request, 'cab/blog.html')

def about(request):
	return render(request, 'cab/about.html')

def faq(request):
	return render(request, 'cab/faq.html')


def career(request):
	return render(request, 'cab/career.html')



def privacy_policy(request):
	return render(request, 'cab/privacy_policy.html')


def press_release(request):
	return render(request, 'cab/press_release.html')

def terms_and_conditions(request):
	return render(request, 'cab/terms_and_conditions.html')

def routes(request):
	return render(request, 'cab/routes.html')

def cab_cities(request):
	cities = City.objects.all()
	c_name = []
	x = 0
	for city in cities:
		c_name.append(city.name)
		x+=1
	resp = {'cities': c_name}
	return JsonResponse(resp)

@csrf_exempt
def bookcab(request):
	if request.POST:
		b_cab = BookCab()
		b_cab.From = request.POST['From']
		b_cab.To = request.POST['To']
		b_cab.Date = request.POST['Date']
		b_cab.Date_return = request.POST['Date_return']
		# b_cab.Time = request.POST['Time']
		if request.POST['OneWay'] == 'One Way':
			b_cab.OneWay = True
		else: 
			b_cab.OneWay = False

		if request.POST['Sharing'] == 'Sharing':
			b_cab.Sharing = True
		else: 
			b_cab.Sharing = False
		try:
			cabs = Cab.objects.filter(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)	
			print cabs
		except ObjectDoesNotExist:
			pass
		try:
			p_cabs = PostCab.objects.filter(From = b_cab.From, To = b_cab.To, Date = b_cab.Date)
		except ObjectDoesNotExist:
			pass
		try:
			share_cabs = BookCab.objects.filter(From = b_cab.From, To = b_cab.To, Date = b_cab.Date, Sharing = True)	
		except ObjectDoesNotExist:
			pass
			
		D_name = []
		D_phone = []
		Price = []
		type_cab = []
		cab_id = []
		cust_names = []
		From = []
		To = []
		Date = []
		Date_return = []
		# Time = []
		OneWay = []
		Sharing = []

		if b_cab.OneWay == True and b_cab.Sharing == True:
			try:
				for cab in p_cabs:
					D_pcab = p_cabs.user
					D_pcabuserp = UserProfile.objects.get(user = D_pcab)
					D_name.append(D_pcabuserp.name)
					D_phone.append(D_pcabuserp.phone)
					Price.append(p_cabs.price)
					# price_pcab = p_cabs.price
					# type_c = cab.Type 
					type_cab.append(p_cabs.type)
					cab_id.append(p_cab.cab_id) # not for display to users only for returning in the post request to backend
					# pcab_id = p_cabs.id # not for display to users only for returning in the post request to backend
					cust_names.append(D_pcabuserp.name)
					From.append(b_cab.From)
					To.append(b_cab.To)
					Date.append(b_cab.Date)
					Date_return.append(b_cab.Date_return)
					# Time.append(b_cab.Time)
					OneWay.append(b_cab.OneWay)
					Sharing.append(b_cab.Sharing)
			except:
				pass

			try:
				for cab in share_cabs:

					D_name.append(cab.DriverName)
					D_phone.append('9982312111')
					Price.append(distance*cab.price)
					# price_pcab = p_cab.price
					type_cab.append(cab.Type) 
					cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
					# pcab_id = p_cab.id # not for display to users only for returning in the post request to backend
					cust_names = [customer.name for customer in cab.Cust]
					From.append(b_cab.From)
					To.append(b_cab.To)
					Date.append(b_cab.Date)
					Date_return.append(b_cab.Date_return)
					# Time.append(b_cab.Time)
					OneWay.append(b_cab.OneWay)
					Sharing.append(b_cab.Sharing)
			except:
				pass
			try:
				for cab in cabs:

					D_name.append(cab.DriverName)
					D_phone.append('9982312111')
					Price.append(distance*cab.price)
					# price_pcab = p_cab.price
					type_cab.append(cab.Type) 
					cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
					# pcab_id = p_cab.id # not for display to users only for returning in the post request to backend
					cust_names.append('none')
					From.append(b_cab.From)
					To.append(b_cab.To)
					Date.append(b_cab.Date)
					Date_return.append(b_cab.Date_return)
					# Time.append(b_cab.Time)
					OneWay.append(b_cab.OneWay)
					Sharing.append(b_cab.Sharing)

				cab_response = []
				for x in range(0, len(D_name)):
					cab_response.append({'Driver_name': D_name[x],'Driver_phone':D_phone[x], 'Price': Price[x], 'Cab_type': type_cab[x], 'cab_id': cab_id[x], 'cust_names': cust_names[x]})
					x+=1
					# cab_response_dict['Driver_name': name]
					# cab_response_dict['Price': name]
					# cab_response_dict['Cab_type': name]
					# cab_response_dict['cab_id': name]
					# cab_response_dict['cust_names': name]
				# resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id, 'cust_names': cust_names ,'From': From, 'To': To, 'Date': Date, 'Date_return': Date_return, 'OneWay': OneWay, 'Sharing': Sharing}
				resp = {'cabs':cab_response, 'From': b_cab.From, 'To': b_cab.To, 'Date': b_cab.Date, 'Date_return': b_cab.Date_return, 'OneWay': b_cab.OneWay, 'Sharing': b_cab.Sharing}
				print 1
				return render(request, 'cab/search.html', resp)
			except:
				resp = {'status': 'No cabs Found', 'From': b_cab.From, 'To': b_cab.To, 'Date': b_cab.Date, 'Date_return': b_cab.Date_return, 'OneWay': b_cab.OneWay, 'Sharing': b_cab.Sharing}
				print 2
				return render(request, 'cab/search.html', resp)

		elif b_cab.OneWay == True and b_cab.Sharing == False:
			for cab in cabs:# try:
				D_name.append(cab.DriverName)
				D_phone.append('9982312111')
				Price.append(200*cab.price)
				# price_pcab = p_cab.price
				type_cab.append(cab.Type) 
				cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
				From.append(b_cab.From)
				To.append(b_cab.To)
				Date.append(b_cab.Date)
				Date_return.append(b_cab.Date_return)
				# Time.append(b_cab.Time)
				OneWay.append(b_cab.OneWay)
				Sharing.append(b_cab.Sharing)
			cab_response = []
			for x in range(0, len(D_name)):
				cab_response.append({'Driver_name': D_name[x],'Driver_phone':D_phone[x], 'Price': Price[x], 'Cab_type': type_cab[x], 'cab_id': cab_id[x]})
				x+=1
				# cab_response_dict['Driver_name': name]
				# cab_response_dict['Price': name]
				# cab_response_dict['Cab_type': name]
				# cab_response_dict['cab_id': name]
				# cab_response_dict['cust_names': name]
			# resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id, 'cust_names': cust_names ,'From': From, 'To': To, 'Date': Date, 'Date_return': Date_return, 'OneWay': OneWay, 'Sharing': Sharing}
			resp = {'cabs':cab_response, 'From': b_cab.From, 'To': b_cab.To, 'Date': b_cab.Date, 'Date_return': b_cab.Date_return, 'OneWay': b_cab.OneWay, 'Sharing': b_cab.Sharing}			
			# resp = {'Driver_name': D_name, 'D_phone': D_phone, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id,'From': From, 'To': To, 'Date': Date, 'Date_return': Date_return, 'OneWay': OneWay, 'Sharing': Sharing}
			print resp
			return render(request, 'cab/search.html', resp)
			# except:
			# 	print 'some'
			# 	resp = {'status': 'No cabs Found'}
			# 	return JsonResponse(resp)
		else:
			for cab in cabs:
			# days = request.POST['Days']
				D_name.append(cab.DriverName)
				D_phone.append('9982312111')
				Price.append(cab.price)
				# price_pcab = p_cab.price
				type_cab.append(cab.Type) 
				cab_id.append(cab.cab_id) # not for display to users only for returning in the post request to backend
				
				From.append(b_cab.From)
				To.append(b_cab.To)
				Date.append(b_cab.Date)
				Date_return.append(b_cab.Date_return)
				# Time.append(b_cab.Time)
				OneWay.append(b_cab.OneWay)
				Sharing.append(b_cab.Sharing)
			cab_response = []
			for x in range(0, len(D_name)):
				cab_response.append({'Driver_name': D_name[x],'Driver_phone':D_phone[x], 'Price': Price[x], 'Cab_type': type_cab[x], 'cab_id': cab_id[x]})
				x+=1
				# cab_response_dict['Driver_name': name]
				# cab_response_dict['Price': name]
				# cab_response_dict['Cab_type': name]
				# cab_response_dict['cab_id': name]
				# cab_response_dict['cust_names': name]
			# resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id, 'cust_names': cust_names ,'From': From, 'To': To, 'Date': Date, 'Date_return': Date_return, 'OneWay': OneWay, 'Sharing': Sharing}
			resp = {'cabs':cab_response, 'From': b_cab.From, 'To': b_cab.To, 'Date': b_cab.Date, 'Date_return': b_cab.Date_return, 'OneWay': b_cab.OneWay, 'Sharing': b_cab.Sharing}
			# resp = {'Driver_name': D_name, 'Price': Price, 'Cab_type': type_cab, 'cab_id': cab_id,'From': From, 'To': To, 'Date': Date, 'Date_return': Date_return, 'OneWay': OneWay, 'Sharing': Sharing}
			print 4
			return render(request, 'cab/search.html', resp) #JsonResponse(resp)

@login_required
@csrf_exempt
def booknow(request, user):
	if request.POST:
		user_p = UserProfile.objects.get(user = request.user)
		#if book now in request.POST, partho will return id of the cab booked to the backend
		cab_id = request.POST['cab_id']
		# pcab_id = request.POST['pcab_id']

		if not cab_id.startswith('p'): #(pcab_id == null):
		#try:	
			cab_b = Cab.objects.get(pk = cab_id)

			sms_body_cust = '''Hi %s,
		Your Cab will be confirmed with in 15 mins from %s to %s by CabMe.
		Driver/Owner name: Reddy Kumar Simha
		Driver/Owner number: 8890605392
		Cab Type: %s
		''' % (user_p.name, From, To, cab_b.Type)
			requests.get('http://bhashsms.com/api/sendmsg.php?user=8890605392&pass=narasimha132&sender=CabMee&phone=%s&text=%s&priority=dnd&stype=normal') % (user_p.phone, sms_body_cust)
			
			sms_body_simha = '''%s has requested a cab from %s to %s.
		Customer name: %s
		Customer number: %s
		Cab Type: %s
		''' % (user_p.name, From, To, user_p.name, user_p.phone, cab_b.Type)
			requests.get('http://bhashsms.com/api/sendmsg.php?user=8890605392&pass=narasimha132&sender=CabMee&phone=8890605392&text=%s&priority=dnd&stype=normal') % (sms_body_simha)
			b_cab = BookCab()
			b_cab.From = request.POST['From']
			b_cab.To = request.POST['To']
			b_cab.Date = request.POST['Date']
			b_cab.Date_return = request.POST['Date_return']
			# b_cab.Time = request.POST['Time']
			b_cab.OneWay = request.POST['OneWay']
			b_cab.Sharing = request.POST['Sharing']

			b_cab.save()

		else:
			cab_b = PostCab.objects.get(pk = cab_id)
			user_driver = cab_b.user
			userpro_driver = UserProfile.objects.get(user = user_driver)
			sms_body_cust = '''Hi %s,
		Your Cab will be confirmed by %s with in 15 mins from %s to %s.
		Driver/Owner name: %s
		Driver/Owner number: %s
		Cab Type: %s
		''' % (user_p.name,userpro_driver.name, From, To, userpro_driver.name, userpro_driver.phone, cab_b.Type)
			requests.get('http://bhashsms.com/api/sendmsg.php?user=8890605392&pass=narasimha132&sender=CabMee&phone=%s&text=%s&priority=dnd&stype=normal') % (user_p.phone, sms_body_cust)
			
			confirm_url = 'cabme.in'
			sms_body_driver = '''Hi %s,
			%s has requested to pool in your car from %s to %s.
			Kindly confirm his request by following the url %s, or logging in cabme portal.
			User Contact Number: %s
			''' % (userpro_driver.name, user_p.name, From, To, confirm_url ,user_p.phone)
			requests.get('http://bhashsms.com/api/sendmsg.php?user=8890605392&pass=narasimha132&sender=CabMee&phone=%s&text=%s&priority=dnd&stype=normal') % (userpro_driver.phone, sms_body_driver)

		user_p.bookedcabs.add(cab_b) 
		#request.session['feedback'] = cab_b
		key = request.user.id
		# b_cab = BookCab()
		# b_cab.From = request.POST['From']
		# b_cab.To = request.POST['To']
		# b_cab.Date = request.POST['Date']
		# b_cab.Date_return = request.POST['Date_return']
		# b_cab.Time = request.POST['Time']
		# b_cab.OneWay = request.POST['OneWay']
		# b_cab.Sharing = request.POST['Sharing']
		cache.set(key,
			{'booked': True})
		# sms_body = '''Hi %s,
		# Your Cab will be confirmed with in 15 mins from %s to %s by CabMe.
		# Driver/Owner name: Reddy Kumar Simha
		# Driver/Owner number: 8890605392
		# Cab Type: %s
		# ''' % (user_p.name, From, To, cab_b.Type)
		# requests.get('http://bhashsms.com/api/sendmsg.php?user=8890605392&pass=narasimha132&sender=CabMee&phone=%s&text=%s&priority=dnd&stype=normal') % (user_p.phone, sms_body)
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



