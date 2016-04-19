from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from .models import *
from .forms import *
from isbnlib import *
from django.db.models import Q
import re, os

def wishlist(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	if request.method == 'POST':
		bookid = request.POST['bookid']
		wish = Wish()
		wish.user = request.user
		wish.book = Book.objects.get(id=bookid)
		wish.save()
	wishes = Wish.objects.filter(user__id=request.user.id)
	return render(request, 'bookr/wishlist.html', {'wishes': wishes, 'user': request.user})

def books_for_sale(request, user_id):
	if int(request.user.id) == int(user_id):
		private = True
		user = request.user
	else:
		private = False
		user = User.objects.get(id=user_id)
	books = Book.objects.filter(seller__id=user_id)

	return render(request, 'bookr/books_for_sale.html', {'user': user, 'private': private, 'books': books})

def booktype(request, booktype_id):
	booktype = get_object_or_404(BookType, pk=booktype_id)
	print(booktype.title)
	books = Book.objects.filter(booktype__id=booktype.id)
	return render(request, 'bookr/booktype.html', {'booktype': booktype, 'books': books})

def search(request):
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['title', 'author', 'isbn'])

		#found_entries = Book.objects.filter(entry_query).order_by('-pub_date')
		found_entries = BookType.objects.filter(entry_query)
	pairs = dict()
	try:
		for entry in found_entries:
			pairs[entry]=len(Book.objects.filter(booktype__id=entry.id))
	except:
		pairs = None;
	return render(request, 'bookr/search.html', 
		{ 'query_string': query_string, 'pairs': pairs, },)

#from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:
		
		>>> normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']
	
	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
#from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.
	
	'''
	query = None # Query to search for every search term        
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query

def book(request, book_id):
	book = get_object_or_404(Book, pk=book_id)
	try:
		if int(book.seller.id) == int(request.user.id):
			user = request.user
			private = True
			if not request.user.is_authenticated():
				return HttpResponseRedirect(reverse('login'))
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
		else:
			user = book.seller
			private = False
			contact_form = AddContactForm()
	except:
		user = book.seller
		private = False
		contact_form = AddContactForm()
	return render(request, 'bookr/book.html', {'book': book, 'user': user, 'private': private, 'contact_form': contact_form,})

def sell(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	user = request.user
	if request.method == 'POST':
		sell_form = SellForm(request.POST, request.FILES)
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
		if sell_form.is_valid() and 'sellname' in request.POST:
			print('selling fffbook')
			newbook = Book()
			print('fjaksldkfsa')
			print(user)
			newbook.seller = user
			newbook.price = request.POST['price']
			newbook.condition = request.POST['condition']
			print('fadjsl')
			#handle_uploaded_file(request.FILES['image'])
			#newbook.picture = sell_form.cleaned_data['image']
			#print(newbook.picture)
			isbn = EAN13(clean(request.POST['isbn']))
			print('ayy')
			try:
				print('waaah')
				newbook.booktype = BookType.objects.get(isbn__iexact=isbn)
			except:
				print('kill me')
				newbt = BookType()
				print('wow')
				metadata = meta(request.POST['isbn'])
				print('help')
				try:
					newbt.title = metadata['Title']
					newbt.author = ', '.join(metadata['Authors'])
				except:
					newbt.title = 'No title found' + isbn
					newbt.author = 'No authors found' + isbn
				newbt.isbn = isbn
				newbt.save()
				newbook.booktype = newbt
			newbook.save()
			print('time to go')
			print(newbook.id)
			return HttpResponseRedirect(reverse('book', args=(newbook.id,)))
	# if a GET (or any other method) we'll create a blank form
	else:
		contact_form = AddContactForm()
		sell_form = SellForm()
 
	return render(request, 'bookr/sell.html', {'user': user, 'contact_form': contact_form, 'sell_form': sell_form })

def handle_uploaded_file(f):
	with open("bookr/images/test.jpg", 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def account(request, user_id):
	if int(user_id) == int(request.user.id):
		user = request.user
		private = True
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
		if request.method == 'POST':
			contact_form = AddContactForm(request.POST)
			rating_form = RatingForm(request.POST)
			if contact_form.is_valid():
				newcontact = Contact()
				newcontact.user = user
				newcontact.contact_text = request.POST['contact_text']	
				newcontact.contact_type = request.POST['contact_type']
				newcontact.save()
		# if a GET (or any other method) we'll create a blank form
		else:
			contact_form = AddContactForm()
			rating_form = RatingForm()
	else:
		user = User.objects.get(id=user_id)
		private = False
		if request.method == 'POST':
			contact_form = AddContactForm()
			rating_form = RatingForm(request.POST)
			if not request.user.is_authenticated():
				return HttpResponseRedirect(reverse('login'))
			if rating_form.is_valid():
				rating = Review()
				rating.rater = request.user
				rating.ratee = user
				rating.stars = request.POST['stars']
				rating.text = request.POST['text']
				try:
					newseller = user.seller
				except:
					newseller = Seller()
					newseller.user = user
				allrevs = Review.objects.filter(ratee=user)
				sum = 0
				for rev in allrevs:
					sum += rev.stars
				newseller.rating = int(sum/len(allrevs))
				newseller.save()
				rating.save()
		else:
			contact_form = AddContactForm()
			rating_form = RatingForm()
	reviews = Review.objects.filter(ratee=user)

	return render(request, 'bookr/account.html', {'user': user, 'contact_form': contact_form, 'rating_form': rating_form, 'private': private, 'reviews': reviews })



def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def index(request):
	print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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