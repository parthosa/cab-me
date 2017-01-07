from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate, login ,logout
from .models import *
from cab.models import *
import requests
import json
from django.views.decorators.cache import cache_page

@cache_page(60*10)
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
			print 1		
			list_of_registered_emails = [x.username for x in registered_members]
			registered_contacts = UserProfile.objects.all()
			list_of_registered_contacts = [x.phone for x in registered_contacts]
			if email in list_of_registered_emails:
				status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }
				print 2
				return JsonResponse(status)	
				# return HttpResponseRedirect('../../../register')

			elif len(str(contact)) != 10: 
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
				print cust_cache

				# return JsonResponse(status)
				return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard'})

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')

@cache_page(60*10)
def verify_otp(request):
	cust_cache = cache.get(request.session['contact'])
	print cust_cache
	print request.session['contact']
	otp = request.POST['otp']
	print cust_cache['otp_id']
	verify_otp_api = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/VERIFY/%s/%s'''%(cust_cache['otp_id'], otp)
	verify_otp = requests.get(verify_otp_api)
	if json.loads(verify_otp.text)['Status'] == 'Success':
		print 1
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
			print 2
			if cache.get(request.user.id) is not None:
				login(request, user)
				return HttpResponseRedirect('../../feedback/')	
			else:
				login(request, user)
				return JsonResponse({'status': 1, 'message': 'Successfully logged in'})
		else:
			context = {'status': 0,'error_heading' : "Invalid Login Credentials", 'message' :  'Invalid Login Credentials. Please try again'}
			return JsonResponse(context) #render(request, 'main/login.html', context)
	else:
		print 1
		return render(request, 'main/login.html')		

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('../../')

def social_profile_build(request):
	s_user = SocialAccount.objects.get(user=request.user)
	request.user.is_active = False
	request.user.save()
	context = {}
	try:
		email = s_user.extra_data['email']
	except:
		email = None
# p_user = UserProfile.objects.get()
	if request.POST:
		userp_exists = False
		user_exist = False

		try:
			UserProfile.objects.get(email_id=request.POST['email'])
			userp_exists = True
		except:
			pass

		try:
			User.objects.get(email=request.POST['email'])
			user_exist = True
		except:
			pass
			
		if userp_exists or user_exist:
			context['error_message'] = 'This email is already registered.'
			context['status'] = 0
			return JsonResponse(context)
		
		p_user.phone = request.POST['phone']
		send_otp_url = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/%s/AUTOGEN'''%(contact)
		send_otp = requests.get(send_otp_url)
		otp_id = send_otp.text.split(',')[1][11:-2]	
		request.session['contact'] = p_user.phone
		key = request.session['contact']
		cache.set(key,
			{'name': name,
			 'phone': p_user.phone,
			 'otp_id': otp_id
			})
		try:
			p_user.email_id = s_user.extra_data['email']
		except:
			p_user.email_id = request.POST['email']

		return JsonResponse({'status' :1, 'message': 'An otp has been sent to your contact number to verify the same.'})
	return JsonResponse({'status': 1, 'message': 'An otp has been sent to your contact number to verify the same'})		