from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .models import User, Note
from django.views.decorators.csrf import csrf_exempt

# FLAW 5 (A07 - Auth Failures): No brute force protection
from django.core.cache import cache
# FIX: Uncomment below to add rate limiting
# from django.core.cache import cache
#@csrf_exempt
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # FLAW 5 FIX: Add this block before the query
        #attempts_key = f"login_attempts_{username}"
        #attempts = cache.get(attempts_key, 0)
        #if attempts >= 5:
        #    return HttpResponse("Too many attempts. Try again later.", status=429)
        #cache.set(attempts_key, attempts + 1, timeout=300)

        #F(A03 - Injection): Raw SQL with user input
        # FIX: Use ORM instead:
        #user = User.objects.filter(username=username, password=password).first()
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM notes_user WHERE username='{username}' AND password='{password}'"
            )
            row = cursor.fetchone()
        #user = User.objects.filter(username=username, password=password).first()
        #row = (user.id,) if user else None


        if row:
            response = redirect('/notes/')
            response.set_cookie('user_id', row[0])
            return response
        else:
            error = "Invalid credentials"

    return render(request, 'notes/login.html', {'error': error})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #FLAW 3 FIX: Hash the password before saving
        #from django.contrib.auth.hashers import make_password
        #User.objects.create(username=username, password=make_password(password))
        User.objects.create(username=username, password=password)
        return redirect('/login/')

    return render(request, 'notes/register.html')


def notes_view(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('/login/')

    # FLAW 2 (A01 - Broken Access Control): Uses URL param instead of session
    # FIX: Remove the override below, always use the cookie's user_id
    user_id = request.GET.get('user_id', user_id)

    notes = Note.objects.filter(user_id=user_id)
    return render(request, 'notes/notes.html', {'notes': notes, 'user_id': user_id})


def create_note(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return redirect('/login/')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(user_id=user_id, title=title, content=content)
        return redirect('/notes/')

    return render(request, 'notes/notes.html', {})