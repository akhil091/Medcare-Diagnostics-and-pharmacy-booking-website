from django.db import models
from django.conf import settings

import time
from time import time,ctime

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Specialization(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name


class Doctor(models.Model):

    Name = models.CharField(max_length=500)
    Gender = models.CharField(choices=GENDER, max_length=50)
    Qualification = models.CharField(max_length=500)
    week_timing = models.CharField(max_length=500,default="")
    Specialization = models.ForeignKey("Specialization",on_delete=models.CASCADE,null=True,blank=True)
    Condition = models.ForeignKey("Condition",on_delete=models.CASCADE,null=True,blank=True)
    Overall_Exp = models.CharField(max_length=500)
    Description = models.TextField()
    Fee = models.FloatField(blank=True,null=True)
    Profile_pic = models.ImageField(upload_to="Doctor_Profile",null=True,blank=True)

    Sunday = models.BooleanField(default=False)
    Monday = models.BooleanField(default=False)
    Tuesday = models.BooleanField(default=False)
    Wednesday = models.BooleanField(default=False)
    Thrusday = models.BooleanField(default=False)
    Friday = models.BooleanField(default=False)
    Saturday = models.BooleanField(default=False)

    Avaliable_From = models.TimeField(null=True,blank=True)
    Avaliable_Upto = models.TimeField(null=True,blank=True)

    def __str__(self):
        return self.Name

    def get_avaliablity(self):
        return f"{self.Avaliable_From} - {self.Avaliable_Upto}"

    def getDate(self,time):
        value = str(ctime(time))
        return value[:11] + value[20:24]

    def get_doc_timing(self):
        Booked = []
        Booked.append(self.Sunday)
        Booked.append(self.Monday)
        Booked.append(self.Tuesday)
        Booked.append(self.Wednesday)
        Booked.append(self.Thrusday)
        Booked.append(self.Friday)
        Booked.append(self.Saturday)

        weekdays = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        Date = []

        today = str(ctime(time())[:3])

        for i in range(len(weekdays)):
            if weekdays[i] == today:
                split_date = i
                break

        rendering_booked = Booked[split_date:] + Booked[:split_date]

        for i in range(7):
            t = float(time()) + float(i*86400)
            Date.append(self.getDate(t))

        Dict = {}
        present_doc = []
        for i in range(7):
            Dict[Date[i]] = rendering_booked[i]
            if rendering_booked[i]:
                present_doc.append(Date[i])

        return present_doc

class AllBooking(models.Model):

    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=50,null=True, blank=True)
    Last_Name = models.CharField(max_length=50,null=True, blank=True)
    Email = models.CharField(max_length=500,null=True, blank=True)
    Age = models.CharField(max_length=50,null=True, blank=True)
    Phone = models.CharField(max_length=50,null=True, blank=True)
    Doctor = models.ForeignKey("Doctor",on_delete=models.CASCADE)
    Date = models.CharField(max_length=50)
    Fee = models.FloatField()
    paid = models.BooleanField(default=False)
    Allot_Time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.User.First_Name} {self.User.Last_Name}"


