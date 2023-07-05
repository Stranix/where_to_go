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
                self.add_place_with_images_in_db()

            if options['folder']:
                self.download_new_place_from_folder(options['folder'])
                self.add_place_with_images_in_db()
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
        response = requests.get(url)
        response.raise_for_status()
        self.places_received.append(response.json())

    def download_new_place_from_folder(self, root_folder: str):
        for root, dirs, files in os.walk(root_folder):
            for name in files:
                filename = os.path.join(root, name)
                place = self.load_json(filename)
                if place:
                    self.places_received.append(place)

        if not self.places_received:
            raise FileNotFoundError

    def add_place_with_images_in_db(self):
        for received_place in self.places_received:
            place, created = Place.objects.get_or_create(
                title=received_place['title'],
                lng=received_place['coordinates']['lng'],
                lat=received_place['coordinates']['lat'],
            )

            if not created:
                logger.warning(f'Место {place.title} уже существует в бд')
                continue

            place.description_short = received_place['description_short']
            place.description_long = received_place['description_short']
            place.save()

            for position, image_url in enumerate(
                    received_place['imgs'],
                    start=1
            ):
                image_content_file = self.get_content_file_from_url(image_url)

                if not image_content_file:
                    continue

                image = Image.objects.create(position=position)
                image_name = self.get_image_name_from_url(image_url)
                image.picture.save(image_name, image_content_file)
                place.images.add(image)

    def get_content_file_from_url(self, url: str) -> ContentFile | None:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return ContentFile(response.content)
        except requests.exceptions.HTTPError:
            logger.error('Не смог загрузить файл')
        except requests.exceptions.ConnectTimeout:
            logger.error('Проблема с соединением, не смог скачать файл')

    def get_image_name_from_url(self, url: str) -> str:
        split_result = urllib.parse.urlsplit(url)
        url_path = split_result.path
        return url_path.split('/')[-1]

    def load_json(self, filename: str) -> dict | None:
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except json.decoder.JSONDecodeError:
            logger.error('Не смог зачитать файл %s', filename)
