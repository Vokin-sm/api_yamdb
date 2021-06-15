from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Titles(models.Model):
    ...


class Categories(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    slug = models.SlugField(unique=True)


class Genres(models.Model):
    ...


class Reviews(models.Model):
    ...


class Comments(models.Model):
    ...
