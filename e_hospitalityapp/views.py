from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DoctorRegistrationForm
from .models import *


# Create your views here.
def home(request):
    return render(request, 'home.html')


def patientRegistration(request):
    login_table = loginTable()
    userprofile = PatientProfile()
    medicalhistory = MedicalHistory()
    medicalinsurance = MedicalInsurance()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password1']
        date_of_birth = request.POST['date_of_birth']
        diagnosis = request.POST['diagnosis']
        treatment = request.POST['treatment']
        medications = request.POST['medications']
        allergies = request.POST['allergies']
        provider_name = request.POST['provider_name']
        policy_number = request.POST['policy_number']
        expiration_date = request.POST['expiration_date']
        coverage_details = request.POST['coverage_details']

        login_table.username = request.POST['username']
        login_table.password = request.POST['password']
        login_table.password2 = request.POST['password1']
        login_table.type = 'patient'
        if password == password2:
            user = User.objects.create_user(username=username, password=password)

            userprofile.user = user
            userprofile.date_of_birth = date_of_birth

            medicalhistory.diagnosis = diagnosis
            medicalhistory.treatment = treatment
            medicalhistory.medications = medications
            medicalhistory.allergies = allergies

            medicalhistory.user_profile = userprofile

            medicalinsurance.provider_name = provider_name
            medicalinsurance.policy_number = policy_number
            medicalinsurance.expiration_date = expiration_date
            medicalinsurance.coverage_details = coverage_details

            medicalinsurance.user_profile = userprofile

            userprofile.save()
            medicalhistory.save()
            medicalinsurance.save()
            login_table.save()

            messages.info(request, 'Registration success')
            return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    return render(request, 'register.html')


def doctor_registration(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():

            # Save the user part of the form
            user = User.objects.create_user(username=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])

            # Now, create the doctor object with additional fields
            doctor = DoctorProfile.objects.create(
                user=user,
                specialization=form.cleaned_data['specialization'],
                experience=form.cleaned_data['experience'],
                license_number=form.cleaned_data['license_number'],
                profile_picture=form.cleaned_data.get('profile_picture')
            )

            user.save()
            doctor.save()

            return redirect('home')  # Redirect to a success page
        else:
            print(form.errors)
    else:
        form = DoctorRegistrationForm()

    return render(request, 'doctor_registration2.html', {'form': form})


def loginPage1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        try:
            if user is not None:
                user_details = loginTable.objects.get(username=username, password=password)
                user_name = user_details.username
                type = user_details.type

                if type == 'patient':
                    request.session['username'] = user_name
                    return redirect('patient_view')
                elif type == 'admin':
                    request.session['username'] = user_name
                    return redirect('admin_view')
                elif type == 'doctor':
                    request.session['username'] = user_name
                    return redirect('doctor_view')

            else:
                messages.error(request, "Invalid username or password")
        except:
            messages.error(request, 'invalid role')
    return render(request, 'login.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                # Fetch user role from loginTable, but without checking plaintext password
                user_details = loginTable.objects.get(username=username)
                user_name = user_details.username
                user_type = user_details.type

                if user_type == 'patient':
                    request.session['username'] = user_name
                    return redirect('patient_view')
                elif user_type == 'admin':
                    request.session['username'] = user_name
                    return redirect('admin_list')
                elif user_type == 'doctor':
                    request.session['username'] = user_name
                    return redirect('doctor_view')

            except loginTable.DoesNotExist:
                messages.error(request, 'User role not found.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def admin_view(request):
    user_name = request.session['username']
    return render(request, 'admin_view.html', {'user_name': user_name})


def patient_view(request):
    user_name = request.session['username']
    return render(request, 'patient_view.html', {'user_name': user_name})


def doctor_view(request):
    user_name = request.session['username']
    return render(request, 'doctor_view.html', {'user_name': user_name})


def login(request):
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('login')


def facilities(request):
    return render(request, 'facilities.html')


def appoinments(request):
    return render(request, 'appoinments.html')


def user_list(request):
    # user = User()
    # if request.method=='POST':

    return render(request, 'user_list.html')


def rolebase(request):
    return render(request, 'rolebase.html')


def doctor_registration2(request):
    return render(request, 'doctor_registration.html')


from django.shortcuts import render, redirect
from django.db import transaction
from .forms import AdminRegistrationForm
from .models import Administrator
from django.contrib.auth.models import User


def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user part of the form
                    user = form.save()

                    # Now, create the administrator object with additional fields
                    admin = Administrator.objects.create(
                        user=user,
                        department=form.cleaned_data['department'],
                        position=form.cleaned_data['position'],
                        employee_id=form.cleaned_data['employee_id'],
                        date_of_joining=form.cleaned_data['date_of_joining'],
                        profile_picture=form.cleaned_data.get('profile_picture'),
                        address_line1=form.cleaned_data['address_line1'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        postal_code=form.cleaned_data['postal_code'],
                        country=form.cleaned_data['country']
                    )
                    admin.save()

                return redirect('home')  # Redirect to a success page
            except Exception as e:
                form.add_error(None, "An error occurred while saving. Please try again.")
                print(f"Error: {e}")  # For debugging purposes
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin_registration.html', {'form': form})


from django.shortcuts import render
from .models import Administrator


def admin_list(request):
    # Fetch all administrators
    administrators = Administrator.objects.all()

    # Pass the list to the template
    context = {
        'administrators': administrators
    }

    return render(request, 'admin_list.html', context)


def admin_edit(request, pk):
    admin = get_object_or_404(Administrator, pk=pk)

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, request.FILES, instance=admin.user)
        if form.is_valid():
            form.save()
            admin.department = form.cleaned_data['department']
            admin.position = form.cleaned_data['position']
            admin.employee_id = form.cleaned_data['employee_id']
            admin.date_of_joining = form.cleaned_data['date_of_joining']
            admin.profile_picture = form.cleaned_data.get('profile_picture')
            admin.save()
            messages.success(request, 'Administrator updated successfully!')
            return redirect('admin_list')
    else:
        form = AdminRegistrationForm(instance=admin.user)

    return render(request, 'admin_edit.html', {'form': form, 'admin': admin})


# View to delete an administrator
def admin_delete(request, pk):
    admin = get_object_or_404(Administrator, pk=pk)

    if request.method == 'POST':
        admin.user.delete()  # This will also delete the related user
        messages.success(request, 'Administrator deleted successfully!')
        return redirect('admin_list')

    return render(request, 'admin_confirm_delete.html', {'admin': admin})


def admin_approve(request, pk):
    admin = get_object_or_404(Administrator, pk=pk)
    login_table = loginTable()
    if request.method == 'POST':
        login_table.username = admin.user.username
        login_table.password = admin.user.password
        login_table.password2 = admin.user.password
        login_table.type = 'admin'

        login_table.save()

        messages.success(request, 'Administrator approved successfully!')

    return redirect('admin_list')




from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.models import User

class DoctorListView(ListView):
        model = DoctorProfile
        template_name = 'doctor_list.html'
        context_object_name = 'doctors'

    # You can add update and delete views as well
class DoctorUpdateView(UpdateView):
        model = DoctorProfile
        fields = ['specialization']  # Fields you want to allow updating
        template_name = 'doctor_edit.html'
        success_url = reverse_lazy('doctor_list')

class DoctorDeleteView(DeleteView):
        model = DoctorProfile
        template_name = 'doctor_confirm_delete.html'
        success_url = reverse_lazy('doctor_list')




# facility/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Facility
from .forms import FacilityForm

# List all facilities
def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'facility_list.html', {'facilities': facilities})

# View details of a specific facility
def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    return render(request, 'facility_detail.html', {'facility': facility})

# Create a new facility
def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('facility-list'))
    else:
        form = FacilityForm()
    return render(request, 'facility_form.html', {'form': form})

# Update an existing facility
def facility_update(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('facility-list'))
    else:
        form = FacilityForm(instance=facility)
    return render(request, 'facility_form.html', {'form': form})

# Delete a facility
def facility_delete(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == 'POST':
        facility.delete()
        return redirect('facility-list')
    return render(request, 'facility_confirm_delete.html', {'facility': facility})
