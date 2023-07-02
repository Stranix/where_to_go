from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from urllib import parse
from urllib.request import urlopen

from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = HTMLField(verbose_name='Полное Описание')
    lng = models.FloatField(verbose_name='Координаты - Долгота', null=True)
    lat = models.FloatField(verbose_name='Координаты - Широта', null=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Image(models.Model):
    position = models.SmallIntegerField(
        verbose_name='Позиция',
        default=0,
        blank=False,
        null=False,
    )
    image_field = models.ImageField(verbose_name='Файл изображения')
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        related_name='images',
        verbose_name='Место',
        null=True,
        blank=True
    )

    def get_remote_image(self, url: str):
        if not self.image_field:
            img_temp = NamedTemporaryFile()
            img_temp.write(urlopen(url).read())
            img_temp.flush()
            self.image_field.save(
                self.get_image_name_from_url(url),
                File(img_temp)
            )
        self.save()

    def get_image_name_from_url(self, url: str) -> str:
        split_result = parse.urlsplit(url)
        url_path = split_result.path
        return url_path.split('/')[-1]

    class Meta:
        ordering = ['position']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'{self.position} {self.place}'
