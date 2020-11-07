from django.urls import path
from . import views
urlpatterns = [
	
    path('djangosearch/', views.djangosearch, name = 'djangosearch'),	
    path('django/<int:developmentcategorey>/', views.django, name = 'developmentcategorey_django'),
	path('django/', views.django, name = 'django'),
	path('developmentcategorey/', views.developmentcategorey, name='developmentcategorey'),
	path('postdetails/<slug:slug>', views.postdetails, name='postdetails'),
	
]