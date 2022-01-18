from django.contrib import admin
from .models import Business, Person, Activity, Page, Proxy, URL


admin.site.register(Person)
admin.site.register(Activity)
admin.site.register(Page)
admin.site.register(Proxy)
admin.site.register(URL)


class BusinessAdmin(admin.ModelAdmin):
    list_filter = ('complete',"in_process")
    list_display = ('name',"complete",'url')
    search_fields = ['name', 'url']



admin.site.register(Business, BusinessAdmin)
