from django.shortcuts import render, HttpResponse, redirect
from autoservice import models,forms
import datetime
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from autoservice.api_views import GetUserCars
def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    context = {}
    return render(request,
                  'index.html',
                  context)
def cars(request):
    context ={}
    user = request.user
    as_user = models.AS_user.objects.get(user=user)
    pk = request.GET['pk']
    current_user = models.User.objects.get(pk=pk)
    current_as_user = models.AS_user.objects.get(user=current_user)
    if not user.is_authenticated:
        return redirect('/login')
    request.query_params = {}
    request.query_params['pk'] = user.pk
    # c = GetUserCars()
    # cars = c.get(request)
    context['lang'] = as_user.lang.short_code
    context['cars'] = models.UserCar.objects.filter(user=current_as_user)
    return render(request,'my_cars.html',context)

def logon(request):
    context = {}

    form = forms.LoginForm()
    if request.method == 'GET':
        context['form'] = form
        return render(request,
                      'login.html',
                      context)
    if request.method == 'POST':
        user1 = authenticate(username=request.POST['email'].lower(),
                            password=request.POST['password'])

        if not user1 is None:
            login(request, user1)
            request.session.set_expiry(1209600)
            if Token.objects.filter(user_id=user1.id).count() == 0:
                token = Token.objects.create(user=user1)
                token.save_base()
            return redirect('/')
        else:
            form = forms.LoginForm(request.POST)
            form.add_error('email','Неправильные данные')
            form.add_error('password','Неправильные данные')
            context['form'] = form
            return render(request,
                      'login.html',
                      context)




def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    context = {}
    form = forms.RegisterForm
    if request.method == 'GET':
        context['form'] = form()
    if request.method == 'POST':
        form =  form(request.POST)
        if form.is_valid():
            passw = request.POST['password']
            passw1 = request.POST['password1']
            if passw == passw1:
                u = models.User()
                au = models.AS_user()
                u.first_name = request.POST['first_name']
                u.email = request.POST['email']
                u.last_name = request.POST['last_name']
                u.username = request.POST['email']
                u.set_password(request.POST['password'])
                u.save()
                au.user = u
                lang = models.Language.objects.get(pk=request.POST['lang'])
                au.lang = lang
                user_to_login = authenticate(username=request.POST['email'].lower(),
                                             password=request.POST['password'])
                login(request, user_to_login)
                return redirect('/')
            else:
                form.add_error('password','Пароли не совпадают')
        context['form'] = form
    return render(request,
                  'registration/registration.html',
                  context)
def user_add_car(request):
    context={}
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    as_user = models.AS_user.objects.get(user=user)
    form = forms.CarFormForUser
    if request.method == 'GET':
        context['form'] = form()
    if request.method == 'POST':
        form =  form(request.POST)
        if form.is_valid():
            lang = as_user.lang.short_code
            car = models.Car()
            if lang == 'ru':
                car.name_ru = request.POST['name']
            if lang == 'en':
                car.name_en = request.POST['name']
            car.year = request.POST['year']
            car.save()
            car_user = models.UserCar()
            car_user.user = as_user
            car_user.car = car
            car_user.save()
            return redirect('/my_cars')

    context['form'] = form
    return render(request,'add_user_car.html',context)

def add_car_for_user(request):
    context={}

    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    as_user = models.AS_user.objects.get(user=user)
    form = forms.CarFormForUser
    if request.method == 'GET':
        context['form'] = form()
    if request.method == 'POST':
        form =  form(request.POST)
        if form.is_valid():
            lang = as_user.lang.short_code
            car = models.Car()
            if lang == 'ru':
                car.name_ru = request.POST['name']
            if lang == 'en':
                car.name_en = request.POST['name']
            car.year = request.POST['year']
            car.save()
            car_user = models.UserCar()
            car_user.user = as_user
            car_user.car = car
            car_user.save()
            return redirect('/my_cars')

    context['form'] = form
    return render(request,
                  'add_user_car.html',
                  context)

def user_detail(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')

    pk = request.GET['pk']
    current_user = models.User.objects.get(pk=pk)
    current_as_user = models.AS_user.objects.get(user=current_user)

    as_user = models.AS_user.objects.get(user=user)
    context = {'pk':pk,'current_user':current_user,
               'current_as_user':current_as_user,
               'user':user,'as_user':as_user}
    return render(request,
                  'user_detail.html',
                  context)

def change_user_data(request):
    pk = request.GET['pk']
    user = request.user
    if not user.is_authenticated:
        return redirect('/login')
    context = {}
    form = forms.UserDataForm
    current_user = models.User.objects.get(pk=pk)
    current_as_user = models.AS_user.objects.get(user=current_user)
    if request.method == 'GET':
        form = form(instance=current_user)
        form.get_data()
    if request.method == 'POST':
        form = form(instance=current_user,
                    data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_detail?pk=' + str(current_user.pk))
    context['form'] = form
    return render(request,
                  'change_user_data.html',
                  context)

def change_lang(request):
    user = request.user
    context = {}
    if not user.is_authenticated:
        return redirect('/login')
    pk = request.GET['pk']
    current_user = models.User.objects.get(pk=pk)
    current_as_user = models.AS_user.objects.get(user= current_user)
    form = forms.ChangeLang
    if request.method == 'GET':
        form = form(instance=current_as_user)
        form.get_data()
    if request.method == 'POST':
        form = form(instance=current_as_user,
                    data=request.POST)


        if form.is_valid():
            form.save()
            return redirect('/user_detail?pk='+str(current_user.pk))
    context['form'] = form
    return render(request,
                  'change_lang.html',
                  context)







# Create your views here.
