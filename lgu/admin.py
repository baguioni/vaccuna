from django.contrib import admin
from lgu.models import LocalGovernmentUnit


@admin.register(LocalGovernmentUnit)
class LocalGovernmentUnitAdmin(admin.ModelAdmin):
    list_display = ('name', )
