from django.contrib import admin
from .models import News, Company, Query, Enrolled, CompanyAnalytics
admin.site.register(News)
admin.site.register(Company)
admin.site.register(Query)
admin.site.register(Enrolled)
admin.site.register(CompanyAnalytics)