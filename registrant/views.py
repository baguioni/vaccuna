from django.shortcuts import render

def RegistrantHome(request, *args, **kwargs):
    return render(request, "home.html", {})
