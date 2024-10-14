
from django.urls import path,include
from .import views
from .views import DoctorListView, DoctorUpdateView, DoctorDeleteView

urlpatterns = [
    path("",views.home,name='home'),
    path("register/", views.patientRegistration, name='register'),
    path('login/',views.loginPage,name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('doctor_view/', views.doctor_view, name='doctor_view'),
    path('patient_view/',views.patient_view,name='patient_view'),
    path('logout/',views.logout,name='logout'),
    # path('facilities/',views.facilities,name='facilities'),
    path('appoinments',views.appoinments,name='appoinments'),
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
    path('facilities/<int:pk>/delete/', views.facility_delete, name='facility-delete')

]
