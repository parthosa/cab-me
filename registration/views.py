from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate, login ,logout
from .models import *
from cab.models import *

def Init_Reg(request):
	if request.POST:

		name = request.POST['Name']
		# last_name = request.POST['Lname']
		email = request.POST['Email']
		contact = int(request.POST['Contact'])
		password = request.POST['Password']
		password_confirm = request.POST['Password_confirm']
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

			elif len(str(contact)) < 10: 
				resp = {"status": 0, "message": 'Please enter a valid contact number'}	
				return JsonResponse(resp)					
			# user_c = User()
			elif contact in list_of_registered_contacts:
				status = { "status" : 0 , "message" : "This phone number is already registered! Please Refresh the page to register with another contact number . " }
				print 2
				return JsonResponse(status)
			
			else:
				print 3
				member = UserProfile()
				member.email_id = email
				member.phone = contact
				member.name = name

				if len(str(contact)) < 10: 
					pass
				# member.save()				
				user = User.objects.create_user(
					username=email,
					password=password)				
				# user_c.save()	
				print 4
				member.user = user
				print 5
				member.save()
				print 6

				status = { "registered" : True , "id" : user.id }

				# return JsonResponse(status)
				return HttpResponseRedirect('../../main')

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')

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
			return JsonResponse({'status': 0, 'message': 'Invalid Login Credentials. Please try again'})
	else:
		print 1
		return render(request, 'main/login.html')		

@csrf_exempt
def user_logout(request):
	logout(request)
	return JsonResponse({'status': 1, 'message': 'Successfully logged out'})

def social_profile_build(request):
	s_user = SocialAccount.objects.get(user=request.user)
	context = {}
	try:
		email = s_user.extra_data['email']
	except:
		context['email'] = True
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
			return render(request, 'main/social_account.html', context)
		
		p_user = UserProfile()
		p_user.phone = request.POST['phone']
		try:
			p_user.email_id = s_user.extra_data['email']
		except:
			p_user.email_id = request.POST['email']
		p_user.email_verified = True
		p_user.user = request.user
		p_user.name = s_user.extra_data['first_name'] + ' ' + s_user.extra_data['last_name']
		p_user.user.save()
		p_user.save()
		return HttpResponseRedirect('../dashboard/')
	return render(request, 'main/social_account.html', context)		