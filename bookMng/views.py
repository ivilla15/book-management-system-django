from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import MainMenu

from .forms import BookForm
from django.http import HttpResponseRedirect

from .models import Book

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.decorators.http import (require_POST)
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():

            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()

            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })


def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.get_comments()

    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.book = book
                comment.user = request.user
                comment.save()
                return redirect('book_detail', book_id=book.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comments': comments,
        'form': form,
    })




def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def shopping_cart(request):
    total_price = 0

    # Retrieve the list of book IDs from the session's 'cart' key
    cart = request.session.get('cart', [])

    # Get the books in the cart using the list of book IDs
    books_in_cart = Book.objects.filter(id__in=cart)

    # Loop through the books and modify the pic_path
    for book in books_in_cart:
        book.pic_path = book.picture.url[14:]  # Adjust the picture path
        total_price += book.price

    # Render the shopping cart page with the context
    return render(
        request,
        template_name='bookMng/shopping_cart.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books_in_cart,  # Books in the cart
            'total_price': total_price,
        }
    )


@require_POST
def cart_remove(request, book_id):
    total_price = 0

    # Retrieve the cart from the session and convert it to a list
    cart = list(request.session.get('cart', []))

    # Check if the book_id is in the cart and remove it if it is
    if book_id in cart:
        cart.remove(book_id)

    # Save the updated cart back to the session
    request.session['cart'] = cart

    # Get the books in the cart
    books_in_cart = Book.objects.filter(id__in=cart)

    # Loop through the books and modify the pic_path
    for book in books_in_cart:
        book.pic_path = book.picture.url[14:]  # Adjust the picture path
        total_price += book.price

    # Render the shopping cart page with the updated list of books
    return render(
        request,
        template_name='bookMng/shopping_cart.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books_in_cart,  # Books in the cart
            'total_price': total_price,
        }
    )
@require_POST
def cart_add(request, book_id):
    # Retrieve the cart from the session and convert it to a list
    cart = list(request.session.get('cart', []))

    # Check if the book_id is not already in the cart and append it if it isn't
    if book_id not in cart:
        cart.append(book_id)

    # Save the updated cart back to the session
    request.session['cart'] = cart

    # Get the books in the cart
    books_in_cart = Book.objects.filter(id__in=cart)

    # Get all books to display
    books = Book.objects.all()

    # Modify the pic_path for each book
    for b in books:
        b.pic_path = b.picture.url[14:]

    # Render the page with the list of books
    return render(
        request,
        template_name='bookMng/displaybooks.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books,  # All books to display
        }
    )

def favorites(request):
    # Retrieve the list of book IDs from the session's 'favorites' key
    favorites = request.session.get('favorites', [])

    # Get the books in the favorites using the list of book IDs
    books_in_favorites = Book.objects.filter(id__in=favorites)

    # Loop through the books and modify the pic_path
    for book in books_in_favorites:
        book.pic_path = book.picture.url[14:]  # Adjust the picture path

    # Render the favorites page with the context
    return render(
        request,
        template_name='bookMng/favorites.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books_in_favorites,  # Books in favorites
        }
    )


@require_POST
def favorites_remove(request, book_id):
    # Retrieve the favorites from the session and convert it to a list
    favorites = list(request.session.get('favorites', []))

    # Check if the book_id is in favorites and remove it if it is
    if book_id in favorites:
        favorites.remove(book_id)

    # Save the updated favorites back to the session
    request.session['favorites'] = favorites

    # Get the books in the cart
    books_in_favorites = Book.objects.filter(id__in=favorites)

    # Render the favorites page with the updated list of books
    return render(
        request,
        template_name='bookMng/favorites.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books_in_favorites,  # Books in favorites
        }
    )
@require_POST
def favorites_add(request, book_id):
    # Retrieve the favorites from the session and convert it to a list
    favorites = list(request.session.get('favorites', []))

    # Check if the book_id is not already in favorites and append it if it isn't
    if book_id not in favorites:
        favorites.append(book_id)

    # Save the updated favorites back to the session
    request.session['favorites'] = favorites

    # Get the books in favorites
    books_in_favorites = Book.objects.filter(id__in=favorites)

    # Get all books to display
    books = Book.objects.all()

    # Modify the pic_path for each book
    for b in books:
        b.pic_path = b.picture.url[14:]

    # Render the page with the list of books
    return render(
        request,
        template_name='bookMng/displaybooks.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
            'books': books,  # All books to display
        }
    )

def about_us(request):
    return render(
        request,
        template_name='bookMng/about_us.html',
        context={
            'item_list': MainMenu.objects.all(),  # Main menu items
        }
    )

def search_books(request):
    query = request.GET.get('q')  # Get the search term
    books = Book.objects.filter(
        Q(name__icontains=query) | Q(username__username__icontains=query)
    ) if query else []

    return render(request, 'bookMng/search_results.html',
                  {'item_list': MainMenu.objects.all(), 'books': books, 'query': query})

def mybooks(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(username=request.user)
        for b in books:
            b.pic_path = b.picture.url[14:]
        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': books,
                      })
    else:
        return redirect('login')