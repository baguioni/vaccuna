from django.contrib import admin
from lgu.models import LocalGovernmentUnit, VaccinationSite


@admin.register(LocalGovernmentUnit)
class LocalGovernmentUnitAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(VaccinationSite)
class VaccinationSiteAdmin(admin.ModelAdmin):
    list_display = ('name', )
