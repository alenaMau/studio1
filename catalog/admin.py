from django.contrib import admin

from catalog.models import Category, Status, Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fields = ['name', 'description', 'status_id', 'category_id', 'photo', 'comment']


admin.site.register(Order, OrderAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fields = ['name']


admin.site.register(Category, CategoryAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fields = ['name']


admin.site.register(Status, StatusAdmin)
