from django.contrib import admin

from .models import User, Reviews, Comments, Titles, Genres, Categories


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'bio',
        'email',
        'role',
        'confirmation_code',
        'is_active',
        'is_staff'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'title',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('title', )
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review',
        'pub_date'
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
