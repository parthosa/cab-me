from django.shortcuts import render
from registration.models import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
import requests
import json


# def login(request):
# 	return render(request,'cab/login.html')

@csrf_exempt
@login_required(login_url='/accounts/login/')
def create_invite_code(request):
	user_p = UserProfile.objects.get(user = request.user)
	if user_p.refer_stage == '0':
		resp = {'status': 1, 'message': 'Kindly download and login through the android application to get your invite code.','refer_stage':user_p.refer_stage,'wallet':user_p.cabme_cash}
		return render(request, 'cab/earn_money.html',resp)
	else:
		invite_code = str(user_p.name[0]) + str(user_p.id) + str(user_p.phone)
		user_p.invite_id = invite_code
		user_p.save()
		invite_url = '''http://cabme.in/refferal/invite/%s''' % (invite_code)

		response = {'status': 1, 'message': 'Your invite url is '+ invite_url,'refer_stage':user_p.refer_stage,'wallet':user_p.cabme_cash}
		return render(request, 'cab/earn_money.html',response)


# @cache_page(60*10)
@csrf_exempt
def refer_registration(request, invite_code):
	#test
	user_i = UserProfile.objects.get(invite_id = invite_code)
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
						 'otp_id': otp_id,
						 'invite_code': invite_code
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard'})
				# return HttpResponseRedirect('../../../register')
			except ObjectDoesNotExist:
				if len(str(contact)) != 10: 
					resp = {"status": 0, "message": 'Please enter a valid contact number'}	
					
					return JsonResponse(resp)					
				# user_c = User()
				elif contact in list_of_registered_contacts:
					status = { "status" : 0 , "message" : "This phone number is already registered! Please Refresh the page to register with another contact number . " }

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
					request.session['contact'] = contact
					key = request.session['contact']
					cust_cache = cache.set(key,
						{'name': name,
						 'email_id': email,
						 'phone': contact,
						 'otp_id': otp_id,
						 'invite_code': invite_code
						})

					# return JsonResponse(status)
					return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/dashboard'})

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
	else:
		return render(request, 'cab/register.html')
			# return HttpResponseRedirect('../../../register')


# @cache_page(60*10)
@csrf_exempt
def verify_otp(request):


	cust_cache = cache.get(request.session['contact'])
	while cust_cache == None:
		cust_cache = cache.get(request.session['contact'])
	print cust_cache
	user_i = UserProfile.objects.get(invite_id = cust_cache['invite_code'])
	otp = request.POST['otp']
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
			print user_i.user
			member.invited_by = user_i.user
			member.user = user
			member.save()
			print member.invited_by.username

			user_i.invites.add(user)
			user_i.save()
			print user_i.invites.all()

			cache.delete(request.session['contact'])

			resp = {'status': 1 , 'message': 'You have successfully verified your phone number. You can login now'}
		else:
			user = User.objects.get(username = cust_cache['fbid'])
			user.is_active = True
			user.save()

			member = UserProfile()
			member.email_id = cust_cache['email_id']
			member.phone = cust_cache['phone']
			member.fbid = cust_cache['fbid']
			member.invited_by = user_i.user
			member.user = user
			member.save()

			user_i.invites.add(user)
			user_i.save()

			cache.delete(request.session['contact'])

			resp = {'status': 1 , 'message': 'You have successfully verified your phone number. You can login now'}

	else:
		resp = {'status': 0, 'message': 'The OTP you entered is incorrect. Kindly check it again'}

	return JsonResponse(resp)

@login_required(login_url='/accounts/login/')
@csrf_exempt
def wallet(request):
	user_p = UserProfile.objects.get(user = request.user)
	cash = user_p.cabme_cash
	response = {}
	if user_p.refer_stage == '0':
		response = {'cabme_cash': cash, 'message': 'Kindly download our application and login with it to get Rs 200 in you cabme wallet.'}

	elif user_p.refer_stage == '1':
		# user_p.refer_stage == '1'
		# user_p.save()
		invites_left = 5-user_p.invites.all().count()
		response = {'cabme_cash': cash, 'message': 'Kindly invite '+ str(invites_left)+ ' more people to earn Rs 200 more.'}

	elif user_p.invites == '2':
		# user_p.refer_stage == '2'
		# user_p.save()
		invites_left = 25-user_p.invites.all().count()
		response = {'cabme_cash': cash, 'message': 'Kindly invite '+ str(invites_left)+ ' more people to earn Rs 200 more.'}

	elif user_p.invites == '3':
		# user_p.refer_stage == '3'
		# user_p.save()
		invites_left = 65-user_p.invites.all().count()
		response = {'cabme_cash': cash, 'message': 'Kindly invite '+ str(invites_left)+ ' more people to earn Rs 200 more.'}
	
	elif user_p.invites == '4':
		# user_p.refer_stage == '4'
		# user_p.save()
		invites_left = 125-user_p.invites.all().count()
		response = {'cabme_cash': cash, 'message': 'Kindly invite '+ str(invites_left)+ ' more people to earn Rs 200 more.'}
	
	else:
		pass
	print user_p.invites
	return JsonResponse(response)

# @cache_page(60*10)
def social_login_fb(request):
	if request.POST:
		cache.clear()
		fbid = request.POST['fbid']
		invite_code = request.POST['invite_code']
		name = request.POST['Name']
		email = request.POST['Email']
		try:
			user_p = User.objects.get(username=fbid)
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

# @cache_page(60*10)
def social_contact(request):
	contact = request.POST['phone']
	send_otp_url = '''http://2factor.in/API/V1/b5dfcd4a-cf26-11e6-afa5-00163ef91450/SMS/%s/AUTOGEN'''%(contact)
	send_otp = requests.get(send_otp_url)
	otp_id = send_otp.text.split(',')[1][11:-2]
	request.session['contact'] = contact
	prev_cache = cache.get(request.session['fbid'])
	while prev_cache == None:
		prev_cache = cache.get(request.session['fbid'])

	name = prev_cache['name']
	email = prev_cache['email']
	fbid = prev_cache['fbid']
	invite_code = prev_cache['invite_code']
	cache.clear()

	key = request.session['contact']
	cust_cache = cache.set(key,
		{'name': name,
		 'email_id': email,
		 'phone': contact,
		 'otp_id': otp_id,
		 'fbid': fbid,
		 'invite_code': invite_code
		})

	# return JsonResponse(status)
	return JsonResponse({'status': 1, 'message': 'You have Successfully registered, you will be now redirected to verify your otp.', 'location_redirection': '/verify_otp'})

