from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import ckeditor
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# slug
from django.utils.text import slugify
from random import random
from django.db.models.signals import pre_save
from blog.models import Author
# Create your models here.

class DevelopmentCategorey(models.Model):
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title
class DevelopView(models.Model):
    client_ip = models.GenericIPAddressField()
    #view_count = models.IntegerField(default=0)
    #view_count = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    developmentpost = models.ForeignKey('DevelopmentPost', on_delete=models.CASCADE, blank=True, null=True)





    def __str__(self):
        return self.client_ip
class DevelopmentPost(models.Model):
  
    development_categories = models.ManyToManyField(DevelopmentCategorey)
    title = models.CharField(max_length=55)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    overview = models.TextField(max_length=155)
    seo_keywords = models.TextField(max_length=255,default='-')
    content = RichTextUploadingField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d')
    dev_post = models.ImageField(upload_to='photos/%Y/%m/%d')
    
    featured = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.title

    @property
    def view_count(self):
        return DevelopView.objects.filter(developmentpost=self).count()

    def get_absolute_url(self):
        return reverse('postdetails',kwargs={ 'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = DevelopmentPost.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver, DevelopmentPost)
