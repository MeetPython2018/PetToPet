from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'verify/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            tel = form.cleaned_data['tel']
            request.session['tel'] = tel
            return redirect(reverse("official:index"))
        else:
            error_msg = form.errors

            return render(request, 'verify/login.html', {'form': form, 'errors': error_msg})


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        error_msg = form.errors
        return render(request, 'verify/register.html', {'form': form, 'errors': error_msg})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            pass_word = request.POST.get("password", "")
            form.password = make_password(pass_word)
            form.save()
            return redirect(reverse('verify:login'))
        else:
            error_msg = form.errors
            return render(request, 'verify/register.html', {'form': form, 'errors': error_msg})


def wel(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'verify/wel.html', {'form': form})


def secede(request):
    if request.method == 'GET':
        del request.session['tel']
        return redirect(reverse("verify:login"))

