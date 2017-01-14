from django.shortcuts import render,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
# import moment
from datetime import datetime
from django.core.cache import cache
from django.contrib.auth import authenticate, login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json, ast
from django.contrib.admin.views.decorators import staff_member_required

@csrf_exempt
def Init_Reg(request):
	if request.POST:
		print request.POST
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

			registered_drivers = Driver.objects.all()	
			registered_vendors = Vendor.objects.all()	
			list_of_registered_emails = [x.email for x in registered_drivers] + [x.email for x in registered_vendors]
			list_of_registered_contacts = [x.contact for x in registered_drivers] + [x.contact for x in registered_vendors]
			if email in list_of_registered_emails:
				context = {'message':'This email is already registered '}
				return render(request, 'vendor/register.html',context)
			elif contact in list_of_registered_contacts:
				context = {'message':'This email is already registered '}
				return render(request, 'vendor/register.html',context)
				# return HttpResponseRedirect('../../../register')
			elif len(str(contact)) != 10: 
				print 2
				context = {'message':'Please enter a valid conatct number'}

				return render(request, 'vendor/register.html',context)
			# user_c = User()
			else:
				print 1
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
					cab.vendor = member
					cab.save()
					member.cabs.add(cab)
					member.save()

					status = { "registered" : True , "id" : user.id }

					return redirect('../register_success')

					# return JsonResponse(status)
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
					return redirect('../register_success')

					# return JsonResponse({'status':1, 'message':'Successfully registered'})

		else:
			context = {'message':'Passwords do not match'}

			return render(request, 'vendor/register.html',context)
			# return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')
	else:
		return render(request, 'vendor/register.html')


@csrf_exempt
def register_success(request):
	return render(request, 'vendor/register_success.html')

@csrf_exempt
def user_login(request):

	if request.method == 'POST':
		username = request.POST['phone']
		password = request.POST['password']
		print request.POST
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				# if user.is_staff:
				# 	login(request, user)
				# 	return HttpResponseRedirect('../dashboard')	
				# else:
				login(request, user)
				# resp = {'successful': True, 'auth': 'User successfully logged in(success)'}
				# return JsonResponse(resp)  HttpResponseRedirect('../dashboard/')
				#return HttpResponseRedirect('../../../user/')
				return redirect('../login_success')
			else:
				pass
				# # context = {'error_heading' : "Account Inactive", 'error_message' :  'Your account is currently INACTIVE.'}
				# # return JsonResponse(resp)
				# return HttpResponseRedirect('../../../login/')
		else:
			context = {'message':'Try Again'}
			# context = {'successful': True, 'auth': 'User successfully logged in(failiure)'}
			# return JsonResponse(context)
			return render(request, 'vendor/login.html',context)
			# return HttpResponseRedirect('../../../login')
	else:
		return render(request, 'vendor/login.html')
		# return HttpResponseRedirect('../users/authenticate')		

@csrf_exempt
def login_success(request):
	return render(request, 'vendor/login_success.html')

@csrf_exempt
def user_logout(request):
	logout(request)
	return render(request, 'vendor/login.html')

@csrf_exempt
@login_required(login_url='/vendor/login')
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
		if isinstance(driver, Driver) == True:
			cab.driver = driver
		else:
			cab.vendor = driver
		cab.save()
		driver.cabs.add(cab)
		driver.save()

	response = {'status': 1, 'message': 'The cab has been successfully added'}
	return render(request, 'vendor/view_cabs.html',response)


@csrf_exempt
@login_required(login_url='/vendor/login')
def view_cabs(request):
	try:
		driver = Driver.objects.get(user = request.user)
		cabs = Cab.objects.filter(driver = driver)
		print driver
	except ObjectDoesNotExist:
		driver = Vendor.objects.get(user = request.user)
		cabs = Cab.objects.filter(vendor = driver)

	print cabs
	cab_list = []

	for cab in cabs:
		cab_list.append({'cab_type': cab.cab_type, 'cab_number': cab.cab_number})

	response = {'cabs': cab_list, 'isVendor':isinstance(driver,Vendor)}
	
	return render(request, 'vendor/view_cabs.html',response)
