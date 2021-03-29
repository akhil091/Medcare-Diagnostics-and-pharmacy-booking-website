from django.contrib import admin
from Lab.models import NotSure,Tests,HealthPackage,Condition,Order,Cart,Address, ZipCode, Lab_Result

@admin.register(NotSure)
class NotSureAdmin(admin.ModelAdmin):
    pass

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    pass

@admin.register(HealthPackage)
class HealthPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass    

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    pass

@admin.register(Lab_Result)
class Lab_ResultAdmin(admin.ModelAdmin):
    pass
