from django.contrib import admin

from users.models import MyUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    search_fields = list_display
    ordering = ['username']

admin.site.register(MyUser, UserAdmin)
