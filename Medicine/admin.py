from django.contrib import admin

from Medicine.models import Medicines
# Register your models here.

@admin.register(Medicines)
class MedicinesAdmin(admin.ModelAdmin):
    pass
