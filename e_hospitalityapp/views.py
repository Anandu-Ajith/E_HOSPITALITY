from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def home(request):
    return render(request,'home.html')

def userRegistration(request):
    login_table=loginTable()
    userprofile=UserProfile()
    if request.method=='POST':
        userprofile.date_of_birth=request.POST['date_of_birth']

        userprofile.username=request.POST['username']
        userprofile.password = request.POST['password']
        userprofile.password2 = request.POST['password1']


        login_table.username=request.POST['username']
        login_table.password=request.POST['password']
        login_table.password2=request.POST['password1']
        login_table.type='patient'
        if request.POST['password']==request.POST['password1']:
            userprofile.save()
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
