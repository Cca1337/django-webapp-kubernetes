from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def register(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:

                login(response, user)
                messages.success(response, f"[REGISTERED] and Logged in! Welcome %s!" % username)

            else:
                messages.error(response, f"[ERROR] Something went wrong!")


        return redirect("/")

    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

def logout_view(response):

    logout(response)

    messages.success(response, f"[Logged out]")

    return redirect("/")
