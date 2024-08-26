from django.contrib import admin

from users.models import User, OneTimePassword


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'email', 'first_name', 'last_name', 'password', 'contact', 'address', 'role', 'image', 'cv',
        'is_verified', 'date_joined', 'last_login')


class OneTimePasswordAdmin(admin.ModelAdmin):
    model = OneTimePassword
    list_display = ('user', 'code')


admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword, OneTimePasswordAdmin)
