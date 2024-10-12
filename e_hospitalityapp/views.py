from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def home(request):
    return render(request,'home.html')

def userRegistration(request):
    login_table=loginTable()
    userprofile=UserProfile()
    medicalhistory = MedicalHistory()
    medicalinsurance=MedicalInsurance()
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password1']
        date_of_birth=request.POST['date_of_birth']
        diagnosis=request.POST['diagnosis']
        treatment=request.POST['treatment']
        medications=request.POST['medications']
        allergies=request.POST['allergies']
        provider_name = request.POST['provider_name']
        policy_number = request.POST['policy_number']
        expiration_date = request.POST['expiration_date']
        coverage_details = request.POST['coverage_details']

        login_table.username=request.POST['username']
        login_table.password=request.POST['password']
        login_table.password2=request.POST['password1']
        login_table.type='patient'
        if password==password2:
            user = User.objects.create_user(username=username,password=password)

            userprofile.user = user
            userprofile.date_of_birth  = date_of_birth

            medicalhistory.diagnosis = diagnosis
            medicalhistory.treatment = treatment
            medicalhistory.medications = medications
            medicalhistory.allergies = allergies

            medicalhistory.user_profile = userprofile

            medicalinsurance.provider_name=provider_name
            medicalinsurance.policy_number = policy_number
            medicalinsurance.expiration_date = expiration_date
            medicalinsurance.coverage_details = coverage_details

            medicalinsurance.user_profile= userprofile




            userprofile.save()
            medicalhistory.save()
            medicalinsurance.save()
            login_table.save()

            messages.info(request,'Registration success')
            return redirect('login')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
    return render (request,'register.html')

def loginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=loginTable.objects.filter(username=username,password=password,type='user').exists()
        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='patient':
                    request.session['username']=user_name
                    return redirect('patient_view')
                elif type=='admin':
                    request.session['username']=user_name
                    return redirect('admin_view')
                elif type=='doctor':
                    request.session['username'] = user_name
                    return redirect('doctor_view')

            else:
                    messages.error(request,"Invalid username or password")
        except:
            messages.error(request,'invalid role')
    return render(request,'login.html')

def admin_view(request):
    user_name=request.session['username']
    return  render(request,'admin_view.html',{'user_name':user_name})

def patient_view(request):
    user_name = request.session['username']
    return render(request,'patient_view.html',{'user_name':user_name})
def doctor_view(request):
    user_name = request.session['username']
    return render(request,'doctor_view.html',{'user_name':user_name})




def login(request):
    return  render(request,'login.html')
