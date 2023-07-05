import os
import sys
import json
import urllib
import logging

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place
from places.models import Image

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загрузка информации о новых местах'
    places_received = []

    def handle(self, *args, **options):
        try:
            if options['link']:
                self.download_new_place_from_url(options['link'])

            if options['folder']:
                self.download_new_place_from_folder(options['folder'])

            self.add_places_with_images_in_db()

        except requests.exceptions.HTTPError:
            logger.error(
                'Не смог загрузить файл. Проверьте ссылку и попробуйте еще',
            )
            sys.exit()
        except FileNotFoundError:
            folder = options['folder']
            logger.error('Ничего не нашел, проверьте папку %s', folder)

    def add_arguments(self, parser):
        parser.add_argument(
            '--link',
            '-l',
            type=str,
            help='Ссылка на json нового места для добавления',
        )
        parser.add_argument(
            '--folder',
            '-f',
            type=str,
            help='Ссылка на папку с  json с местами для добавления',
        )

    def download_new_place_from_url(self, url: str):
        logger.info('Получаю информацию о месте из url')
        response = requests.get(url)
        response.raise_for_status()
        place_serializer = response.json()
        if place_serializer.get('title'):
            self.places_received.append(place_serializer)
            logger.info('Ок. Информация получена')

    def download_new_place_from_folder(self, root_folder: str):
        logger.info('Получаю информацию о месте из файлов в папке')
        for root, dirs, files in os.walk(root_folder):
            for name in files:
                filename = os.path.join(root, name)
                place_serializer = self.load_json(filename)
                if place_serializer.get('title'):
                    logger.info('Ок. Информация получена')
                    self.places_received.append(place_serializer)

        if not self.places_received:
            raise FileNotFoundError

    def add_places_with_images_in_db(self):
        logger.info('Сохраняю информацию о местах с картинками')
        for received_place in self.places_received:
            try:
                place = self.add_place_to_db(received_place)
                if not received_place.get('imgs'):
                    logger.warning('Для места %s нет картинок', place.title)
                    continue
                for image_url in received_place['imgs']:
                    image = self.add_image_to_db_from_url(image_url)
                    logger.info('Связываю место и картинку')
                    place.images.add(image)
            except KeyError:
                logger.error('Не могу сохранить, не полная информация о месте')

    def add_place_to_db(self, received_place: dict) -> Place:
        logger.info(
            'Добавляю информацию о месте %s в базу',
            received_place['title']
        )
        place, _ = Place.objects.get_or_create(
            title=received_place['title'],
            defaults={
                'lng': received_place['coordinates']['lng'],
                'lat': received_place['coordinates']['lat'],
                'description_short': received_place.get('description_short', ''),
                'description_long': received_place.get('description_long', '')
            }
        )
        return place

    def add_image_to_db_from_url(self, image_url: str) -> Image:
        logger.info('Загружаю информацию о картинке в базе из url')
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image, _ = Image.objects.update_or_create(
                picture=ContentFile(
                    response.content,
                    self.get_image_name_from_url(image_url)
                )
            )
            logger.info('Изображение сохранено: %s', image.picture.name)
            return image
        except requests.exceptions.HTTPError:
            logger.error('Не смог загрузить файл')
        except requests.exceptions.ConnectTimeout:
            logger.error('Проблема с соединением, не смог скачать файл')

    def get_image_name_from_url(self, url: str) -> str:
        logger.info('Получаю имя картинки из url')
        split_result = urllib.parse.urlsplit(url)
        url_path = split_result.path
        return url_path.split('/')[-1]

    def load_json(self, filename: str) -> dict | None:
        logger.info('Зачитываю json file: %s', filename)
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except json.decoder.JSONDecodeError:
            logger.error('Не смог зачитать файл %s', filename)
