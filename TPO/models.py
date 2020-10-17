from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class News(models.Model):
    domains = (
        ('PYTHON DEV','Python Dev'),
        ('JAVA DEV','Java Dev'),
        ('FRONTEND DEV','Frontend Dev'),
        ('BACKEND DEV','Backend Dev'),
        ('FULLSTACK DEV','Fullstack Dev'),
        ('DATA SCIENTIST','Data Scientist')
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    Domain = models.CharField(max_length=50, choices = domains ,default="JAVA DEV" )

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

class CompanyAnalytics(models.Model):
    cname=models.CharField(max_length=50)
    cplaced=models.IntegerField()
    ctype=models.CharField(max_length=50)
    pkg=(
        ("ELITE","Elite"),
        ("SUPERD","Super Dream"),
        ("DREAM","Dream"),
        ("NORMAL","Normal")
    )
    c_pkg_type=models.CharField(max_length=50,choices=pkg)

    
