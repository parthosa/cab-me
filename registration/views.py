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
					cust_cache = cache.set(key,
						{'name': name,
						 'email_id': email,
						 'phone': contact,
						 'otp_id': otp_id
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard'})
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
					cust_cache = cache.set(key,
						{'name': name,
						 'email_id': email,
						 'phone': contact,
						 'otp_id': otp_id
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard'})

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')
	else:
		return render(request, 'cab/register.html')		



# @cache_page(60*10)
def verify_otp(request):
	cust_cache = cache.get(request.session['contact'])
	while cust_cache == None:
		cust_cache = cache.get(request.session['contact'])
	# print cust_cache
	print request.session['contact']
	otp = request.POST['otp']
	# print cust_cache['otp_id']
	cust_cache = cache.get(request.session['contact'])
	verify_otp_api = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/VERIFY/%s/%s'''%(cust_cache['otp_id'], otp)
	verify_otp = requests.get(verify_otp_api)
	if json.loads(verify_otp.text)['Status'] == 'Success':
		if not 'fbid' in cust_cache:
			user = User.objects.get(username = cust_cache['email_id'])
			user.is_active = True
			user.save()

			member = UserProfile()

			member.name = cust_cache['name']
			member.email_id = cust_cache['email_id']
			member.phone = cust_cache['phone']
			member.user = user
			member.save()

			cache.delete(request.session['contact'])

			resp = {'status': 1 , 'message': 'You have successfully verified your phone number. You can login now'}

		else:
			user = User.objects.get(username = cust_cache['fbid'])
			user.is_active = True
			user.save()

			member = UserProfile()
			# while cust_cache == None:
			# 	cust_cache = cache.get(request.session['contact'])
			member.name = cust_cache['name']
			member.email_id = cust_cache['email_id']
			member.phone = cust_cache['phone']
			member.fbid = cust_cache['fbid']
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
			prev_cache = cache.get(request.session['fbid'])
			while prev_cache == None:
				prev_cache = cache.get(request.session['fbid'])
			print prev_cache
			request.session['contact'] = contact
			name = prev_cache['name']
			fbid = prev_cache['fbid']

			key = request.session['contact']
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
		email = request.POST['Email']
		try:
			user_p = User.objects.get(fbid=fbid)
			if user_p.refer_stage < 1:
				user_p.refer_stage = '1'
				user_p.app_downloaded = True
				user_p.save()
			else:
				pass
			user_l = authenticate(username = fbid, password = fbid)
		except ObjectDoesNotExist:
			request.session['fbid'] = fbid
			# user_p = UserProfile.objects.create(fbid = fbid, name = name, email_id = email)
			user.create(
				username = fbid,
				password = fbid
				)
			user.is_active = False
			user.save()
			key = request.session['fbid']
			cache.set(key,
				{'name': name,
				 'fbid': fbid,
				 'email': email
				})

		return JsonResponse({'status': 1, 'message': 'You will be redirected to confirm your contact number'})	