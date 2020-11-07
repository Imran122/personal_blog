from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from .models import Post, Author, Categorey, PostView
from django.db.models import Count, Q
from django.db import models
from linux.models import LinuxPost, LinuxCategorey
from development.models import DevelopmentCategorey,DevelopmentPost
from accounts.models import Signup
# Create your views here.

def search(request):
	most_recent = Post.objects.order_by('-timestamp')[:4]
	categorey_count = get_categorey_count()
	queryset = Post.objects.all()
	query = request.GET.get('q')

	if query:
		queryset = queryset.filter(
			Q(title__icontains = query)

		).distinct()
	paginator = Paginator(queryset, 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)
	context = {
		'queryset': queryset,
		'most_recent': most_recent,
		'categorey_count': categorey_count,
		'page_request_var': page_request_var,
		'queryset': paginated_queryset,

	}
	return render(request, 'pages/search_result.html', context)
	


def get_categorey_count():
	queryset = Post.objects.values('categories__id', 'categories__title').annotate(Count('categories__title'))

	return queryset
def get_linuxcategorey_count():
	queryset2 = LinuxPost.objects.values('linuxcategories__id', 'linuxcategories__title').annotate(Count('linuxcategories__title'))

	return queryset2
def get_developmentcategorey_count():
	queryset3 = DevelopmentPost.objects.values('development_categories__id', 'development_categories__title').annotate(Count('development_categories__title'))

	return queryset3
def index(request):
	linuxcategorey_count = get_linuxcategorey_count()
	developmentcategorey_count = get_developmentcategorey_count()
	categorey_count = get_categorey_count()
	featured = Post.objects.filter(featured = True)
	latest = Post.objects.order_by('-timestamp')[0:3]
	dj_recent = DevelopmentPost.objects.order_by('-timestamp')[:3]
	linux_latest = LinuxPost.objects.order_by('-timestamp')[:3]
	
	if request.method == "POST":
		email = request.POST["email"]
		new_signup = Signup()
		new_signup.email = email
		new_signup.save()

	context = {
		'object_list': featured,
		'latest': latest,
		'categorey_count': categorey_count,
		'linux_latest': linux_latest,
		'dj_recent': dj_recent,
		'linuxcategorey_count': linuxcategorey_count,
		'developmentcategorey_count': developmentcategorey_count,
	}
	return render(request, 'pages/index.html', context)



def blog(request, category = None):

	categorey_count = get_categorey_count()
	most_recent = Post.objects.order_by('-timestamp')[:4]
	
	if category is None:
		post_list = Post.objects.all()
	else:
		post_list = Post.objects.filter(categories = category)

	paginator = Paginator(post_list, 6)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	context = {
		'post_list':post_list,
		'queryset': paginated_queryset,
		'most_recent': most_recent,
		'page_request_var': page_request_var,
		'categorey_count': categorey_count,
		
	}
	return render(request, 'pages/blog.html', context)



def post(request,slug):
	#return HttpResponse(get_client_ip(request))
	categorey_count = get_categorey_count()
	
	most_recent = Post.objects.order_by('-timestamp')[:4]
	
	#post = get_object_or_404(Post, slug=slug, id=id)
	post = Post.objects.filter(slug=slug)
	if post.exists():
		post = post.first()
	else:
		HttpResponse("<h3>page not found</h3>")
	


		
	
	

	context = {
		#'postview':postview,
		#'view_count': view_count,
		'post': post,
		'most_recent': most_recent,
		'categorey_count': categorey_count,
		
		
	}
	return render(request, 'pages/post.html', context)


def categorey(request):
	most_recent = Post.objects.order_by('-timestamp')[:4]
	categorey_count = get_categorey_count()

	queryset = Post.objects.order_by('categories')
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
			Q(title__icontains = query)
		).distinct()

	context = {

		'queryset': queryset,
		'most_recent': most_recent,
		'categorey_count': categorey_count
	}
	return render(request, 'pages/categorey.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


	