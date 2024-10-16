
from django.urls import path,include
from .import views
from .views import DoctorListView, DoctorUpdateView, DoctorDeleteView, patient_profile_detail, \
    get_doctors_by_specialization, appointment_list, patient_appointment_list, payment_cancel
from .views import (
    edit_patient_profile,
    edit_medical_history,
    edit_medical_insurance)
from .views import create_appointment


urlpatterns = [
    path("",views.home,name='home'),
    path("register/", views.patientRegistration, name='register'),
    path('login/',views.loginPage,name='login'),
    path('health/',views.health,name='health'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('doctor_view/', views.doctor_view, name='doctor_view'),
    path('patient_view/',views.patient_view,name='patient_view'),
    path('logout/',views.logout_view,name='logout'),
    # path('facilities/',views.facilities,name='facilities'),
    path('appoinments',views.appointment_list,name='appoinments'),
    path('user_list',views.user_list,name='user_list'),
    path('rolebase/',views.rolebase,name='rolebase'),
    path('doctor-register/',views.doctor_registration,name='doctor-register'),
    path('admin-register/',views.admin_registration,name='administration'),
    path('admin_list/', views.admin_list, name='admin_list'),
    path('admin_approve/<int:pk>/', views.admin_approve, name= 'admin_approve'),
    path('doctor_approve/<int:pk>/', views.doctor_approve, name='doctor_approve'),

    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/edit/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),

    path('facilities/', views.facility_list, name='facility-list'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility-detail'),
    path('facilities/new/', views.facility_create, name='facility-create'),
    path('facilities/<int:pk>/edit/', views.facility_update, name='facility-update'),
    path('facilities/<int:pk>/delete/', views.facility_delete, name='facility-delete'),

    path('patient/<int:pk>/', patient_profile_detail, name='patient_profile_detail'),
    path('patient/<int:pk>/edit/', edit_patient_profile, name='edit-patient-profile'),
    path('patient/<int:pk>/medical-history/edit/', edit_medical_history, name='edit-medical-history'),
    path('patient/<int:pk>/medical-insurance/edit/', edit_medical_insurance, name='edit-medical-insurance'),
    path('create_appointment/',create_appointment, name='create_appointment'),
    path('patient_appointments/<int:pk>/', patient_appointment_list, name='appointment_list'),
    path('get_doctors/', get_doctors_by_specialization, name='get_doctors_by_specialization'),

    path('appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointment/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointment/<int:appointment_id>/pay/', views.create_stripe_payment, name='create_stripe_payment'),
    path('create-appointment/<int:appointment_id>/', views.create_patient_appointment, name='create_patient_appointment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('appointments/<int:patient_id>/', views.display_appointments, name='display_appointments'),
    path('appointments/<int:appointment_id>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointments/<int:appointment_id>/reschedule/<int:new_appointment_id>/confirm/', views.confirm_reschedule_appointment, name='confirm_reschedule_appointment'),

    path('patients/<int:patient_id>/medical-history/', views.medical_history_list, name='medical_history_list'),
    path('patients/<int:patient_id>/medical-history/create/', views.create_medical_history, name='create_medical_history'),
    path('medical-history/<int:history_id>/edit/', views.edit_medical_history, name='edit_medical_history'),
    path('medical-history/<int:history_id>/delete/', views.delete_medical_history, name='delete_medical_history'),
    path('patients/<int:patient_id>/payments/', views.payment_details_for_patient, name='payment_details_for_patient'),

    path('patients/', views.patient_list, name='patient_list'),
    path('doctor/<int:doctor_id>/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('appointment/<int:appointment_id>/patients/', views.patient_list_for_appointment, name='patient_list_for_appointment'),

    path('prescription/add/<int:pk>', views.create_prescription, name='prescription-add'),
    path('prescription/<int:pk>/edit/', views.edit_prescription, name='prescription-edit'),
    path('prescription/<int:pk>/', views.view_prescription, name='prescription-detail'),
    path('prescription/<int:pk>/delete/', views.delete_prescription, name='prescription-delete'),
    path('patient/<int:patient_id>/prescriptions/', views.view_patient_prescriptions, name='patient-prescriptions'),
    path('admin-edit/<int:pk>/', views.admin_edit, name='admin_edit'),
    path('admin-delete/<int:pk>/', views.admin_delete, name='admin_delete'),
    path('payment-cancel/<int:patient_id>', payment_cancel, name='payment_cancel'),

]
