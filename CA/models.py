from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import *

class PrsignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    password = models.CharField(default='', max_length=15)
    ref_code=models.CharField(max_length=55,default='')
    recommend_by=models.CharField(max_length=30,default='',blank=False)
    joiningDate = models.DateField(default=timezone.now, null=True, blank=True)    
    payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
    ispaid = models.BooleanField(default=False)
    totalNoOfReferrals = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.email

class CompanyDetails(models.Model):
    owner = models.ForeignKey(PrsignUp, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='')
    comp_start_date = models.DateField(default=timezone.now, null=True, blank=True)
    comp_due_date = models.DateField(default=datetime.now()+timedelta(days=15))