from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse

from .models import *

def Init_Reg(request):
	if request.POST:

		name = request.POST['Name']
		# last_name = request.POST['Lname']
		email = request.POST['Email']
		contact = int(request.POST['Contact'])
		password = request.POST['Password']
		password_confirm = request.POST['Password_confirm']
		if (password == password_confirm):

			registered_members = UserProfile.objects.all()			
			list_of_registered_emails = [x.email for x in registered_members]
			if email in list_of_registered_emails:
				status = { "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }
				return JsonResponse(status)	
				# return HttpResponseRedirect('../../../register')

			elif len(str(contact)) < 10: 
				resp = {"status": 0, "message": 'Please enter a valid conatct number'}	
				return JsonResponse(resp)					
			# user_c = User()
			
			else:
				member = UserProfile()
				member.email = email
				member.contact = contact
				member.name = name

				if len(str(contact)) < 10: 
					pass
				# member.save()				
				user = User.objects.create_user(
					username=email,
					password=password)				
				# user_c.save()	
				member.user = user
				member.save()

				status = { "registered" : True , "id" : user.id }

				return JsonResponse(status)
				# return HttpResponseRedirect('../../../login')

		else:
			status = { "status": 0 , "message": "Passwords do not match"}

			return JsonResponse(status)
			# return HttpResponseRedirect('../../../register')

def user_login(request):



	if request.method == 'POST':
		# m sending email...
		# email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if cache.get(request.user.id) is not None:
				login(request, user)
				return HttpResponseRedirect('../feedback/')	
			else:
				login(request, user)
				return HttpResponseRedirect('../dashboard/')
		else:
			context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Invalid Login Credentials. Please try again'}
			return render(request, 'main/login.html', context)
	else:
		return render(request, 'main/login.html')		

def user_logout(request):
	logout(request)
	return redirect('registration:login')			