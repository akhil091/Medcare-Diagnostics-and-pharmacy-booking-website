from django.db import models

class Messages(models.Model):
    
    Name = models.CharField(max_length=500)
    Email = models.CharField(max_length=500)
    Contact = models.CharField(max_length=500)
    Subject = models.CharField(max_length=500)
    Message = models.TextField()

    def __str__(self):
        return self.Name
    