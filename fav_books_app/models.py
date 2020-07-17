
from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    
    def basic_validator(request, post_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        all_emails = User.objects.filter(email=post_data['email'])

        if len(post_data['first_name'])< 1:
            errors['first_name'] = 'First Name is required'

        if len(post_data['last_name'])< 1:
            errors['last_name'] = 'Last Name is required'

        if len(post_data['email'])< 1:
            errors['email'] = 'Email is required'

        if len(post_data['password'])< 1:
            errors['password'] = 'Password is required'

        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = 'Passwords do not match'

        if not email_regex.match(post_data['email']):
            errors['email_valid'] = 'Email not valid'
        
        if post_data['email'] in all_emails:
            errors['email_exist'] = 'Email already taken'


        return errors

    def login(request, post_data):
        from .models import User
        errors = {}

        all_users = User.objects.all()
        

        username_post = post_data['email']
        password_post = post_data['password']

        for user in all_users:
            if username_post == user.email and bcrypt.checkpw(password_post.encode(), user.password.encode())==True:
                errors = {}
                return errors
            
            if username_post != user.email or password_post != user.password:
                errors['password'] = 'Email/Password incorrect'


        return errors

    def new_book_valid(request,post_data):
        errors = {}
        if len(post_data['title']) <1:
            errors['title'] = 'Title is required'
        if len(post_data['desc']) <5:
            errors['description'] = 'Description must be at least 5 characters'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # books = favorite books that user has posted
    # liked_books = books from other users that user has liked
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    user_who_liked = models.ManyToManyField(User, related_name='liked_books')
    