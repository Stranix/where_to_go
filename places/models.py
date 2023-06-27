from django.db import models


class Place(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    lng = models.FloatField(verbose_name='Координаты - Долгота')
    lat = models.FloatField(verbose_name='Координаты - Широта')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField(verbose_name='Имя картинки', max_length=200)
    image_field = models.ImageField(verbose_name='Файл изображения')
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        related_name='images',
        verbose_name='Место',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'{self.id} {self.place}'
