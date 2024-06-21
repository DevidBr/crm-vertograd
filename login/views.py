from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from login.forms import LoginForm


def main(request):
    if request.user.is_authenticated is False:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    login(request, user=user)
                    return redirect("dashboard:home_dashboard")
                else:
                    form.add_error(None, "Неправильный логин или пароль")
        else:
            form = LoginForm()
        return render(request, "login/index.html", {"form": form})
    else:
        return redirect("dashboard:home_dashboard")


@login_required(login_url="login:main")
def log_out(request):
    logout(request)
    return redirect("login:main")



