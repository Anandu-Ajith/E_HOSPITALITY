
from django.urls import path,include
from .import views
from .views import DoctorListView, DoctorUpdateView, DoctorDeleteView, patient_profile_detail, \
    get_doctors_by_specialization, appointment_list, patient_appointment_list
from .views import (
    edit_patient_profile,
    edit_medical_history,
    edit_medical_insurance)
from .views import create_appointment


urlpatterns = [
    path("",views.home,name='home'),
    path("register/", views.patientRegistration, name='register'),
    path('login/',views.loginPage,name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('doctor_view/', views.doctor_view, name='doctor_view'),
    path('patient_view/',views.patient_view,name='patient_view'),
    path('logout/',views.logout,name='logout'),
    # path('facilities/',views.facilities,name='facilities'),
    path('appoinments',views.appointment_list,name='appoinments'),
    path('user_list',views.user_list,name='user_list'),
    path('rolebase/',views.rolebase,name='rolebase'),
    path('doctor-register/',views.doctor_registration,name='doctor-register'),
    path('admin-register/',views.admin_registration,name='administration'),
    path('admin_list/', views.admin_list, name='admin_list'),
    path('admin_approve/<int:pk>/', views.admin_approve, name= 'admin_approve'),

    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/edit/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_edit'),
    path('doctors/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),

    path('facilities/', views.facility_list, name='facility-list'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility-detail'),
    path('facilities/new/', views.facility_create, name='facility-create'),
    path('facilities/<int:pk>/edit/', views.facility_update, name='facility-update'),
    path('facilities/<int:pk>/delete/', views.facility_delete, name='facility-delete'),

    path('patient/<int:pk>/', patient_profile_detail, name='patient-profile-detail'),
    path('patient/<int:pk>/edit/', edit_patient_profile, name='edit-patient-profile'),
    path('patient/<int:pk>/medical-history/edit/', edit_medical_history, name='edit-medical-history'),
    path('patient/<int:pk>/medical-insurance/edit/', edit_medical_insurance, name='edit-medical-insurance'),
    path('create_appointment/',create_appointment, name='create_appointment'),
    path('patient_appointments/', patient_appointment_list, name='appointment_list'),
    path('get_doctors/', get_doctors_by_specialization, name='get_doctors_by_specialization'),

    path('appointment/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointment/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),

]
