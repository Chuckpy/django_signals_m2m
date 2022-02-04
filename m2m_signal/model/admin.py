from django.contrib import admin
from .models import Products, OpenSearch

# Register your models here.

class OpenSearchAdmin(admin.ModelAdmin):
    list_display=('own_product','total_likes','total_matches')
    readonly_fields = ['own_product','match']    
    

admin.site.register(Products)
admin.site.register(OpenSearch,OpenSearchAdmin)

