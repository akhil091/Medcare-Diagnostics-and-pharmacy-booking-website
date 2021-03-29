from django.urls import path
from Doctors import views


urlpatterns = [
    path('doctor', views.DoctorDetialView.as_view()),
    path('doctor/<int:id>', views.GetDoctorView.as_view()),
    path('doctor/filter', views.Doc_FilterView.as_view()),
    path('doctor/specialization',views.SpecializationView.as_view()),
    path('doctor/condition',views.ConditionView.as_view()),
    path('doctors/',views.doctorpage),
    path('doctordetails/<int:id>',views.doctorprofile),
    path('conditions/<int:id>',views.conditiondoctors),
    path('specializations/<int:id>',views.specialitydoctors),
]
