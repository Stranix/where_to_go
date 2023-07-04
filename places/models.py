from django.db import models

from urllib.request import urlopen

from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    description_short = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    description_long = HTMLField(
        verbose_name='Полное Описание',
        blank=True
    )
    lng = models.FloatField(verbose_name='Координаты - Долгота')
    lat = models.FloatField(verbose_name='Координаты - Широта')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Image(models.Model):
    position = models.SmallIntegerField(
        verbose_name='Позиция',
        default=0,
    )
    picture = models.ImageField(verbose_name='Файл изображения')
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        related_name='images',
        verbose_name='Место',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['position']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'{self.position} {self.place}'
