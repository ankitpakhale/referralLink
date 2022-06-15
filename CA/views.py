from django.shortcuts import render,redirect
from django.http import HttpResponse
from requests import request
from .models import *
from datetime import datetime
import random, string


def genrated_ref_code():
    code = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)))
    return code

# promoter signup
def prSignupView(self):
    new_code = ''
    d = ''
    if self.POST:
        Name = self.POST.get('name')
        Email = self.POST.get('email')
        ref_code = self.POST.get('ref_code')
        Password = self.POST.get('password')
        ConfirmPassword = self.POST.get('confirmPassword')
        try:
            data=PrsignUp.objects.get(email=Email)
            msg = 'Email already taken'
            return render(self , 'prsignup.html',{'msg':msg})
        except:
            if ConfirmPassword == Password:
                v = PrsignUp()
                try:
                    d=PrsignUp.objects.get(ref_code= ref_code)
                    v.recommend_by=d.email
                    print(d.id)
                except:
                    pass
                v.name = Name
                v.email = Email
                v.password = Password
                v.save()
                try:
                    q1 = PrsignUp.objects.filter(recommend_by = d.email)
                    d.totalNoOfReferrals = len(q1)     
                    d.save()
                except:
                    pass
                return redirect('PRLOGIN')
            else:
                msg = 'Enter Same Password'
            return render(self , 'prsignup.html',{'msg':msg},{'ref_code':ref_code})   
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

# pr logout
def prLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('PRLOGIN')    

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
# def MAINDASH(request):
#     li = []
#     caobj =  CasignUp.objects.all()
#     probj =  PrsignUp.objects.all()
#     for i in caobj:
#         caRefCount = PrsignUp.objects.filter(recommend_by = i.email)
#         li.append(len(caRefCount))
#     link  = 'http://127.0.0.1:8000/casignup/j75mnhd67v4m18r'    
#     context = {
#         'caobj': caobj,
#         'probj': probj,        
#         'calen': len(caobj),
#         'prlen': len(probj),
#         'link' : link,
#         'li' : li,
#     }
#     if request.POST:
#         ca_id = request.POST['ca_id']
#         ca_ins = CasignUp.objects.get(email = ca_id)

#         total_amount = ca_ins.totalAmount
#         total_amount += ca_ins.pendingAmount
#         ca_ins = CasignUp.objects.filter(email = ca_id).update(totalAmount = total_amount, pendingAmount = 0)
#         print("Paid to CA Successfully")
#     return render(request, 'maindash.html', context)

