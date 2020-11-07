from django.shortcuts import render
from django.db.models import Count, Q
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Author
from django.http import HttpResponse, request
from .models import LinuxPost, LinuxPostView, LinuxCategorey
from django.db import models
# Create your views here.
def get_linuxcategorey_count():
	queryset2 = LinuxPost.objects.values('linuxcategories__id', 'linuxcategories__title').annotate(Count('linuxcategories__title'))

	return queryset2


def linuxcategorey(request):
	most_recent = LinuxPost.objects.order_by('-timestamp')[:4]
	linuxcategorey_count = get_linuxcategorey_count()

	queryset2 = LinuxPost.objects.order_by('linuxcategories')
	query = request.GET.get('q')
	if query:
		queryset2 = queryset2.filter(
			Q(title__icontains = query)
		).distinct()

	context = {

		'queryset2': queryset2,
		'most_recent': most_recent,
		'linuxcategorey_count': linuxcategorey_count
	}
	return render(request, 'linux/linuxcategorey.html', context)



def linuxpost(request, linuxcategorey = None):

	linuxcategorey_count = get_linuxcategorey_count()
	most_recent = LinuxPost.objects.order_by('-timestamp')[:4]
	if linuxcategorey is None:
		post_list = LinuxPost.objects.all()
	else:
		post_list = LinuxPost.objects.filter(linuxcategories = linuxcategorey)

	paginator = Paginator(post_list, 6)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset2 = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset2 = paginator.page(1)
	except EmptyPage:
		paginated_queryset2 = paginator.page(paginator.num_pages)

	context = {
		'post_list': post_list,
		'queryset2': paginated_queryset2,
		'most_recent': most_recent,
		'page_request_var': page_request_var,
		'linuxcategorey_count': linuxcategorey_count,
		
	}
	
	return render(request, 'linux/linux.html',context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def linuxdetails(request,slug): # post er alter a gadgetdetails
	
	linuxcategorey_count = get_linuxcategorey_count()
	#view_count = get_view_count()
	most_recent = LinuxPost.objects.order_by('-timestamp')[:4]
	linuxpost = LinuxPost.objects.filter(slug=slug)
	if linuxpost.exists():
		linuxpost = linuxpost.first()
	else:
		HttpResponse("<h3>page not found</h3>")		

	context = {
		#'postview':postview,
		#'linuxpostview': linuxpostview,
		'linuxpost': linuxpost,
		'most_recent': most_recent,
		'linuxcategorey_count': linuxcategorey_count,
		
	}
	return render(request, 'linux/linuxdetails.html', context)



def linuxsearch(request):
	most_recent = LinuxPost.objects.order_by('-timestamp')[:4]
	linuxcategorey_count = get_linuxcategorey_count()
	queryset2 = LinuxPost.objects.all()
	query = request.GET.get('q')

	if query:
		queryset2 = queryset2.filter(
			Q(title__icontains = query)

		).distinct()
	
	paginator = Paginator(queryset2, 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset2 = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset2 = paginator.page(1)
	except EmptyPage:
		paginated_queryset2 = paginator.page(paginator.num_pages)
	context = {
		'queryset2': queryset2,
		'most_recent': most_recent,
		'linuxcategorey_count': linuxcategorey_count,
		'page_request_var': page_request_var,
		'queryset2': paginated_queryset2,

	}
	return render(request, 'linux/linux_search_result.html', context)