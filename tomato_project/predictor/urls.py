from django.urls import path 
from . import views 
urlpatterns = [ 
    path('', views.home_view, name='home'), 
    path('about/', views.about_view, name='about'), 
    path('contact/', views.contact_view, name='contact'), 
    path('predict/', views.predict_disease, name='predict_disease'), # Must handle POST 
    path('result/', views.show_result, name='show_result'), # Used for result page/Back button 
    path('cause/<str:disease_name>/', views.show_cause, name='show_cause'), 
    path('solution/<str:disease_name>/', views.show_solution, name='show_solution'), 
    path('progress/', views.progress_view, name='progress_view'), 
]