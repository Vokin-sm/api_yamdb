import django_filters

from api.models import Titles


class TitlesFilter(django_filters.FilterSet):
    """Titles Filter"""

    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='exact')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='contains')
    year = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Titles
        fields = ['name', 'year', 'category', 'genre']
