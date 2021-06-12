from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Titles(models.Model):
    ...


class Categories(models.Model):
    ...


class Genres(models.Model):
    ...


class Reviews(models.Model):
    ...


class Comments(models.Model):
    ...
