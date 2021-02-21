from django.shortcuts import render
from lgu.models import LocalGovernmentUnit

def DashboardView(request, lgu_id):
    obj = LocalGovernmentUnit.objects.get(id=lgu_id)
    context = {
        'obj': obj
    }
    return render(request, "mapTemplate.html", context)
