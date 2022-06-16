from django.shortcuts import render,redirect
from django.http import HttpResponse
from requests import request
from .models import *
from datetime import datetime
import random, string


def genrated_ref_code():
    code= str(''.join(random.choices(string.ascii_uppercase + string.digits, k= 12)))
    return code

def make_comp(request):
    if 'email' in request.session:
        if request.POST:
            comp= CompanyDetails(
            owner= PrsignUp.objects.get(email= request.session['email']),
            name= request.POST.get('comp_name'))
            comp.save()
        return redirect('PRDASHBOARD')
    return redirect('PRLOGIN')

# promoter signup
def prSignupView(self):
    d= ''
    if self.POST:
        Name= self.POST.get('name')
        Email= self.POST.get('email')
        ref_code= self.POST.get('ref_code')
        Password= self.POST.get('password')
        ConfirmPassword= self.POST.get('confirmPassword')
        try:
            data=PrsignUp.objects.get(email=Email)
            msg= 'Email already taken'
            return render(self , 'prsignup.html',{'msg':msg})
        except:
            if ConfirmPassword== Password:
                v= PrsignUp()
                try:
                    d= PrsignUp.objects.get(ref_code= ref_code)
                    v.recommend_by=d.email
                except:
                    pass
                v.name= Name
                v.email= Email
                v.password= Password
                v.save()
                return redirect('PRLOGIN')
            else:
                msg= 'Enter Same Password'
            return render(self , 'prsignup.html',{'msg':msg})   
    return render(self,'prsignup.html')
# ----------------------------------------------------------------------------------------------------------
# promoter login
def prlogin(self):
    if self.POST:
        em= self.POST.get('email')
        pass1= self.POST.get('password')
        try:
            print("Inside first try block")
            check= PrsignUp.objects.get(email= em)
            print("Email is ",em,check.email)
            if check.password== pass1:
                self.session['email']= check.email
                return redirect('PRDASHBOARD')
            else:
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')
    return render(self,'prlogin.html')    
# ----------------------------------------------------------------------------------------------------------
# payment page
def payment(request):
    if 'email' in request.session:
        main_key= PrsignUp.objects.get(email= request.session['email'])
        
        # rec_obj= PrsignUp.objects.get(email= main_key.recommend_by)
        # print(rec_obj)
        # print(rec_obj.totalNoOfReferrals)
        # print(type(rec_obj.totalNoOfReferrals))
        # if rec_obj.totalNoOfReferrals <= 1:
        #     print('in fi')
        #     # extend= CompanyDetails.objects.filter(owner= rec_obj)[0]
        #     # extend.comp_due_date= extend.comp_due_date + timedelta(days=30)
        #     # extend.save()
        # else:
        #     msg = "You can get max benifts of 1 referrals only"
        #     print(msg)

        if request.POST:
            if main_key.ispaid== False:
                try:
                    print("in try")
                    rec_obj= PrsignUp.objects.get(email= main_key.recommend_by)
                    print(rec_obj)
                    print(rec_obj.totalNoOfReferrals)

                    if rec_obj.totalNoOfReferrals <= 12:
                        print('in fi')
                        extend= CompanyDetails.objects.filter(owner= rec_obj)[0]
                        extend.comp_due_date= extend.comp_due_date + timedelta(days=30)
                        extend.save()
                    else:
                        msg = "You can get maximum benefits of 12 referrals only"
                        print(msg)

                    PrsignUp.objects.filter(email= rec_obj).update(totalNoOfReferrals= rec_obj.totalNoOfReferrals + 1)
                    msg= 'Paid Successfully'
                    print(msg)
                except:
                    print("in except")
                    pass
                user_given_date= main_key.payment_due_date
                if not main_key.ref_code:
                    PrsignUp.objects.filter(email= request.session['email']).update(ref_code= genrated_ref_code())
                PrsignUp.objects.filter(email= request.session['email']).update(ispaid= True, payment_due_date= user_given_date + timedelta(days= 365))
                return redirect('PRDASHBOARD')                
            else:
                msg= 'You have already paid'
                print(msg)
                return redirect('PRDASHBOARD')                                
    return redirect('PRLOGIN')
# ----------------------------------------------------------------------------------------------------------
# dashboard for promoter    
def PRdashboard(request):
    if 'email' in request.session:
        print("Inside promoter dashboard")
        z= ''
        msg= ''
        main_key= PrsignUp.objects.get(email= request.session['email'])  
        all_comp= CompanyDetails.objects.filter(owner= main_key)
# --------------------------------------------------------------------------------------------------------------------------------
        newdate= datetime.today().strftime('%Y-%m-%d')
        if newdate >= str(main_key.payment_due_date):
            z= 'Please pay the payment'
        else:
            z= f'You can use it till {main_key.payment_due_date}'
# --------------------------------------------------------------------------------------------------------------------------------
#         if request.POST:
#             rec_obj= ''
#             if main_key.ispaid== False:
# # --------------------------------------------------------------------------------------------------------------------------------
#                 try:
#                     rec_obj= main_key.recommend_by
#                     rec_obj= PrsignUp.objects.get(email= rec_obj)
#                     total_referrals= rec_obj.totalNoOfReferrals
#                     # PrsignUp.objects.filter(email= rec_obj).update(totalNoOfReferrals= total_referrals +1)
#                     given_date= rec_obj.payment_due_date
#                     PrsignUp.objects.filter(email= rec_obj).update(payment_due_date= given_date + timedelta(days=30))
#                     msg= 'Paid Successfully'
#                     print(msg)
#                 except:
#                     pass
#                 user_given_date= main_key.payment_due_date
#                 if not main_key.ref_code:
#                     PrsignUp.objects.filter(email= request.session['email']).update(ref_code= genrated_ref_code())
#                 PrsignUp.objects.filter(email= request.session['email']).update(ispaid= True, payment_due_date= user_given_date + timedelta(days=365))
# # --------------------------------------------------------------------------------------------------------------------------------
#             else:
#                 msg= 'You have already paid'
#                 print(msg)
#                 return render(request, 'prdashboard.html', {'all_comp': all_comp, 'key':main_key, 'time' : z , 'msg' : msg})
        # ------------------------------------------------------------------------------------
        return render(request, 'prdashboard.html', {'all_comp': all_comp, 'main_key':main_key, 'time' : z , 'msg' : msg})
    return redirect('PRLOGIN')

# pr logout
def prLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('PRLOGIN')    

# pr timeout
def PRtimeout(request):
    if 'email' in request.session:
        due_id= PrsignUp.objects.get(email=request.session['email'])
        print(due_id, "this is the due_id1")

        # due_id= PrsignUp.objects.get(id=PrsignUp.objects.get(email=request.session['email']).id)
        newdate= datetime.today().strftime('%Y-%m-%d')
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
#     li= []
#     caobj=  CasignUp.objects.all()
#     probj=  PrsignUp.objects.all()
#     for i in caobj:
#         caRefCount= PrsignUp.objects.filter(recommend_by= i.email)
#         li.append(len(caRefCount))
#     link = 'http://127.0.0.1:8000/casignup/j75mnhd67v4m18r'    
#     context= {
#         'caobj': caobj,
#         'probj': probj,        
#         'calen': len(caobj),
#         'prlen': len(probj),
#         'link' : link,
#         'li' : li,
#     }
#     if request.POST:
#         ca_id= request.POST['ca_id']
#         ca_ins= CasignUp.objects.get(email= ca_id)

#         total_amount= ca_ins.totalAmount
#         total_amount += ca_ins.pendingAmount
#         ca_ins= CasignUp.objects.filter(email= ca_id).update(totalAmount= total_amount, pendingAmount= 0)
#         print("Paid to CA Successfully")
#     return render(request, 'maindash.html', context)

