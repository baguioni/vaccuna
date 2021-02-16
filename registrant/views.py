from django.shortcuts import render
from registrant.forms import IndividualRegistrantForm


def RegistrantHome(request, *args, **kwargs):
    return render(request, "home.html", {})

def IndividualRegistrantRegister(request):
    form = IndividualRegistrantForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }

    return render(
        request, 'form.html', context
    )
