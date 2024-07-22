from django.urls import path
from playground import views
urlpatterns=[
    path('hello/', views.form),
    path('submit/',views.process_userform),
]