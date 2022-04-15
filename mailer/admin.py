from django.contrib import admin
from mailer.models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'created_at', 'updated_at']
    # search_fields = ['email', 'status', 'created_at', 'updated_at']


admin.site.register(Address, AddressAdmin)

admin.site.site_title = 'Панель управления'
admin.site.site_header = 'Панель управления'