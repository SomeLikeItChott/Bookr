from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Contact, Book
from .forms import *

def sell(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	user = request.user
	if request.method == 'POST':
		sell_form = SellForm(request.POST)
		contact_form = AddContactForm(request.POST)
		if contact_form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			newcontact = Contact()
			newcontact.user = user
			newcontact.contact_text = request.POST['contact_text']	
			newcontact.contact_type = request.POST['contact_type']
			newcontact.save()
		if sell_form.is_valid():
			newbook = Book()
			newbook.seller = user
			newbook.price = request.POST['price']
			newbook.condition = request.POST['condition']
			newbook.ISBN = request.POST['ISBN']
			newbook.save()
	# if a GET (or any other method) we'll create a blank form
	else:
		contact_form = AddContactForm()
		sell_form = SellForm()
 
	return render(request, 'bookr/sell.html', {'user': user, 'contact_form': contact_form, 'sell_form': sell_form })

def private_account(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	user = request.user
	if request.method == 'POST':
		contact_form = AddContactForm(request.POST)
		if contact_form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			newcontact = Contact()
			newcontact.user = user
			newcontact.contact_text = request.POST['contact_text']	
			newcontact.contact_type = request.POST['contact_type']
			newcontact.save()
	# if a GET (or any other method) we'll create a blank form
	else:
		contact_form = AddContactForm()
 
	return render(request, 'bookr/account.html', {'user': user, 'contact_form': contact_form })



def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def index(request):
	print('you are ' + str(request.user))
	return render(request, 'bookr/index.html')

def login_view(request):
	print(request.POST)
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