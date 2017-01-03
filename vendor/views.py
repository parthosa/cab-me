from django.shortcuts import render
from .models import *
from Fund.models import *
from UserM.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import moment
from datetime import datetime
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json, ast
from django.contrib.admin.views.decorators import staff_member_required

@csrf_exempt
def Init_Reg(request):
	if request.POST:

		name = request.POST['Name']
		email = request.POST['Email']
		contact = int(request.POST['Contact'])
		password = request.POST['Password']
		password_confirm = request.POST['Password_confirm']
		if (password == password_confirm):

			registered_members = UserProfile.objects.all()			
			list_of_registered_emails = [x.email for x in registered_members]
			if email in list_of_registered_emails:
				# status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }
				# return JsonResponse(status)	
				return HttpResponseRedirect('../../../register')
			elif len(str(contact)) < 10: 
				resp = {"status": 0, "message": 'Please enter a valid conatct number'}						
			# user_c = User()
			else:
				if member_type = 'Vendor':
					member = Vendor()
					member.email = email
					member.contact = contact
					member.name = name
				
					user = User.objects.create_user(
						username=email,
						password=password)				
					# user_c.save()	
					member.user = user
					member.save()

					# status = { "registered" : True , "id" : user.id }

					# return JsonResponse(status)
					return HttpResponseRedirect('../../../login')

				else:
					member = Driver()
					member.email = email
					member.contact = contact
					member.name = name

					user = User.objects.create_user(
						username=email,
						password=password
						)
					member.user = user
					member.save()

					return HttpResponseRedirect('../../../login')

		else:
			# status = { "status": 0 , "message": "Passwords do not match"}

			# return JsonResponse(status)
			return HttpResponseRedirect('../../../register')

@csrf_exempt
def user_login(request):

	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				# if user.is_staff:
				# 	login(request, user)
				# 	return HttpResponseRedirect('../dashboard')	
				# else:
				login(request, user)
				resp = {'successful': True, 'auth': 'User successfully logged in(success)'}
				return JsonResponse(resp)  #HttpResponseRedirect('../dashboard/')
				#return HttpResponseRedirect('../../../user/')
			else:
				pass
				# # context = {'error_heading' : "Account Inactive", 'error_message' :  'Your account is currently INACTIVE.'}
				# # return JsonResponse(resp)
				# return HttpResponseRedirect('../../../login/')
		else:
			context = {'successful': True, 'auth': 'User successfully logged in(failiure)'}
			return JsonResponse(context)
			# return HttpResponseRedirect('../../../login')
	else:
		print 'something'
		return HttpResponseRedirect('../users/authenticate')		

@csrf_exempt
def user_logout(request):
	logout(request)
	return redirect('registration:login')	
