import email
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime
# Create your views here.

# CA signup form
def SignupView(self, ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']

        created_by = self.POST['created_by']

        tier1 = self.POST['tier1']
        tier2 = self.POST['tier2']
        tier3 = self.POST['tier3']

        percentage1 = self.POST['percentage1']
        percentage2 = self.POST['percentage2']
        percentage3 = self.POST['percentage3']

        try:
            data=CasignUp.objects.get(email=Email)
            msg = 'Email already taken'
            return render(self , 'signup.html',{'msg':msg})
        except:
            if ConfirmPassword == Password:
                CasignUp.objects.create(name = Name, email = Email, number = Number, password = Password, confirmPassword = ConfirmPassword, percentage = 10)
                data=CasignUp.objects.get(email=Email)
                
                Offerings.objects.create(
                    CA = data,
                    created_by = created_by,
                    payment_date = datetime.today(),
                    tier1 = tier1,
                    tier2 = tier2,
                    tier3 = tier3,
                    percentage1 = percentage1,
                    percentage2 = percentage2,
                    percentage3 = percentage3,
                )
                
                
                return redirect('CALOGIN')

            else:
                msg = 'Enter Same Password'
                return render(self, 'signup.html',{'msg':msg}) 
                    
        # except:
        #     msg = 'Invalid Email Address'
        #     return render(self, 'signup.html',{'msg':msg}) 

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
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')

    return render(self,'login.html')

#ca dashboard
def dashboard(request):
    if 'email' in request.session:
        try:
            # nameMsg = logged in user's email
            nameMsg = CasignUp.objects.get(email = request.session['email'])
            print(nameMsg.link,"This is the referral link")
            # obj = giving queryset of all promoter's data
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)
            newdate = datetime.today().strftime('%Y-%m-%d')
            
            amountHasToBePaid = 0
            for i in obj:
                if i.ispaid == True:
                    amountHasToBePaid += ((10000*20)/100)
                else:
                    print(f"{i} user has not paid yet")
            CasignUp.objects.filter(email = request.session['email']).update(amount = amountHasToBePaid)

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






