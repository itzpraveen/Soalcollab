from django.contrib import admin
from .models import Client, Task, Attachment

admin.site.register(Client)
admin.site.register(Task)
admin.site.register(Attachment)
