from django.contrib import admin
from .models import SiteUser,Lots,Reply, News

admin.site.register(SiteUser)
admin.site.register(Lots)
admin.site.register(Reply)
admin.site.register(News)
