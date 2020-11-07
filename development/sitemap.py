from django.contrib.sitemaps import Sitemap

from .models import DevelopmentPost

class DevelopmentPostSitemap(Sitemap):
        changefreq = "weekly"
        priority = 0.9

        def items(self):
                return DevelopmentPost.objects.all()

        def location(self, obj):
                return "/development/" + str(obj)
