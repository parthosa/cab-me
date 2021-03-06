from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from .models import *
from cab.models import *
import requests
import json
# from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
# import redis


def register_app(request):
	return render(request, 'registration/register.html')

def login_app(request):
	return render(request, 'registration/login.html')



def register_success(request):
	return render(request, 'registration/register_success.html')		

def login_success(request):
	return render(request, 'registration/login_success.html')		


# @cache_page(60*10)
def Init_Reg(request):
	if request.POST:

		name = request.POST['Name']
		# last_name = request.POST['Lname']
		email = request.POST['Email']
		contact = int(request.POST['Contact'])
		password = request.POST['Password']
		password_confirm = request.POST['Password_confirm']
		try:
			cache.clear()
		except:
			pass
		if (password == password_confirm):

			registered_members = User.objects.all()	
			list_of_registered_emails = [x.username for x in registered_members]
			registered_contacts = UserProfile.objects.all()
			list_of_registered_contacts = [x.phone for x in registered_contacts]
			try:
				tmp_user = User.objects.get(username = email)
				if tmp_user.is_active:
					print 'active user'
					status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }
					return JsonResponse(status)	
				else:
					print 'not active'
					status = { "registered" : True , "id" : tmp_user.id }
					send_otp_url = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/%s/AUTOGEN'''%(contact)
					send_otp = requests.get(send_otp_url)
					otp_id = send_otp.text.split(',')[1][11:-2]	
					request.session['contact'] = contact
					print request.session['contact']
					key = request.session['contact']
					request.session['name'] = name
					request.session['email'] = email
					request.session['phone'] = contact
					request.session['otp_id'] = otp_id
					cust_cache = cache.set(key,
						{'name': name,
						 'email_id': email,
						 'phone': contact,
						 'otp_id': otp_id
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard', 'otp_id': otp_id})
				# return HttpResponseRedirect('../../../register')

			except ObjectDoesNotExist:
				print 'no user'
				if len(str(contact)) != 10: 
					resp = {"status": 0, "message": 'Please enter a valid contact number'}	
					return JsonResponse(resp)					
				# user_c = User()
				elif contact in list_of_registered_contacts:
					status = { "status" : 0 , "message" : "This phone number is already registered! Please Refresh the page to register with another contact number . " }
					print 2
					return JsonResponse(status)

				
				else:
					user = User.objects.create_user(
						username=email,
						password=password)
					user.is_active = False		
					user.save()		
					# user_c.save()	

					status = { "registered" : True , "id" : user.id }
					send_otp_url = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/%s/AUTOGEN'''%(contact)
					send_otp = requests.get(send_otp_url)
					otp_id = send_otp.text.split(',')[1][11:-2]	
					print otp_id
					request.session['contact'] = contact
					print request.session['contact']
					key = request.session['contact']
					request.session['name'] = name
					request.session['email'] = email
					request.session['phone'] = contact
					request.session['otp_id'] = otp_id
					cust_cache = cache.set(key,
						{'name': name,
						 'email_id': email,
						 'phone': contact,
						 'otp_id': otp_id
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard', 'otp_id': otp_id})

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')
	else:
		return render(request, 'cab/register.html')		



# @cache_page(60*10)
def verify_otp(request):
	# print cust_cache
	print request.session['contact']
	otp = request.POST['otp']
	# cust_cache = cache.get(request.session['contact'])
	# while cust_cache == None:
	# 	cust_cache = cache.get(request.session['contact'])

	# print cust_cache['otp_id']
	verify_otp_api = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/VERIFY/%s/%s'''%(request.session['otp_id'], otp)
	verify_otp = requests.get(verify_otp_api)
	if json.loads(verify_otp.text)['Status'] == 'Success':
		if not 'fbid' in request.session:
			user = User.objects.get(username = request.session['email'])
			user.is_active = True
			user.save()

			member = UserProfile()

			member.name = request.session['name']
			member.email_id = request.session['email']
			member.phone = request.session['phone']
			member.user = user
			member.save()

			cache.delete(request.session['contact'])

			resp = {'status': 1 , 'message': 'You have successfully verified your phone number. You can login now'}

		else:
			user = User.objects.get(username = request.session['fbid'])
			user.is_active = True
			user.save()

			member = UserProfile()
			# while cust_cache == None:
			# 	cust_cache = cache.get(request.session['contact'])
			member.name = request.session['name']
			member.email_id = request.session['email']
			member.phone = request.session['phone']
			member.fbid = request.session['fbid']
			member.user = user
			member.save()

			cache.delete(request.session['contact'])

			resp = {'status': 1 , 'message': 'You have successfully verified your phone number. You can login now'}

	else:
		resp = {'status': 0, 'message': 'The OTP you entered is incorrect. Kindly check it again'}

	return JsonResponse(resp)

def user_login(request):

	if request.method == 'POST':
		# m sending email...
		# email = request.POST['email']
		username = request.POST['email']
		password = request.POST['password']
		print username
		print password
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				print 2
				if cache.get(request.user.id) is not None:
					login(request, user)
					return HttpResponseRedirect('../../feedback/')	
				else:
					login(request, user)
					return JsonResponse({'status': 1, 'message': 'Successfully logged in','name': UserProfile.objects.get(user=user).name})
			else:
				return JsonResponse({'status': 0, 'message': 'Kindly complete your registration first by verifying your contact number'})
		else:
			context = {'status': 0,'error_heading' : "Invalid Login Credentials", 'message' :  'Invalid Login Credentials. Please try again'}
			return JsonResponse(context) #render(request, 'main/login.html', context)
	else:
		print 1
		return render(request, 'cab/login.html')		

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('../../')

# @cache_page(60*10)
def social_login_fb(request):
	if request.POST:
		fbid = request.POST['fbid']
		name = request.POST['Name']
		# email = request.POST['Email']
		try:
			user_p = User.objects.get(username=fbid)
			if user_p.is_active:
				user = authenticate(username = fbid, password = fbid)
				login(request, user)
				return JsonResponse({'status': 1, 'message': 'Succesfully logged in'})
			
			else:
				request.session['fbid'] = fbid
				key = request.session['fbid']
				request.session['name'] = name
				request.session['fbid'] = fbid
				prev_cache = cache.set(key,
					{'name': name,
					 'fbid': fbid,
					})
				print prev_cache

				return JsonResponse({'status': 2, 'message': 'You will be redirected to confirm your contact number'})
		
		except ObjectDoesNotExist:
			request.session['fbid'] = fbid
			# user_p = UserProfile.objects.create(fbid = fbid, name = name, email_id = email)
			user = User.objects.create_user(
				username = fbid,
				password = fbid)
			user.is_active = False
			user.save()
			key = request.session['fbid']
			request.session['name'] = name
			request.session['fbid'] = fbid
			prev_cache = cache.set(key,
				{'name': name,
				 'fbid': fbid,
				})

			return JsonResponse({'status': 2, 'message': 'You will be redirected to confirm your contact number'})

# @cache_page(60*10)
def social_contact(request):
	if request.POST:
		contact = request.POST['phone']
		email = request.POST['Email']
		registered_members = User.objects.all()	
		list_of_registered_emails = [x.username for x in registered_members] + [x.email_id for x in UserProfile.objects.all()]
		registered_contacts = UserProfile.objects.all()
		list_of_registered_contacts = [x.phone for x in registered_contacts]
		print 'done yahan tak'

		if len(str(contact)) != 10: 
			resp = {"status": 0, "message": 'Please enter a valid contact number'}	
			return JsonResponse(resp)					
		# user_c = User()
		elif contact in list_of_registered_contacts:
			print 'contact exists'
			status = { "status" : 0 , "message" : "This phone number is already registered! Please Refresh the page to register with another contact number . " }
			return JsonResponse(status)
		elif email in list_of_registered_emails:
			status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another email . " }
			return JsonResponse(status)
		else:
			send_otp_url = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/%s/AUTOGEN'''%(contact)
			send_otp = requests.get(send_otp_url)
			otp_id = send_otp.text.split(',')[1][11:-2]
			# prev_cache = cache.get(request.session['fbid'])
			# while prev_cache == None:
			# 	prev_cache = cache.get(request.session['fbid'])
			# print prev_cache
			request.session['contact'] = contact
			name = request.session['name']
			fbid = request.session['fbid']

			key = request.session['contact']
			request.session['name']	 = name
			request.session['email'] = email
			request.session['phone'] = contact
			request.session['otp_id'] = otp_id
			request.session['fbid'] = fbid
			cust_cache = cache.set(key,
				{'name': name,
				 'email_id': email,
				 'phone': contact,
				 'otp_id': otp_id,
				 'fbid': fbid
				})
			# print cache.get(request.session['contact'])

			# return JsonResponse(status)
			return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/verify_otp'})

def user_login_app(request):

	if request.method == 'POST':
		# m sending email...
		# email = request.POST['email']
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		user_p = UserProfile.objects.get(user = user)
		if user:
			if user.is_active:
				if int(user_p.refer_stage) > 0:
					print 1
					if cache.get(request.user.id) is not None:
						login(request, user)
						return HttpResponseRedirect('../../feedback/')	
					else:
						login(request, user)
						return JsonResponse({'status': 1, 'message': 'Successfully logged in'})

				else:
					print user_p.refer_stage
					user_p.refer_stage = '1'
					user_p.app_downloaded = True
					user_p.save()
					print user_p.refer_stage
					if cache.get(request.user.id) is not None:
						login(request, user)
						return HttpResponseRedirect('../../feedback/')	
					else:
						login(request, user)
						return JsonResponse({'status': 1, 'message': 'Successfully logged in'})
			else:
				return JsonResponse({'status': 0, 'message': 'Kindly complete your registration first by verifying your contact number'})

		else:
			context = {'status': 0,'error_heading' : "Invalid Login Credentials", 'message' :  'Invalid Login Credentials. Please try again'}
			return JsonResponse(context) #render(request, 'main/login.html', context)
	else:
		return render(request, 'main/login.html')	

# @cache_page(60*10)
def social_login_fb_app(request):
	if request.POST:
		cache.clear()
		fbid = request.POST['fbid']
		name = request.POST['Name']
		
		try:
			user_p = user_p.objects.get(fbid=fbid)
			if int(user_p.refer_stage) == 0:
				user_p.refer_stage = '1'
				user_p.app_downloaded = True
				user_p.save()
			else:
				pass
			user_l = authenticate(username = fbid, password = fbid)
			login(request, user_l)

			return JsonResponse({'status': 1, 'message': 'Successfully logged in'})
		except ObjectDoesNotExist:
			email = request.POST['Email']
			request.session['fbid'] = fbid
			# user_p = UserProfile.objects.create(fbid = fbid, name = name, email_id = email)
			user.create(
				username = fbid,
				password = fbid
				)
			user.is_active = False
			user.save()
			key = request.session['fbid']
			request.session['name'] = name
			request.session['fbid'] = fbid
			request.session['email'] = email
			cache.set(key,
				{'name': name,
				 'fbid': fbid,
				 'email': email
				})

			return JsonResponse({'status': 2, 'message': 'You will be redirected to confirm your contact number'})	

def test_cache_set(request):
	request.session['contact'] = 569841
	key = request.session['contact']
	name = 'af'
	email = 'hthr'
	contact = 7689768
	otp_id = 'dhdtrh'
	fbid = 780797
	cust_cache = cache.set(key,
		{'name': name,
		 'email_id': email,
		 'phone': contact,
		 'otp_id': otp_id,
		 'fbid': fbid
		})
	print cache.get(request.session['contact'])
	return JsonResponse({'status':'done'})