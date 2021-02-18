from django.shortcuts import render
from registrant.forms import IndividualRegistrantForm, AddressFieldForm
from django.http import HttpResponseRedirect

def RegistrantHome(request, *args, **kwargs):
    return render(request, "home.html", {})

def IndividualRegistrantRegister(request):
    individual_form = IndividualRegistrantForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)

    if request.method == 'POST':
        if individual_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            individual = individual_form.save(commit=False)
            # Save address to individual
            individual.address = address
            individual.save()
            return HttpResponseRedirect('/success')
        else:
            context = {
                'individual_form': individual_form,
                'address_form': address_form,
            }
    else:
        context = {
            'individual_form': individual_form,
            'address_form': address_form,
        }

    return render(
        request, 'form.html', context
    )
