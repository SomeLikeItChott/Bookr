from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/bookr/")

def index(request):
	print('you are ' + str(request.user))
	return render(request, 'bookr/index.html')

def login_view(request):
	print('loading login')
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect("/bookr/")
					# Redirect to a success page.
				else:
					print('jafdskls')
					# Return a 'disabled account' error message
			else:
				print('jfkasdljfadslkfdsajlkdfsa')
			return HttpResponseRedirect("/bookr/")
	else:
		form = AuthenticationForm()
 
	return render(request, "bookr/login.html",  {'form': form,  })

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/bookr/")
	else:
		form = UserCreationForm()
 
	return render(request, "bookr/register.html",  {'form': form,  })