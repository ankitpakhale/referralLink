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
        try:
            data=CasignUp.objects.filter(email=Email)
            if data:
                msg = 'Email already taken'
                return render(self , 'signup.html',{'msg':msg})

            elif ConfirmPassword == Password:
                v = CasignUp(name = Name, email = Email, number = Number, password = Password, confirmPassword = ConfirmPassword)
                # v.percentage = '10%'
                v.save()
                return redirect('CALOGIN')

            else:
                msg = 'Enter Same Password'
                return render(self , 'signup.html',{'msg':msg}) 
                
        finally:
            messages.success(self, 'Signup Successfully Done...')

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
        print("Inside dashboard")
        try:
            nameMsg = CasignUp.objects.get(email = request.session['email'])

            obj=PrsignUp.objects.filter(recommend_by=nameMsg.name)
            print(obj)

            due_id = CasignUp.objects.get(id=nameMsg.id)
            newdate = datetime.today().strftime('%Y-%m-%d')
            print("This is new date", newdate)
            print("This is due date",str(due_id.payment_due_date))
            if newdate >= str(due_id.payment_due_date):
                z = 'Please pay the payment'
            else:
                z = f'You can use it till {due_id.payment_due_date}'

            return render(request, 'dashboard.html', {'key':nameMsg,'obj':obj,'len':len(obj), 'time' : z })
       
        except:
            del request.session['email']
            return redirect('CALOGIN')
        
        
        # l=[]
        # for i in obj:
        #     obj1=PrsignUp.objects.filter(recommend_by=i.name)  
        #     l.append(obj1)
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
                v.recommend_by=d.name
                v.save()
            # --------------------------------------------------------------------------------
                q1 = PrsignUp.objects.filter(recommend_by = d.name)
                d.totalNoOfReferrals = len(q1)     
                for i in q1:
                    if i.ispaid == True:
                        try:
                            d.amount = ((10000*20)/100) * len(q1)
                            print(d.amount)
                        except:
                            pass
                    else:
                        print(f"{i} user has not paid yet")
                d.save()

            # --------------------------------------------------------------------------------
                # q1 = PrsignUp.objects.filter(recommend_by = d.name)                
                # k = CasignUp()
                # if q1:
                #     k.subuser = d
                #     k.save()

                # return redirect('PRLOGIN',ref_code)
                return redirect('PRLOGIN')

            else:
                msg = 'Enter Same Password'
                return render(self , 'prsignup.html',{'msg':msg},{'ref_code':ref_code}) 
                
        finally:
            messages.success(self, 'Signup Successfully Done...')

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

# dashboard for promoter    
def PRdashboard(request):
    if 'email' in request.session:
        print("Inside promoter dashboard")
        try:
            nameMsg = PrsignUp.objects.get(email =  request.session['email'])  
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.name)
            print(obj)

            due_id = PrsignUp.objects.get(id=nameMsg.id)
            newdate = datetime.today().strftime('%Y-%m-%d')
            print("This is new date", newdate)
            print("This is due date",str(due_id.payment_due_date))
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
        
        due_id = PrsignUp.objects.get(id=PrsignUp.objects.get(email=request.session['email']).id)
        # due_id = PrsignUp.objects.get(id=PrsignUp.objects.get(email=request.session['email']).id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        print("This is new date", newdate)
        print("This is due date",str(due_id.payment_due_date))
        if newdate >= str(due_id.payment_due_date):
            return HttpResponse('Please pay the payment')
        else:
            print(f'You can use it till {due_id.payment_due_date}')
            return HttpResponse(f'You can use it till {due_id.payment_due_date}')
    return redirect('PRLOGIN')

# Dashboard for main Host
def MAINDASH(request):
    li = []
    caobj =  CasignUp.objects.all()

    for i in caobj:
        caRefCount = PrsignUp.objects.filter(recommend_by = i.name)
        counters = 0
        for j in caRefCount:
            counters += 1
        li.append(counters)

    probj =  PrsignUp.objects.all()
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






