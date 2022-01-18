from django.contrib import admin
from .models import Business, Person, Activity, Page, Proxy, URL

admin.site.register(Person)
admin.site.register(Activity)
admin.site.register(Page)
admin.site.register(Proxy)
admin.site.register(URL)


class PersonInline(admin.TabularInline):
    model = Person

class ActivityInline(admin.TabularInline):
    model = Activity

class BusinessAdmin(admin.ModelAdmin):
    list_filter = ('complete', "in_process", 'status')
    list_display = ('name', "complete", 'url')
    search_fields = ['name', 'url']
    inlines = [PersonInline,ActivityInline ]


admin.site.register(Business, BusinessAdmin)
