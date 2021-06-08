from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey("List", on_delete=models.CASCADE, default=None)


class List(models.Model):
    pass
