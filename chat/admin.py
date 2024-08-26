from django.contrib import admin
from .models import Message, Room


# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = "id", "name"


class MessageAdmin(admin.ModelAdmin):
    list_display = "id", "value", "date", "room", "user"


admin.site.register(Message, MessageAdmin)
admin.site.register(Room, RoomAdmin)
