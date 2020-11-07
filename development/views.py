from django.shortcuts import render
from django.db.models import Count, Q
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Author
from django.http import HttpResponse, request
from .models import DevelopmentPost, DevelopView
from django.db import models
# Create your views here.

def get_developmentcategorey_count():
	queryset3 = DevelopmentPost.objects.values('development_categories__id', 'development_categories__title').annotate(Count('development_categories__title'))

	return queryset3
def developmentcategorey(request):
	most_recent = DevelopmentPost.objects.order_by('-timestamp')[:4]
	developmentcategorey_count = get_developmentcategorey_count()

	queryset3 = DevelopmentPost.objects.order_by('development_categories')
	query = request.GET.get('q')
	if query:
		queryset3 = queryset3.filter(
			Q(title__icontains = query)
		).distinct()

	context = {

		'queryset3': queryset3,
		'most_recent': most_recent,
		'developmentcategorey_count': developmentcategorey_count
	}
	return render(request, 'develop/developmentcategorey.html', context)




def django(request, developmentcategorey = None):

	developmentcategorey_count = get_developmentcategorey_count()
	most_recent = DevelopmentPost.objects.order_by('-timestamp')[:4]
	if developmentcategorey is None:
		post_list = DevelopmentPost.objects.all()
	else:
		post_list = DevelopmentPost.objects.filter(development_categories = developmentcategorey)

	paginator = Paginator(post_list, 6)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset3 = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset3 = paginator.page(1)
	except EmptyPage:
		paginated_queryset3 = paginator.page(paginator.num_pages)

	context = {
		'post_list': post_list,
		'queryset3': paginated_queryset3,
		'most_recent': most_recent,
		'page_request_var': page_request_var,
		'developmentcategorey_count': developmentcategorey_count,
		
	}
	
	return render(request, 'develop/django.html',context)


    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def postdetails(request,slug): # post er alter a gadgetdetails
	
	developmentcategorey_count = get_developmentcategorey_count()
	#view_count = get_view_count()
	most_recent = DevelopmentPost.objects.order_by('-timestamp')[:4]
	developmentpost = DevelopmentPost.objects.filter(slug=slug)
	if developmentpost.exists():
		developmentpost = developmentpost.first()
	else:
		HttpResponse("<h3>page not found</h3>")
	#seo

	context = {
		#'postview':postview,
		#'view_count': view_count,
		'developmentpost': developmentpost,
		'most_recent': most_recent,
		'developmentcategorey_count': developmentcategorey_count,
		
	}
	return render(request, 'develop/postdetails.html', context)



def djangosearch(request):
	most_recent = DevelopmentPost.objects.order_by('-timestamp')[:4]
	developmentcategorey_count = get_developmentcategorey_count()
	queryset3 = DevelopmentPost.objects.all()
	query = request.GET.get('q')

	if query:
		queryset3 = queryset3.filter(
			Q(title__icontains = query)

		).distinct()

		
	paginator = Paginator(queryset3, 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset3 = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset3 = paginator.page(1)
	except EmptyPage:
		paginated_queryset3 = paginator.page(paginator.num_pages)
	context = {
		'queryset3': queryset3,
		'most_recent': most_recent,
		'developmentcategorey_count': developmentcategorey_count,
		'page_request_var': page_request_var,
		'queryset3': paginated_queryset3,

	}
	return render(request, 'develop/django_search.html', context)
# here is code for 
