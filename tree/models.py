from django.db import models


class TreeElements(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=True, blank=True)
