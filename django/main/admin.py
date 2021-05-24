from django.contrib import admin
from .models import ToDoList, Item, Note, Picture
# Register your models here.

admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Note)
admin.site.register(Picture)
