from django.db import models
from django.utils import timezone


class Bucket(models.Model):
    """Represents a bucket to store items in"""
    name = models.CharField(max_length=255)
    created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class IdentifierType(models.Model):
    name = models.CharField(max_length=255)
    regex = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    """Represents an item to be managed"""
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Identifier(models.Model):
    type = models.ForeignKey(IdentifierType, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.type.name + ': ' + self.value
