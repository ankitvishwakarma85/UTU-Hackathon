from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail',kwargs={'pk':self.pk})

class Company(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    background = models.TextField() #Image link
    Eligibility = models.TextField()
    Status = models.CharField(max_length=10, choices = (('OPEN','Open'),('CLOSED','Closed')),default='OPEN' )
    #Student = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('company-detail',kwargs={'pk':self.pk})


class Query(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank= True, null=True)

    def __str__(self):
        return self.content

class Enrolled(models.Model):
    date_applied = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank= True, null=True)

    def __str__(self):
        return self.date_applied


    
