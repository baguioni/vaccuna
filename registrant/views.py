from django.shortcuts import render
from registrant.forms import IndividualRegistrantForm, AddressFieldForm, IndividualFormset
from core.forms import UserSignupForm
from django.http import HttpResponseRedirect
from registrant.models import Registrant, Individual


def RegistrantHome(request, *args, **kwargs):
    return render(request, "home.html", {})

def HouseholdRegisterView(request):
    if request.method == "GET":
        user_form = UserSignupForm(request.GET or None)
        address_form = AddressFieldForm(request.POST or None)
        formset = IndividualFormset(queryset=Individual.objects.none())

    if request.method == "POST":

        user_form = UserSignupForm(request.POST)
        address_form = AddressFieldForm(request.POST or None)
        formset = IndividualFormset(request.POST)

        if formset.is_valid() and address_form.is_valid() and user_form.is_valid():
            address = address_form.save()
            user = user_form.save(commit=False)
            user.is_registrant = True
            user.save()

            # Create registrant object
            registrant = Registrant(user=user, address=address, is_household=True)
            registrant.save()

            for individual_form in formset:
                if individual_form.is_valid():
                    try:
                        individual = individual_form.save(commit=False)
                        individual.registrant = registrant
                        individual.save()
                    except:
                        print('database error')

            return HttpResponseRedirect('/success')

    context = {
        'user_form': user_form,
        'address_form': address_form,
        'formset': formset,

    }

    return render(request, 'householdForm.html', context)

def IndividualRegisterView(request):
    individual_form = IndividualRegistrantForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)
    user_form = UserSignupForm(request.POST or None)

    if request.method == 'POST':

        if individual_form.is_valid() and address_form.is_valid() and user_form.is_valid():
            # Save user and address
            address = address_form.save()
            user = user_form.save(commit=False)
            user.is_registrant = True
            user.save()

            # Create registrant object
            registrant = Registrant(user=user, address=address)
            registrant.save()

            # Save link individual to registrant
            individual = individual_form.save(commit=False)
            individual.registrant = registrant
            individual.save()

            return HttpResponseRedirect('/success')
        else:
            context = {
                'individual_form': individual_form,
                'address_form': address_form,
                'user_form': user_form,
            }
    else:
        context = {
            'individual_form': individual_form,
            'address_form': address_form,
            'user_form': user_form,
        }

    return render(
        request, 'individualForm.html', context
    )
