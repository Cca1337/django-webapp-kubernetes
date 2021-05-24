from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField


# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note", null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    note = models.CharField(max_length=200)

    def __str__(self):
        return self.note

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="obrazok", null=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now, blank=True)
    mimetype = models.CharField(max_length=30)
#    file = models.FileField(upload_to='main/media/')
    file = CloudinaryField('image')

    def __str__(self):
        return self.name
