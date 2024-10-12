
from django.urls import path,include
from .import views
urlpatterns = [
    path("",views.home,name='home'),
    path("register/",views.userRegistration,name='register'),
    path('login/',views.loginPage,name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('doctor_view/', views.doctor_view, name='doctor_view'),
    path('patient_view/',views.patient_view,name='patient_view')

]
