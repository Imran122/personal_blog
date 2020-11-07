from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, DevelopmentCategorey,DevelopmentPost,DevelopView
# Register your models here.
#Email: mdimranhossain0066@gmail.com
#Pass: ghost22boy#
#username : imran

class DevelopmentPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','is_published','author')
    list_display_links = ('id', 'title',)
    list_editable = ('is_published',)
    search_fields = ('title',)

class DevelopmentCategoreyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)

admin.site.register(DevelopmentPost,DevelopmentPostAdmin)
admin.site.register(DevelopView)
admin.site.register(DevelopmentCategorey,DevelopmentCategoreyAdmin)