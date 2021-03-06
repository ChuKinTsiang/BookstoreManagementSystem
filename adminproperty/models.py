from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import datetime
from django.db.models.signals import post_save
 
#class AdminProperty(models.Model):
class AdminProperty(User):
    admin = models.OneToOneField(User, primary_key=True, parent_link=True)
#    real_name = models.CharField(max_length=30, blank=True, null=True)
    GENDER_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'Male'),
        ('2', 'Female'),
        ('9', 'Not Applicable'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=0)
    birthday = models.DateField(blank=True, null=True)
#    def email(self):
#        return self.admin.email
    def display_birthday(self):
        return str(self.birthday)
    display_birthday.short_description = 'birthday'
    def age(self):
        if not self.birthday:
            return 'Unknown'
        today = datetime.date.today()
        birthday_this_year = datetime.date(today.year, self.birthday.month, self.birthday.day)
        years = today.year - self.birthday.year
        if today < birthday_this_year:
            years -= 1
#        return (datetime.datetime.now().date() - self.birthday)
        return years

class PerAdminPropertyBackend(ModelBackend):
    def has_module_perms(self, user, app_label):
        return app_label == 'adminproperty'
        
        
def add_AdminProperty(sender, instance, created, *args, **kwargs):
    if created:
        admin = AdminProperty(admin=instance)
        admin.__dict__.update(instance.__dict__)
        admin.save()
    
post_save.connect(add_AdminProperty, sender=User)


