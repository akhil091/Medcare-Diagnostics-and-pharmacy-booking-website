from django.db import models
from django.conf import settings

STATUS = (
    ('Incart','Incart'),
    ('Order Placed','Order Placed'),
    ('Arrived','Arrived'),
    ('Collected','Collected'),
    ('Result Out','Result Out'),
)

class Condition(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class NotSure(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    prescription = models.FileField(upload_to="Prescriptions")
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=50)
    valid = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tests(models.Model):

    Name = models.CharField(max_length=500)
    Description = models.TextField()
    Test_Type = models.CharField(max_length=50)
    Pre_Test_Information = models.CharField(max_length=500)
    Test_Components = models.CharField(max_length=500)
    Report_Delivery = models.CharField(max_length=500,null=True,blank=True)
    Price = models.FloatField()
    Discount_Price = models.FloatField()
    Method = models.TextField()
    conditions = models.ForeignKey("Condition", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Name} --> {self.id}"

    class Meta:
        verbose_name_plural = ("Tests")


class HealthPackage(models.Model):

    Name = models.CharField(max_length=500)
    Description = models.TextField()
    Test_Type = models.CharField(max_length=50)
    Pre_Test_Information = models.CharField(max_length=500)
    Test_Components = models.CharField(max_length=500)
    Report_Delivery = models.CharField(max_length=500,null=True,blank=True)
    Price = models.FloatField()
    Discount_Price = models.FloatField()
    Method = models.TextField()
    conditions = models.ForeignKey("Condition", on_delete=models.CASCADE)
    Tests_includes = models.ManyToManyField("Tests")

    def __str__(self):
        return f"{self.Name} --> {self.id}"


class Cart(models.Model):

    Patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Ordered = models.BooleanField(default=False)
    Test = models.ForeignKey("Tests", on_delete=models.CASCADE,null=True,blank=True)
    Package = models.ForeignKey("HealthPackage", on_delete=models.CASCADE,null=True,blank=True)
    when = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        if self.Test is not None:
            return f"{self.Test}"
        else:
            return f"{self.Package}"
        # return f"{self.Patient}"

    def get_original_price(self):
        if self.Test is not None:
            return self.Test.Price
        else:
            return self.Package.Price

    def get_total_price(self):
        if self.Test is not None:
            return self.Test.Discount_Price
        else:
            return self.Package.Discount_Price

    class Meta:
        verbose_name_plural = ("Cart")


class Order(models.Model):

    Patient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Tests = models.ManyToManyField("Cart", related_name=("Tests_Field"))
    Packages = models.ManyToManyField("Cart", related_name=("Packages_Field"))
    Ordered_Date = models.DateTimeField()
    Ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True,default=0)
    # payment_status = models.BooleanField(default=False, blank=True, null=True)
    service_status = models.CharField(choices=STATUS,blank=True, null=True,max_length=50)
    # payment_type = models.CharField(choices=PAYMENT_CHOICES,blank=True, null=True,max_length=50)
    Delivery_Charges = models.FloatField(default=0.0)
    when = models.CharField(max_length=500,null=True,blank=True)
    new = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.Patient}"

    def get_total(self):
        total = 0.0
        for in_cart in self.Tests.all():
            total += in_cart.get_total_price()
        for in_cart in self.Packages.all():
            total += in_cart.get_total_price()
        # if self.coupon:
        #     total -= dis * self.coupon.coupon_discount
        self.total_amount = total
        self.save()
        return total


class Address(models.Model):
    Patient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=500,null=True,blank=True)
    Last_Name = models.CharField(max_length=50)
    Address = models.TextField()
    Landmark = models.TextField(null=True,blank=True)
    Extra = models.TextField(null=True,blank=True)
    Phone = models.CharField(null=True,blank=True,max_length=15)
    PinCode = models.IntegerField(null=True,blank=True)
    default = models.BooleanField(default=False)
    secondary_address = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.First_Name}"
    class Meta:
        verbose_name_plural = ("Addresses")

class ZipCode(models.Model):
    Location = models.CharField(max_length=500)
    PinCode = models.IntegerField()
    Charges = models.FloatField()

    def __str__(self):
        return self.Location

"""

class Coupon(models.Model):
    coupon = models.CharField(max_length=15)
    coupon_discount = models.FloatField()

    def __str__(self):
        return self.coupon
"""

class Lab_Result(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Patient_Name = models.CharField(max_length=500)
    Test = models.CharField(max_length=500)
    Result = models.FileField(upload_to="Results")

    def __str__(self):
        return f"{self.User}"
    
