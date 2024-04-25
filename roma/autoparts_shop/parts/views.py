from django.shortcuts import render, get_object_or_404, redirect
from .models import Part
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.http import HttpResponse, Http404
import os

def home(request):
    parts = Part.objects.all()
    return render(request, 'parts/home.html', {'parts': parts})

@login_required
def product_detail(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    return render(request, 'parts/product_detail.html', {'part': part})

def checkout(request):
    purchased = False  # Флаг для отображения сообщения о покупке
    
    if request.method == 'POST':
        # Здесь должна быть логика обработки заказа
        # Например, сохранение данных заказа в базе данных и т.д.
        
        purchased = True
    
    context = {
        'purchased': purchased
    }
    
    return render(request, 'parts/checkout.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'parts/signup.html', {'form': form})
    
@login_required
def profile(request):
    return render(request, 'parts/profile.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'parts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'parts/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('home')
  
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # После успешной регистрации перенаправляем на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'parts/signup.html', {'form': form})
    
def media(request, path):
    media_root = settings.MEDIA_ROOT
    file_path = os.path.join(media_root, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return HttpResponse(file.read(), content_type='image/jpeg')  # Предположим, что это изображения JPEG
    else:
        raise Http404
