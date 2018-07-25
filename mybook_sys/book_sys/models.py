from django.db import models

# Create your models here.


class Publish(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    pname = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)


class Book(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    publish = models.ForeignKey(Publish, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')


class Author(models.Model):
    aname = models.CharField(max_length=16)
