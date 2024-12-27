from django.contrib import admin
from .models import BikeShareProfile, Station, Bike, Order

@admin.register(BikeShareProfile)
class BikeShareProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'wallet_balance', 'amount_owed']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']

# Make sure to register other models as well
admin.site.register(Station)
admin.site.register(Bike)
admin.site.register(Order)