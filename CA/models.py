from django.db import models
from datetime import datetime, timedelta
from .utils import *
# Create your models here.
class PrsignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    number = models.PositiveIntegerField()
    password = models.CharField(default='', max_length=15)
    confirmPassword = models.CharField(default='', max_length=15)
    link=models.CharField(max_length=55,default='')
    # recommend_by=models.ForeignKey(CasignUp,on_delete=models.CASCADE,null=True,blank=True)
    recommend_by=models.CharField(max_length=30,default='',blank=False)
    payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
    
    def __str__(self):
        return self.email

    def save(self,*args,**kwargs):
        code=genrated_ref_code()
        self.link="http://127.0.0.1:8000/prsignup/"+str(code)
        super().save(*args,**kwargs)         



class CasignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    number = models.PositiveIntegerField()
    password = models.CharField(default='', max_length=15)
    confirmPassword = models.CharField(default='', max_length=15)
    link=models.CharField(max_length=55,default='')
    payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
    subuser=models.ForeignKey(PrsignUp,on_delete=models.CASCADE,null=True,blank=True)
    
    percentage = models.CharField(default='', max_length=15)
    totalNoOfReferrals = models.CharField(default=0, max_length=100)
    amount = models.CharField(default=0, max_length=15)


    def __str__(self):
        return self.email

    def save(self,*args,**kwargs):
        code=genrated_ref_code()
        self.link="http://127.0.0.1:8000/prsignup/"+str(code)
        super().save(*args,**kwargs)    
