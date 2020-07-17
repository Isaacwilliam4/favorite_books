from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode('utf-8')
    
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw
    )
    return redirect('/')

def all_users(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, 'all_user.html', context)

def login(request):
    errors = User.objects.login(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id      
        return redirect('/main')

def delete(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/all_users')

def main(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    all_books = Book.objects.all()
    context = {
        'user' : user,
        'all_books' : all_books
    }
    return render(request, 'main.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def new_book(request):
    errors = User.objects.new_book_valid(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')

    user = User.objects.get(id = request.session['user_id'])
    new_book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        user = user
    )
    user.liked_books.add(new_book)

    return redirect('/main')

def show_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'book' : book,
        'user' : user,
    }

    return render(request, 'show_book.html', context)

def like_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.add(book)
    return redirect(f'/show_book/{book.id}')
    
def unlike_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.remove(book)
    return redirect(f'/show_book/{book.id}')

def edit(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'book' : book,
        'user' : user,
    }

    return render(request, 'edit.html', context)

def update(request, book_id):
    errors = User.objects.new_book_valid(request.POST)
    book = Book.objects.get(id=book_id)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{book.id}')

    if request.method == 'POST':
        
        book = Book.objects.get(id=book_id)

        book.title = request.POST['title']
        book.desc = request.POST['desc']

        book.save()

    return redirect(f'/show_book/{book.id}')