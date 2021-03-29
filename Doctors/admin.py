from django.contrib import admin
from Doctors.models import Specialization,Condition, Doctor, AllBooking

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    pass

@admin.register(AllBooking)
class AllBookingAdmin(admin.ModelAdmin):
    pass

