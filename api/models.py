from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Вы не ввели email")
        if not username:
            raise ValueError("Вы не ввели username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(
            email,
            username,
            password,
            is_staff=True,
            is_superuser=True
        )


class User(AbstractBaseUser, PermissionsMixin):
    role_choices = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]
    id = models.AutoField(
        primary_key=True,
        unique=True
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    username = models.CharField(
        max_length=50,
        unique=True
    )
    bio = models.TextField(
        'description',
        help_text='Напишите кратко о себе',
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(
        max_length=10,
        choices=role_choices,
        default='user',
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название категории объекта',
        unique=True
    )
    slug = models.SlugField(unique=True, max_length=30)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название жанра", unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название')
    year = models.IntegerField(verbose_name="Год выпуска")
    description = models.CharField(
        max_length=150, verbose_name='Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genres, related_name="titles")
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="titles")

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    ...


class Comments(models.Model):
    ...
