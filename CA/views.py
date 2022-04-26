from calendar import c
import email
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.

# CA signup form
def SignupView(self, ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']

        Percentage = int(self.POST['percentage'])

        Created_by = self.POST['created_by']
        Address = self.POST['address']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        current_date = datetime.today().strftime('%Y-%m-%d')
        try:
            data=CasignUp.objects.get(email=Email)
            msg = 'Email already taken'
            return render(self, 'signup.html',{'msg':msg})
        except:
            try:
                if ConfirmPassword == Password:
                    CasignUp.objects.create(
                        name = Name,
                        email = Email, 
                        number = Number, 
                        password = Password, 
                        confirmPassword = ConfirmPassword, 
                        address = Address,
                        created_by = Created_by,
                        percentage = Percentage,
                    )
                    data=CasignUp.objects.get(email=Email)
                    Offerings.objects.create(CA = data, objectCreatedDate = current_date)
                    return redirect('CALOGIN')                
                else:
                    msg = 'Enter Same Password'
                    print(msg)
                    return render(self, 'signup.html',{'msg':msg}) 
            except:
                print("Inside except of CA signup")
                return render(self, 'signup.html',{'msg':'Something went wrong'}) 
    return render(self,'signup.html')


# ca login
def login(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = CasignUp.objects.get(email = em)
            print("Email is ",em,check.email)
            if check.password == pass1:
                self.session['email'] = check.email
                return redirect('CADASHBOARD')
            else:
                msg = 'Invalid Password'
                return render(self, 'login.html',{'msg':msg}) 
        except:
            print("Inside first except block")
            return render(self, 'login.html',{'msg':'Invalid Email ID'}) 
    return render(self,'login.html')


#ca dashboard
def dashboard(request):
    if 'email' in request.session:
        print('CA Dashboard TRY block')
        nameMsg = CasignUp.objects.filter(email = request.session['email'])
        obj=PrsignUp.objects.filter(recommend_by=nameMsg[0].email)
# --------------------------------For New Month----------------------------------
        offering = Offerings.objects.filter(CA = nameMsg[0]).last()
        current_date = datetime.today().strftime('%Y-%m-%d')
        day = datetime.now().day

        if ((day == 26) and (offering.isMonthCompleted == False) and (str(offering.objectCreatedDate) != str(current_date))):
            print("redirecting to newMonth function")
            return redirect('newMonth')
        else:
            print("On same function")
# -------------------------------------------------------------------------------
        newdate = datetime.today().strftime('%Y-%m-%d')
        if newdate >= str(nameMsg[0].payment_due_date):
            msg = 'Please pay the payment'
        else:
            msg = f'You can use it till {nameMsg[0].payment_due_date}'
# -------------------------------------------------------------------------------
        # offering = Offerings.objects.filter(CA = nameMsg).last()
        # day = datetime.now().day
        # if day == 1:
        #     print(f"Today is 1st date of month")
        #     CasignUp.objects.get(email = request.session['email']).update(pendingAmount = offering.monthlyAmount)
        #     offering.monthlyAmount = 0
        #     offering.save()
# -------------------------------------------------------------------------------
        pendAm = nameMsg[0].pendingAmount
        totalAm = nameMsg[0].totalAmount
        am = Offerings.objects.filter(CA = nameMsg[0]).last()
        monthAm = am.monthlyAmount

        print(f":::::::::: {pendAm} ::::: {monthAm} ::::: {totalAm} ::::::::::")
        return render(request, 'dashboard.html', {'key':nameMsg[0],'obj':obj,'len':len(obj), 'time' : msg, 'pendAm': pendAm, 'totalAm': totalAm, 'monthAm': monthAm})
    return redirect('CALOGIN')

# promoter signup
def prSignupView(self,ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        try:
            data=PrsignUp.objects.filter(email=Email)
            if data:
                msg = 'Email already taken'
                return render(self , 'prsignup.html',{'msg':msg})
            elif ConfirmPassword == Password:
                v = PrsignUp(name = Name, email = Email, number = Number, password = Password, confirmPassword = ConfirmPassword)
                try:
                    d=CasignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
                except:
                    d=PrsignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
                print(d.id)
                v.recommend_by=d.email
                v.save()
            # --------------------------------------------------------------------------------
                q1 = PrsignUp.objects.filter(recommend_by = d.email)
                d.totalNoOfReferrals = len(q1)     
                d.save()
            # --------------------------------------------------------------------------------
                return redirect('PRLOGIN')
            else:
                msg = 'Enter Same Password'
                return render(self , 'prsignup.html',{'msg':msg},{'ref_code':ref_code})     
        except:
            msg = 'Invalid Email Address'
            return render(self , 'prsignup.html',{'msg':msg}) 
    return render(self,'prsignup.html')

# promoter login
def prlogin(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = PrsignUp.objects.get(email = em)
            print("Email is ",em,check.email)
            if check.password == pass1:
                self.session['email'] = check.email
                return redirect('PRDASHBOARD')
            else:
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')
    return render(self,'prlogin.html')    

# ----------------------------------------------------------------------------------------------------------
def paidBySir(request):        
    caToBePaid = CasignUp.objects.filter(pendingAmount__gte= 1)
    for i in caToBePaid:
        pass
        # oo = Offerings.objects.filter(CA = i).update(isPaymentGivenBySir = True)
        # CasignUp.objects.filter(email = i.email).update(totalAmount = i.pendingAmount)
        # CasignUp.objects.filter(email = i.email).update(pendingAmount = 0)
    return HttpResponse("Paid Successfully")
    # return render(request, 'paidBySir.html', {'allCA':allCA})

# ----------------------------------------------------------------------------------------------------------

def newMonth(request):
    if 'email' in request.session:
        nameMsg = CasignUp.objects.filter(email = request.session['email'])
        offering = Offerings.objects.filter(CA = nameMsg[0]).last()
# -------------------------------------------------------------------------
        day = datetime.now().day
        current_date = datetime.today().strftime('%Y-%m-%d')
        print("03")
        if ((day == 26) and (offering.isMonthCompleted == False)):
            # if offering.isMonthCompleted == False:
            print(f"Today is 1st date of month")
            CasignUp.objects.filter(email = request.session['email']).update(pendingAmount = offering.monthlyAmount)
            print("06")
            Offerings.objects.filter(CA = nameMsg[0]).update(isMonthCompleted = True)
            print("07")
            # Offerings.objects.create(CA = nameMsg[0])
            data=CasignUp.objects.get(email = request.session['email'])
            Offerings.objects.create(CA = data, objectCreatedDate = current_date)
            print("08")
    # -------------------------------------------------------------------------------------
            return redirect('CADASHBOARD')
        else:
            return redirect('CADASHBOARD')
    return redirect('PRLOGIN')
# -------------------------------------------------------------------------------------
# import schedule
# import time
# schedule.every().hour.do(newMonth)
# -------------------------------------------------------------------------------------

def amountCalculation(request, id, prid):
    print("redirected to the amount calculation function")
    nameMsg = CasignUp.objects.get(id = id) 
    offering = Offerings.objects.filter(CA = nameMsg).last()
# -------------------------------------------------------------------------
    amount = 0
    nameMsg = CasignUp.objects.get(id = id)
    print(nameMsg.email,"100")
    Month_Amount = 0
    print("steps 00")
    Month_Amount += ((10000*nameMsg.percentage)/100)
    print("steps 01")
    amount = offering.monthlyAmount
    amount += Month_Amount
    offering.monthlyAmount = amount
    offering.save()

    # pamount = CasignUp.objects.filter(email = nameMsg.email)
    # pamount = pamount[0].pendingAmount + Month_Amount
    # CasignUp.objects.filter(email = nameMsg.email).update(pendingAmount = pamount)
    # PrsignUp.objects.filter(email = prid).update(isAmountCalculated = True)
    return redirect('PRDASHBOARD')

# ----------------------------------------------------------------------------------------------------------
# dashboard for promoter    
def PRdashboard(request):
    if 'email' in request.session:
        print("Inside promoter dashboard")
        z = ''
        msg = ''
        nameMsg = PrsignUp.objects.filter(email = request.session['email'])  
        print(nameMsg)
        obj=PrsignUp.objects.filter(recommend_by=nameMsg[0].email)
# ----------------------------------------------------------------------------------------------------
        due_id = PrsignUp.objects.get(id=nameMsg[0].id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        if newdate >= str(due_id.payment_due_date):
            z = 'Please pay the payment'
        else:
            z = f'You can use it till {due_id.payment_due_date}'
# ----------------------------------------------------------------------------------------------------
        if request.POST:
            if nameMsg[0].ispaid == False:
# ----------------------------------------------------------------------------------------------------
                rec_obj = nameMsg[0].recommend_by
                try:
                    print("-----------This is the CA's block----------")
                    rec_obj = CasignUp.objects.get(email = rec_obj)
                    print("try block")
                    if rec_obj:
                        total_referrals = rec_obj.totalNoOfReferrals
                        # CasignUp.objects.filter(email = rec_obj).update(totalNoOfReferrals = total_referrals +1)
                        PrsignUp.objects.filter(email = request.session['email']).update(ispaid = True)
                        msg = 'Paid Successfully'
                        print(msg)
                        return redirect('AMOUNTCALCULATION', rec_obj.id, nameMsg[0].email)
                except:
                    print("-----------This is the user's block----------")
                    rec_obj = PrsignUp.objects.get(email = rec_obj)
                    print("except block")
                    if rec_obj:
                        total_referrals = rec_obj.totalNoOfReferrals
                        # PrsignUp.objects.filter(email = rec_obj).update(totalNoOfReferrals = total_referrals +1)
                        PrsignUp.objects.filter(email = request.session['email']).update(ispaid = True)
                        given_date = rec_obj.payment_due_date
                        PrsignUp.objects.filter(email = rec_obj).update(payment_due_date = given_date + timedelta(days=30))
                        msg = 'Paid Successfully'
                        print(msg)
                print(nameMsg[0], "This is the logged in user")
                print(rec_obj, "This is the recommended user")
                PrsignUp.objects.filter(email = request.session['email']).update(payment_due_date = given_date + timedelta(days=365))
# ----------------------------------------------------------------------------------------------------
            else:
                msg = 'You have already paid'
                print(msg)
                return render(request, 'prdashboard.html', {'key':nameMsg[0],'obj':obj,'len':len(obj), 'time' : z , 'msg' : msg})
        # ------------------------------------------------------------------------------------
        return render(request, 'prdashboard.html', {'key':nameMsg[0],'obj':obj,'len':len(obj), 'time' : z , 'msg' : msg})
    return redirect('PRLOGIN')

# ca logout
def userLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('CALOGIN')

# pr logout
def prLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('PRLOGIN')    

# ca timeout
def timeout1(request):
    if 'email' in request.session:
        v=CasignUp.objects.get(email=request.session['email'])
        due_id = CasignUp.objects.get(id=v.id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        print("This is new date", newdate)
        print("This is due date",str(due_id.payment_due_date))
        if newdate >= str(due_id.payment_due_date):
            return HttpResponse('Please pay the payment')
        else:
            return HttpResponse(f'You can use it till {due_id.payment_due_date}')
    return redirect('CALOGIN')

# pr timeout
def PRtimeout(request):
    if 'email' in request.session:
        due_id = PrsignUp.objects.get(email=request.session['email'])
        print(due_id, "this is the due_id1")

        # due_id = PrsignUp.objects.get(id=PrsignUp.objects.get(email=request.session['email']).id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        # print("This is new date", newdate)
        # print("This is due date",str(due_id.payment_due_date))
        if newdate >= str(due_id.payment_due_date):
            return HttpResponse(f'{due_id} Please pay the payment')
        else:
            print(f'You can use it till {due_id.payment_due_date}')
            return HttpResponse(f'You can use it till {due_id.payment_due_date}')
    return redirect('PRLOGIN')

# Dashboard for main Host
def MAINDASH(request):
    li = []
    caobj =  CasignUp.objects.all()
    probj =  PrsignUp.objects.all()
    for i in caobj:
        caRefCount = PrsignUp.objects.filter(recommend_by = i.email)
        li.append(len(caRefCount))
    link  = 'http://127.0.0.1:8000/casignup/j75mnhd67v4m18r'    
    context = {
        'caobj': caobj,
        'probj': probj,        
        'calen': len(caobj),
        'prlen': len(probj),
        'link' : link,
        'li' : li,
    }
    print(li)
    # obj = CasignUp.objects.get(email = caobj[0].email)
    # print(obj)
    # print(obj.name)
    # print(obj.email)
    return render(request, 'maindash.html', context)






