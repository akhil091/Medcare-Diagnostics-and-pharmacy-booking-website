from django.db import models

class Medicines(models.Model):
    Name = models.CharField(max_length=500)
    Phone = models.CharField(max_length=15)
    Prescription_File = models.FileField(upload_to="Prescriptions",null=True,blank=True)
    Prescription_Image = models.ImageField(upload_to="Prescriptions",null=True,blank=True)
    Address = models.TextField()
    Other_Detail = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.Name