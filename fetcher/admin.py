from django.contrib import admin
from .models import Business, Person, Activity, Page, Proxy, URL

# admin.site.register(Person)

admin.site.register(Page)
admin.site.register(Proxy)
admin.site.register(URL)


@admin.action(description="fetch again")
def undo_completed(modeladmin, request, queryset):
    queryset.update(complete=False)


@admin.action(description="cancel being in process")
def in_process(modeladmin, request, queryset):
    queryset.update(in_process=False)

@admin.action(description="get data on next fetch")
def fetch(modeladmin, request, queryset):
    queryset.update(get_on_next_fetch=True)


class PersonInline(admin.TabularInline):
    model = Person


class ActivityInline(admin.TabularInline):
    model = Activity


class BusinessAdmin(admin.ModelAdmin):
    list_filter = ('complete', "in_process", 'status','get_on_next_fetch')
    list_display = ('name', "complete", 'url')
    search_fields = ['name', 'url']
    inlines = [PersonInline, ActivityInline]
    actions = [undo_completed,in_process,fetch]


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name', 'role', "person_id"]
    list_filter = ('role',)


admin.site.register(Business, BusinessAdmin)
admin.site.register(Activity)
admin.site.register(Person, PersonAdmin)
