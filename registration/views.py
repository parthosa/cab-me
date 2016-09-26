from django.shortcuts import render
from .models import *

@csrf_exempt
def Init_Reg(request):
	if request.POST:

		name = request.POST['Name']
		email = request.POST['Email']
		phone = int(request.POST['Phone'])
		password = request.POST['Password']
		password_confirm = request.POST['Password_confirm']
		if (password = password_confirm):
			user_c = User()
			member = UserProfile()
			member.email_id = email
			member.phone = phone
			member.name = name
			registered_members = InitialRegistration.objects.all()
			user_c.username = email
			user.set_password = password
		user.save()
		member.save()	

			list_of_registered_emails = [x.email_id for x in registered_members]
			if ema in list_of_registered_emails: #check for already registered emails....no need to check if valid as we are using email field on fronted side
				status = '{ "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }'
				return JsonResponse(status)
			if len(str(pho)) < 10: #checking lenth of phone number
				pass
			member.save()

			status = '{ "status" : 1 , "message" : "Successfully Registered !" }'

			return JsonResponse(status)

		else:
			status = '{ "status": 0 , "message": "Passwords do not match"}'


def user_login(request):

	context = RequestContext(request)

	if request.method == 'POST':
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