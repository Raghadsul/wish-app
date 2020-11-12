from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name=first_name,last_name=last_name, email=email, password=pw_hash)
    return redirect("/")

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['username'])
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/wishes')
        return redirect("/")

def dashboard(request):
    user = User.objects.get(id=request.session['userid'])
    all_wishes = Wish.objects.all().filter(is_granded=True)
    user_wishes = Wish.objects.filter(wished_by=user, is_granded=False)
    context = { 
        'user': user,
        'all_wishes': all_wishes,
        'user_wishes': user_wishes
    }
    return render(request, "dashboard.html", context)

def newWish(request):
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
    }
    if request.method == "POST":
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(id=request.session['userid'])
            item = request.POST['item']
            desc = request.POST['desc']
            new_wish=Wish.objects.create(item=item, desc=desc, wished_by=user)
            return redirect('/wishes')
    return render(request, "new_wish.html", context)

def removeWish(request, wish_id):
    if request.method == "GET":
        user = User.objects.get(id=request.session['userid'])
        wish = Wish.objects.filter(id=wish_id)
        wish.delete()
    return redirect('/wishes')

def editWish(request, wish_id):
    user = User.objects.get(id=request.session['userid'])
    wish = Wish.objects.get(id=wish_id)
    context = {
        'user': user,
        'wish': wish
    }
    if request.method == "POST":
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            item = request.POST['item']
            desc = request.POST['desc']
            Wish.objects.filter(id=wish_id).update(item=item)
            Wish.objects.filter(id=wish_id).update(desc=desc)
            return redirect('/wishes')
    return render(request, "edit_wish.html", context)

def stats(request):
    user = User.objects.get(id=request.session['userid'])
    all_granded_wishes = Wish.objects.filter(is_granded=True)
    user_granded_wishes = Wish.objects.filter(wished_by=user, is_granded=True)
    user_pending_wishes = Wish.objects.filter(wished_by=user, is_granded=False)
    context = {
        'user': user,
        'all_granded_wishes': all_granded_wishes,
        'user_granded_wishes': user_granded_wishes,
        'user_pending_wishes': user_pending_wishes
    }
    return render(request, "stats.html", context)

def like(request, wish_id):
    user = User.objects.get(id=request.session['userid'])
    wish = Wish.objects.get(id=wish_id)
    user.liked_wishes.add(wish)
    return redirect("/wishes")

def granted(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.is_granded = True
    wish.save()
    return redirect("/wishes")

def logout(request):
    del request.session['userid']
    return redirect("/")