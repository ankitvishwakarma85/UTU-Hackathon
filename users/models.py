from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    year = (('FE','First Year'),('SE','Second Year'),('TE','Third Year'),('BE','Final Year'))
    branch = (('CS','Computer Science'),('IT','Information Technology'),('EXTC','Electronics and Telecommunication'),('ETRX','Electronics'))
    FirstName = models.CharField(max_length = 100, default="")
    LastName = models.CharField(max_length=100,default="")
    Contact = models.DecimalField(decimal_places = 0 ,max_digits=10,default=0)
    CollegeName = models.CharField(max_length = 100,default="")
    CollegeID = models.DecimalField(decimal_places = 0 ,max_digits=10,default=0)
    Year = models.CharField(max_length=10, choices = year,default="FE" )
    Branch = models.CharField(max_length=10, choices = branch,default="CS" )
    CGPA = models.DecimalField(decimal_places=2, default=8, max_digits=4)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profilepics')
    Resume = models.FileField(default = 'Sample.pdf', upload_to = 'Resume')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)