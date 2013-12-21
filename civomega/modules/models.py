from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)
