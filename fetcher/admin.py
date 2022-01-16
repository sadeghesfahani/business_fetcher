from django.contrib import admin
from .models import Business, Person, Activity, Page, Proxy


admin.site.register(Person)
admin.site.register(Activity)
admin.site.register(Page)
admin.site.register(Proxy)



class BusinessAdmin(admin.ModelAdmin):
    list_filter = ('complete',"in_process")
    list_display = ('name',"complete")



admin.site.register(Business, BusinessAdmin)