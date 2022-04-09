from calendar import c
import email
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime
# Create your views here.

# CA signup form
def SignupView1(self, ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']

        Tier1 = int(self.POST['tier1'])
        Tier2 = int(self.POST['tier2'])
        Tier3 = int(self.POST['tier3'])

        Percentage1 = int(self.POST['percentage1'])
        Percentage2 = int(self.POST['percentage2'])
        Percentage3 = int(self.POST['percentage3'])

        Created_by = self.POST['created_by']
        Address = self.POST['address']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
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
                    )
                    data=CasignUp.objects.get(email=Email)
                    try:
                        if Tier1 == 0:
                            Offerings.objects.create(CA = data, tierName = 'Tier1', tierNo = 0, percentage = Percentage1)
                    except:
                        msg = 'Tier 1 Should start from 0'
                        print(msg)
                        return render(self, 'signup.html',{'msg':msg}) 
                    
                    try:
                        if (Tier2 > Tier1) and (Tier2 < Tier3):
                            Offerings.objects.create(CA = data, tierName = 'Tier2', tierNo = Tier2, percentage = Percentage2)
                    except:
                        msg = 'Tier 2 Should be grater then Tier 1 \n Tier 2 should be less then Tier 3'
                        print(msg)
                        return render(self, 'signup.html',{'msg':msg}) 

                    try:
                        if (Tier3 > Tier2) and (Tier3 > Tier1):
                            Offerings.objects.create(CA = data, tierName = 'Tier3', tierNo = Tier3, percentage = Percentage3)
                    except:
                        msg = 'Tier 3 Should be grater then Tier 1 and Tier 2'
                        print(msg)
                        return render(self, 'signup.html',{'msg':msg}) 
                    
                    return redirect('CALOGIN')                
                else:
                    msg = 'Enter Same Password'
                    print(msg)
                    return render(self, 'signup.html',{'msg':msg}) 
            except(ValueError):
                print("Inside value error of CA signup")
                return render(self, 'signup.html',{'msg':'Something went wrong'}) 
    return render(self,'signup.html')

def SignupView(self, ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']
        Tier1 = int(self.POST['tier1'])
        Tier2 = int(self.POST['tier2'])
        Tier3 = int(self.POST['tier3'])
        Percentage1 = int(self.POST['percentage1'])
        Percentage2 = int(self.POST['percentage2'])
        Percentage3 = int(self.POST['percentage3'])
        Created_by = self.POST['created_by']
        Address = self.POST['address']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        try:
            data=CasignUp.objects.get(email=Email)
            msg = 'Email already taken'
            return render(self, 'signup.html',{'msg':msg})
        except:
            try:
                if ConfirmPassword == Password:
                    
                    if (Tier1 == 0) and ((Tier2 > Tier1) and (Tier2 < Tier3)) and ((Tier3 > Tier2) and (Tier3 > Tier1)):                   
                        
                        CasignUp.objects.create(
                            name = Name, 
                            email = Email, 
                            number = Number, 
                            password = Password, 
                            confirmPassword = ConfirmPassword, 
                            address = Address,
                            created_by = Created_by,
                        )

                        data=CasignUp.objects.get(email=Email)
                        Offerings.objects.create(CA = data, tierName = 'Tier1', updatedTierNo = 0 ,    tierNo = 0, percentage = Percentage1)                 
                        Offerings.objects.create(CA = data, tierName = 'Tier2', updatedTierNo = Tier2 ,tierNo = Tier2, percentage = Percentage2)
                        Offerings.objects.create(CA = data, tierName = 'Tier3', updatedTierNo = Tier3 ,tierNo = Tier3, percentage = Percentage3)
                    else:
                        msg = 'Please Read the Tier NOTE before entering Tier'
                        print(msg)
                        return render(self, 'signup.html',{'msg':msg}) 
                    
                    return redirect('CALOGIN')                
                else:
                    msg = 'Enter Same Password'
                    print(msg)
                    return render(self, 'signup.html',{'msg':msg}) 
            except(ValueError):
                print("Inside value error of CA signup")
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
                # print(check.Password)
                self.session['email'] = check.email
                return redirect('CADASHBOARD')
                # nameMsg = CasignUp.objects.get(email = em)
                # msg = 'User Successfully logged in'
                # print(msg)
                # return render(self, 'dashboard.html', {'key':nameMsg})
            else:
                msg = 'Invalid Password'
                return render(self, 'login.html',{'msg':msg}) 
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')
    return render(self,'login.html')

#ca dashboard
def dashboard(request):
    if 'email' in request.session:
        try:
            print('Dashboard TRY block')
            # nameMsg = logged in user's email
            nameMsg = CasignUp.objects.get(email = request.session['email'])
            # obj = giving queryset of all promoter's data
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)
            newdate = datetime.today().strftime('%Y-%m-%d')

            if newdate >= str(nameMsg.payment_due_date):
                msg = 'Please pay the payment'
            else:
                msg = f'You can use it till {nameMsg.payment_due_date}'

            print("redirct")
            return render(request, 'dashboard.html', {'key':nameMsg,'obj':obj,'len':len(obj), 'time' : msg})
        except:
            print("Inside except of dashboard section")
            del request.session['email']
            return redirect('CALOGIN')
    return redirect('CALOGIN')


def paidBySir(request):
    if 'email' in request.session:
        nameMsg = CasignUp.objects.get(email = request.session['email'])            
        obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)            
        
        offering1 = Offerings.objects.filter(CA=nameMsg, tierName='Tier1').last()
        offering2 = Offerings.objects.filter(CA=nameMsg, tierName='Tier2').last()
        offering3 = Offerings.objects.filter(CA=nameMsg, tierName='Tier3').last()

        for i in obj:
            if i.ispaid == True:
                if i.isPaymentRecievedFromSir == False:
                    i.isGivenBySir = True                
                    # i.isPaymentRecievedFromSir = True                
                    i.save()                   
            else:
                print(f"{i.name} user has not paid yet")
        return HttpResponse("Paid Successfully")

    return redirect('CALOGIN')


def amountCalculation(request):
    if 'email' in request.session:
        tier1 = False
        tier2 = False
        tier3 = False
        # try:
        # print('amountCalculations TRY block')
        # Access the data of logged in CA
        nameMsg = CasignUp.objects.get(email = request.session['email'])            
        print(nameMsg.totalAmount,"This is the total Amount")
        # Promoter data of perticular CA referral
        obj=PrsignUp.objects.filter(recommend_by=nameMsg.email, ispaid = True)

        offering1 = Offerings.objects.filter(CA=nameMsg, tierName='Tier1').last()
        offering2 = Offerings.objects.filter(CA=nameMsg, tierName='Tier2').last()
        offering3 = Offerings.objects.filter(CA=nameMsg, tierName='Tier3').last()           
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
        # for tier 1
        if nameMsg.totalNoOfReferrals <= offering2.tierNo-1:
            tier1 = True
            print("Inside Tier 1")
        
        # for tier 2
        elif (nameMsg.totalNoOfReferrals >= offering2.tierNo) and (nameMsg.totalNoOfReferrals <= offering3.tierNo-1):
            tier1 = False
            tier2 = True
            print("Inside Tier 2")
        
        # for tier 3
        else:
            tier2 = False
            tier3 = True
            print("Inside Tier 3")
        print('........................')   
# --------------------------------Amount Calculations For Tier1---------------------------------------------
        if tier1:
            amountHasToBePaid = 0
            for i in obj:
                if i.isAmountCalculated == False:
                    if offering1.isGivenBySir == False:
                        print("00")
                        amountHasToBePaid += ((10000*offering1.percentage)/100)
                        print("01")
                        offering1.monthlyAmount += amountHasToBePaid
                        print("02")

                        offering1.pendingAmount = offering1.monthlyAmount
                        print("03")

                        # i.isAmountCalculated = True
                        # PrsignUp.objects.filter(recommend_by=nameMsg.email, ispaid= True).update(isAmountCalculated = True)
                        PrsignUp.objects.filter(id=i.id).update(isAmountCalculated = True)
                        
                        print("04")

                        offering1.save()
                        print("05")

                        # i.save()

                    else:
                        print(f"You have already got the amount of {i.name}")
                # else:
                #     print(f"{i.name} user has not paid yet")
            print(offering1.pendingAmount,"Pending Amount of tier1")
            print(offering1.monthlyAmount,"Monthly Amount of tier1")

            a = nameMsg.totalAmount
            a +=  offering1.monthlyAmount
            CasignUp.objects.filter(email = request.session['email']).update(totalAmount = a)

# --------------------------------Amount Calculations For Tier1 OLD---------------------------------------------
        if tier1=='96':
            amountHasToBePaid = 0
            for i in obj:
                if i.ispaid == True:
                    if i.isGivenBySir == True:
                        if i.isPaymentRecievedFromSir == False:
                            print("------")
                            amountHasToBePaid += ((10000*offering1.percentage)/100)
                            print("******")
                            # amountHasToBePaid += ((10000*10)/100)
                            offering1.monthlyAmount = amountHasToBePaid
                            offering1.totalAmount += offering1.monthlyAmount

                            # print("77777777")
                            # Offerings.objects.create(CA=nameMsg, monthlyAmount=amountHasToBePaid, totalAmount=offering1.monthlyAmount)
                            # print("11111111")

                            print(f"Your monthly Amount is {offering1.monthlyAmount}")

                            i.isPaymentRecievedFromSir = True
                            print("aaaa")
                            # print(f"You are getting the amount of {i.name}")
                            i.save()
                            offering1.save()
                            print("bbb")
                    else:
                        # print(f"You have already got the amount of {i.name}")
                        print(f"{offering1.monthlyAmount} will be crdite of {i.name} referral")

                    print("cccccc")
                    offering1.totalAmount += offering1.monthlyAmount
                    print("qqqqq")
                    offering1.save()
                    print("wwwwwwwwww")
                else:
                    print(f"{i.name} user has not paid yet")
            print(f"Your Total Amount is {offering1.totalAmount}")

            b = nameMsg.totalAmount
            b +=  offering2.monthlyAmount
            CasignUp.objects.get(email = request.session['email']).update(totalAmount = b)

# --------------------------------Amount Calculations For Tier2---------------------------------------------
        # if tier2:
        #     amountHasToBePaid = 0
        #     for i in obj:
        #         if i.ispaid == True:
        #             if i.isGivenBySir == True:
        #                 amountHasToBePaid += ((10000*offering2.percentage)/100)
        #                 # amountHasToBePaid += ((10000*10)/100)
        #                 # i.isGivenBySir = True
        #                 offering2.monthlyAmount = amountHasToBePaid
        #                 # print(f"You are getting the amount of {i.name}")
        #                 i.save()
        #             else:
        #                 print(f"You have already got the amount of {i.name}")
        #         else:
        #             print(f"{i.name} user has not paid yet")
        #     print(amountHasToBePaid,"Rs Got")

        if tier2:
            offering1.isTierCompleted = True
            offering1.save()
            amountHasToBePaid = 0
            print(offering2.monthlyAmount,"This is the monthly amount of Tier2")
            for i in obj:
                if i.isAmountCalculated == False:
                    if offering2.isGivenBySir == False:
                        amountHasToBePaid += ((10000*offering2.percentage)/100)
                        print("01")
                        offering2.monthlyAmount += amountHasToBePaid
                        print("02")
                        offering2.pendingAmount = offering2.monthlyAmount
                        print("03")
                        # i.isAmountCalculated = True
                        # PrsignUp.objects.filter(recommend_by=nameMsg.email).update(isAmountCalculated = True)
                        PrsignUp.objects.filter(id=i.id).update(isAmountCalculated = True)                        
                        print("04")
                        offering2.save()
                        print("05")
                        # i.save()
                    else:
                        print(f"You have already got the amount of {i.name}")
                # else:
                #     print(f"{i.name} user has not paid yet")
            print(offering2.pendingAmount,"Pending Amount of tier2")
            print(offering2.monthlyAmount,"Monthly Amount of tier2")

            b = nameMsg.totalAmount
            b +=  offering2.monthlyAmount
            CasignUp.objects.filter(email = request.session['email']).update(totalAmount = b)

# --------------------------------Amount Calculations For Tier3---------------------------------------------
        if tier3:
            offering2.isTierCompleted = True
            offering2.save()
            amountHasToBePaid = 0
            for i in obj:
                if i.isAmountCalculated == False:
                    if offering3.isGivenBySir == False:
                        amountHasToBePaid += ((10000*offering3.percentage)/100)
                        print("01")
                        offering3.monthlyAmount += amountHasToBePaid
                        print("02")
                        offering3.pendingAmount = offering3.monthlyAmount
                        print("03")
                        # i.isAmountCalculated = True
                        # PrsignUp.objects.filter(recommend_by=nameMsg.email).update(isAmountCalculated = True)
                        PrsignUp.objects.filter(id=i.id).update(isAmountCalculated = True)                        
                        print("04")
                        offering3.save()
                        print("05")
                        # i.save()
                    else:
                        print(f"You have already got the amount of {i.name}")
                # else:
                #     print(f"{i.name} user has not paid yet")
            print(offering3.pendingAmount,"Pending Amount of tier3")
            print(offering3.monthlyAmount,"Monthly Amount of tier3")

            c = nameMsg.totalAmount
            c +=  offering3.monthlyAmount
            CasignUp.objects.filter(email = request.session['email']).update(totalAmount = c)

# --------------------------------------------------------------------------
    
# ---------------------------------Update Query-----------------------------------------
        # Offerings.objects.filter(CA=nameMsg).update(totalAmount = offering.totalAmount)

        # Offerings.objects.filter(CA=nameMsg).update(totalAmount = amountHasToBePaid)

# -----------------------------------------------------------------------------

        return render(request, 'amount.html', {'key':nameMsg,'amount1': offering1.monthlyAmount,'amount2': offering2.monthlyAmount ,'amount3': offering3.monthlyAmount})
        # except:
        #     print("Inside except of dashboard section")
        #     return render(request, 'amount.html',{'msg':'Something went wrong'})
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
                # nameMsg = PrsignUp.objects.get(email = em)
                # msg = 'User Successfully logged in'
                # print(msg)
                # return render(self, 'prdashboard.html', {'key':nameMsg})
            else:
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')
    return render(self,'prlogin.html')    



# def amount(request, ref_code):
#     try:
#         d=CasignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
#     except:
#         d=PrsignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
#     q1 = PrsignUp.objects.filter(recommend_by = d.name)
#         d.totalNoOfReferrals = len(q1)     
#         for i in q1:
#             if i.ispaid == True:
#                 try:
#                     # d.amount = ((10000*20)/100) * len(q1)
#                     d.amount = ((10000*20)/100) * len(i)
#                     print(d.amount)
#                 except:
#                     pass
#             else:
#                 print(f"{i} user has not paid yet")
#         d.save()

# dashboard for promoter    
def PRdashboard(request):
    if 'email' in request.session:
        print("Inside promoter dashboard")
        try:
            nameMsg = PrsignUp.objects.get(email =  request.session['email'])  
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)
            print(obj)
            due_id = PrsignUp.objects.get(id=nameMsg.id)
            newdate = datetime.today().strftime('%Y-%m-%d')
            if newdate >= str(due_id.payment_due_date):
                z = 'Please pay the payment'
            else:
                z = f'You can use it till {due_id.payment_due_date}'
            return render(request, 'prdashboard.html', {'key':nameMsg,'obj':obj,'len':len(obj), 'time' : z })
        except:
            del request.session['email']
            return redirect('PRLOGIN')
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






