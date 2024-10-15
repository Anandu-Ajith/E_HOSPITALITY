import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import DoctorRegistrationForm, SelectDateForm
from .models import *


# Create your views here.
def home(request):
    return render(request, 'home.html')


def patientRegistration(request):
    login_table = loginTable()
    patientprofile = PatientProfile()
    medicalhistory = MedicalHistory()
    medicalinsurance = MedicalInsurance()
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
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
        gender = request.POST['gender']
        age = request.POST['age']
        blood_group = request.POST['blood_group']

        login_table.username = username
        login_table.password = password
        login_table.password2 = password2
        login_table.type = 'patient'
        if password == password2:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = firstname
            user.last_name = lastname

            patientprofile.user = user
            patientprofile.date_of_birth = date_of_birth
            patientprofile.blood_group = blood_group
            patientprofile.gender = gender
            patientprofile.age = age

            medicalhistory.diagnosis = diagnosis
            medicalhistory.treatment = treatment
            medicalhistory.medications = medications
            medicalhistory.allergies = allergies

            medicalhistory.user_profile = patientprofile

            medicalinsurance.provider_name = provider_name
            medicalinsurance.policy_number = policy_number
            medicalinsurance.expiration_date = expiration_date
            medicalinsurance.coverage_details = coverage_details

            medicalinsurance.user_profile = patientprofile

            user.save()
            patientprofile.save()
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
        user = authenticate(request, username=username, password=password)
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
            login(request,user)
            try:
                # Fetch user role from loginTable, but without checking plaintext password
                user_details = loginTable.objects.get(username=username)
                user_name = user_details.username
                user_type = user_details.type

                if user_type == 'patient':
                    request.session['username'] = user_name
                    patient = PatientProfile.objects.get(user__username=username)
                    medical_insurance = get_object_or_404(MedicalInsurance, user_profile=patient)

                    # Pass the data to the template
                    context = {
                        'patient_profile': patient,
                        'medical_insurance': medical_insurance,
                    }

                    return render(request, 'patient_profile_detail.html', context)
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


def logout_view(request):
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


from django.db import transaction
from .forms import AdminRegistrationForm


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

        admin.is_approved = True
        admin.save()

        messages.success(request, 'Administrator approved successfully!')

    return redirect('admin_list')

def doctor_approve(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    login_table = loginTable()
    if request.method == 'POST':
        login_table.username = doctor.user.username
        login_table.password = doctor.user.password
        login_table.password2 = doctor.user.password
        login_table.type = 'doctor'

        doctor.is_approved = True
        doctor.save()

        login_table.save()

        messages.success(request, 'Doctor approved successfully!')

    return redirect('doctor_list')


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

from django.http import HttpResponseRedirect
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


# views.py


def patient_profile_detail(request, pk):
    # Get the patient profile using the primary key (pk)
    patient_profile = get_object_or_404(PatientProfile, pk=pk)

    # Get the related medical history and medical insurance
    # medical_history = get_object_or_404(MedicalHistory, user_profile=patient_profile)
    medical_insurance = get_object_or_404(MedicalInsurance, user_profile=patient_profile)

    # Pass the data to the template
    context = {
        'patient':patient_profile,
        'patient_profile': patient_profile,
        # 'medical_history': medical_history,
        'medical_insurance': medical_insurance,
    }

    return render(request, 'patient_profile_detail.html', context)


# views.py
from .models import PatientProfile, MedicalHistory, MedicalInsurance
from .forms import PatientProfileForm, MedicalHistoryForm, MedicalInsuranceForm


# Edit Patient Profile
def edit_patient_profile(request, pk):
    patient_profile = get_object_or_404(PatientProfile, pk=pk)
    user = patient_profile.user  # Get the associated user

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient_profile, user=user)

        if form.is_valid():
            # Update the User model first
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Now update the PatientProfile model
            form.save()
            return redirect('patient-profile-detail', pk=pk)
    else:
        form = PatientProfileForm(instance=patient_profile, user=user)

    return render(request, 'edit_patient_profile.html', {'form': form})


# Edit Medical History
def edit_medical_history(request, pk):
    medical_history = get_object_or_404(MedicalHistory, user_profile__pk=pk)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=medical_history)
        if form.is_valid():
            form.save()
            return redirect('patient-profile-detail', pk=pk)
    else:
        form = MedicalHistoryForm(instance=medical_history)

    return render(request, 'edit_medical_history.html', {'form': form})


# Edit Medical Insurance
def edit_medical_insurance(request, pk):
    medical_insurance = get_object_or_404(MedicalInsurance, user_profile__pk=pk)

    if request.method == 'POST':
        form = MedicalInsuranceForm(request.POST, instance=medical_insurance)
        if form.is_valid():
            form.save()
            return redirect('patient-profile-detail', pk=pk)
    else:
        form = MedicalInsuranceForm(instance=medical_insurance)

    return render(request, 'edit_medical_insurance.html', {'form': form})


from .models import DoctorProfile


def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to a success page
        else:
            print(form.errors)
            print("Submitted data:", request.POST)
    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form})


from django.http import JsonResponse


def get_doctors_by_specialization(request):
    specialization = request.GET.get('specialization')
    doctors = DoctorProfile.objects.filter(specialization=specialization).values('id', 'user__first_name',
                                                                                 'user__last_name')
    return JsonResponse(list(doctors), safe=False)


from .forms import AppointmentForm


def edit_appointment(request, appointment_id):
    # Get the existing appointment object or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Form submitted with data
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            # Redirect to a success page or the list of appointments
            return redirect(reverse('appointment_list'))  # Adjust the URL name based on your project
    else:
        # GET request, load the form with the existing appointment data
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Appointment


def delete_appointment(request, appointment_id):
    # Get the appointment object or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # When the user confirms the deletion, delete the appointment
        appointment.delete()
        # Redirect to the list of appointments or a success page
        return redirect(reverse('appointment_list'))  # Adjust the URL name based on your project

    # Render a confirmation page before deleting
    return render(request, 'delete_appointment.html', {'appointment': appointment})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appoinments.html', {'appointments': appointments})


def patient_appointment_list(request,pk):
    selected_date = request.GET.get('date')
    appointments = []

    if selected_date:
        appointments = Appointment.objects.filter(appointment_date=selected_date)

    # If no date is selected, you can set the default to today or leave it empty
    if not selected_date:
        selected_date = timezone.now().date()

    patient = PatientProfile.objects.get(pk=pk)

    context = {
        'patient_profile':patient,
        'appointments': appointments,
        'selected_date': selected_date,
    }
    return render(request, 'patient_appointment_list.html', context)


# def create_checkout_session(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#
#     if request.method == 'POST':
#         line_item = {
#             'price_data': {
#                 'currency': 'USD',
#                 'unit_amount': 100,
#                 'product_data': {
#                     'name': ''
#                 },
#                 'quantity': 1
#             }
#         }
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[line_item],
#             mode='payment',
#             success_url=request.build_absolute_url(reverse('success')),
#             cancel_url=request.build_absolute_url(reverse('cancel'))
#         )
#         return redirect(checkout_session.url, code=303)

def create_stripe_payment(request, appointment_id):
        # Get the appointment details
        stripe.api_key = settings.STRIPE_SECRET_KEY
        appointment = get_object_or_404(PatientAppointment, id=appointment_id)

        if request.method == "POST":
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Appointment with Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name}',
                        },
                        'unit_amount': 5000,  # Amount in cents ($50.00)
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/') + f'?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=request.build_absolute_uri('/payment-cancel/'),
                metadata={  # Add appointment_id to the metadata
                    'appointment_id': appointment.id
                },
            )
            return redirect(session.url, code=303)

        return render(request, 'payment_form.html', {
            'appointment': appointment,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })


def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)

        appointment_id = session.metadata.get('appointment_id')
        appointment = get_object_or_404(PatientAppointment, id=appointment_id)

        if session.payment_status == 'paid':
            appointment.is_payment_done = True
            appointment.save()

            payment = Payment.objects.create(
                appointment=appointment,
                amount=session.amount_total / 100,
                stripe_charge_id=session.payment_intent,
            )

            payment.save()

            return redirect('display_appointments', patient_id=appointment.patient.pk)

    return render(request, 'payment_failed.html')

@login_required
def create_patient_appointment(request, appointment_id):
    # Get the logged-in patient's profile
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    print(patient_profile)
    # Get the selected doctor by doctor_id
    appointment_schedule = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == "POST":
        appoinment = PatientAppointment()
        appoinment.patient = patient_profile
        appoinment.doctor = appointment_schedule.doctor
        appoinment.appointment_date = appointment_schedule.appointment_date
        appoinment.appointment_time_from = appointment_schedule.appointment_time_from
        appoinment.appointment_time_to = appointment_schedule.appointment_time_to
        appoinment.save()

            # Redirect to payment page or another step
        return redirect('create_stripe_payment', appointment_id=appoinment.pk)

    return render(request, 'create_patient_appointment.html', {
        'doctor': appointment_schedule.doctor,
        'patient_profile': patient_profile,
        'appointment_schedule':appointment_schedule
    })

def display_appointments(request, patient_id):
    appointments = PatientAppointment.objects.filter(patient_id=patient_id)
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    return render(request, 'display.html', {'appointments': appointments,
                                            'patient_profile': patient_profile,
                                            })

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(PatientAppointment, id=appointment_id)
    appointment.delete()
    return HttpResponseRedirect(reverse('display_appointments', args=[appointment.patient_id]))


def reschedule_appointment(request, appointment_id):
    patient_appointment = get_object_or_404(PatientAppointment, id=appointment_id)

    if request.method == 'POST':
        form = SelectDateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['appointment_date']

            # Fetch available appointments for the doctor on the selected date
            available_appointments = Appointment.objects.filter(
                doctor=patient_appointment.doctor,
                appointment_date=selected_date
            )

            return render(request, 'available_slots.html', {
                'available_appointments': available_appointments,
                'patient_appointment': patient_appointment
            })
    else:
        form = SelectDateForm()

    return render(request, 'select_date.html', {'form': form})


def confirm_reschedule_appointment(request, appointment_id, new_appointment_id):
    patient_appointment = get_object_or_404(PatientAppointment, id=appointment_id)
    new_appointment = get_object_or_404(Appointment, id=new_appointment_id)

    # Update the patient appointment with the new date and time
    patient_appointment.appointment_date = new_appointment.appointment_date
    patient_appointment.appointment_time_from = new_appointment.appointment_time_from
    patient_appointment.appointment_time_to = new_appointment.appointment_time_to
    patient_appointment.save()

    return redirect('display_appointments', patient_id=patient_appointment.patient.id)

def medical_history_list(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    histories = MedicalHistory.objects.filter(user_profile=patient)
    return render(request, 'medical_history_list.html', {'patient_profile': patient, 'histories': histories})


def create_medical_history(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.user_profile = patient
            medical_history.save()
            return redirect('medical_history_list', patient_id=patient.id)
    else:
        form = MedicalHistoryForm()

    return render(request, 'medical_history_form.html', {'form': form, 'patient_profile': patient})


def edit_medical_history(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            return redirect('medical_history_list', patient_id=history.user_profile.id)
    else:
        form = MedicalHistoryForm(instance=history)

    return render(request, 'medical_history_form.html', {'form': form, 'patient_profile': history.user_profile})

def delete_medical_history(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)
    patient_id = history.user_profile.id
    history.delete()
    return HttpResponseRedirect(reverse('medical_history_list', args=[patient_id]))


def payment_details_for_patient(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)

    # Get all appointments for the patient
    appointments = PatientAppointment.objects.filter(patient=patient)

    # Get all payments associated with the patient's appointments
    payments = Payment.objects.filter(appointment__in=appointments)

    return render(request, 'payment_list.html', {
        'patient_profile': patient,
        'payments': payments
    })