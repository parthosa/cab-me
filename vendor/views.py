from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
# import moment
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
		member_type = request.POST['member_type']
		cab_type = request.POST['cab_type']
		date_of_birth = request.POST['date_of_birth']
		cab_number = request.POST['cab_number']
		if (password == password_confirm):

			registered_members = UserProfile.objects.all()			
			list_of_registered_emails = [x.email for x in registered_members]
			if email in list_of_registered_emails:
				status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }
				return JsonResponse(status)	
				# return HttpResponseRedirect('../../../register')
			elif len(str(contact)) < 10: 
				resp = {"status": 0, "message": 'Please enter a valid conatct number'}						
			# user_c = User()
			else:
				cab = Cab()
				cab.cab_type = cab_type
				cab.cab_number = cab_number
				if member_type == 'Vendor':
					member = Vendor()
					member.email = email
					member.contact = contact
					member.name = name
					member.date_of_birth = date_of_birth
				
					user = User.objects.create_user(
						username=contact,
						password=password)				
					# user_c.save()	
					member.user = user
					member.save()
					cab.driver = member
					cab.save()
					member.cabs.add(cab)
					member.save()

					status = { "registered" : True , "id" : user.id }

					return JsonResponse(status)
					# return HttpResponseRedirect('../../../login')

				else:
					member = Driver()
					member.email = email
					member.contact = contact
					member.name = name
					member.date_of_birth = date_of_birth

					user = User.objects.create_user(
						username=contact,
						password=password
						)
					member.user = user
					member.save()
					cab.driver = member
					cab.save()
					member.cabs.add(cab)
					member.save()

					return JsonResponse({'status':1, 'message':'Successfully registered'})

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')

@csrf_exempt
def user_login(request):

	if request.method == 'POST':
		username = request.POST['phone']
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

@csrf_exempt
@login_required
def add_cab(request):
	if request.POST:
		try:
			driver = Driver.objects.get(user = request.user)
		except ObjectDoesNotExist:
			driver = Vendor.objects.get(user = request.user)
		cab_type = request.POST['cab_type']
		cab_number = request.POST['cab_number']
		cab = Cab()
		cab.cab_type = cab_type
		cab.cab_number = cab_number
		cab.driver = driver
		cab.save()
		driver.cabs.add(cab)
		driver.save()

	return JsonResponse({'status': 1, 'message': 'The cab has been successfully added'})
