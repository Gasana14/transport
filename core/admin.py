from django.contrib import admin

from .models import Customer, Delivery, DriverWaitingList, Driver, Product, Vehicle


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'phone')
    list_display_links = ('id', 'account')
    search_fields = ('phone',)
    list_filter = ('phone',)
    list_per_page = 25


admin.site.register(Customer, CustomerAdmin)


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'driver','date')
    list_display_links = ('id', 'owner')
    search_fields = ('owner', 'date')
    list_filter = ('date',)
    list_per_page = 25


admin.site.register(Delivery, DeliveryAdmin)


class DriverWaitingListAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'driver')
    list_display_links = ('delivery', 'driver')
    search_fields = ('driver', 'delivery')
    list_filter = ('driver',)
    list_per_page = 25


admin.site.register(DriverWaitingList, DriverWaitingListAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'title', 'quantity')
    list_display_links = ('id', 'delivery', 'title', 'quantity')
    search_fields = ('id', 'delivery', 'title', 'quantity')
    list_filter = ('title',)
    list_per_page = 25


admin.site.register(Product, ProductAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'model', 'capacity')
    list_display_links = ('driver', 'model', 'capacity')
    search_fields = ('driver', 'model', 'capacity', 'plate')
    list_filter = ('plate',)
    list_per_page = 25


admin.site.register(Vehicle, VehicleAdmin)