from django.contrib import admin
from .models import User,Comentario,Mensaje

# Register your models here.

admin.site.register(User)
admin.site.register(Mensaje)
admin.site.register(Comentario)