import os
import sys
import json
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from urllib import parse

from places.models import Place
from places.models import Image


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
            print('Не смог загрузить файл. Проверьте ссылку и попробуйте еще')
            sys.exit()
        except FileNotFoundError:
            err_message = 'Ничего не нашел, проверьте папку {}' \
                .format(options['folder'])
            print(err_message)

    def add_arguments(self, parser):
        parser.add_argument(
            '--link',
            '-l',
            type=str,
            help='Ссылка на json нового места для добавления'
        )
        parser.add_argument(
            '--folder',
            '-f',
            type=str,
            help='Ссылка на папку с  json с местами для добавления'
        )

    def download_new_place_from_url(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        self.places_received.append(response.json())

    def download_new_place_from_folder(self, root_folder: str):
        places_json = []

        for root, dirs, files in os.walk(root_folder):
            places_json = [os.path.join(root, name) for name in files
                           if (name.split('.')[-1]) == 'json']

        if not places_json:
            raise FileNotFoundError

        for json_path in places_json:
            with open(json_path, 'r', encoding='utf-8') as json_file:
                self.places_received.append(json.load(json_file))

    def add_place_with_images_in_db(self):
        for received_place in self.places_received:
            place, created = Place.objects.get_or_create(
                title=received_place['title'],
                lng=received_place['coordinates']['lng'],
                lat=received_place['coordinates']['lat'],
            )

            if not created:
                print(f'Место {place.title} уже существует в бд')
                continue

            place.description_short = received_place['description_short']
            place.description_long = received_place['description_short']
            place.save()

            for position, image_url in enumerate(received_place['imgs'],
                                                 start=1):
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
            print('Не смог загрузить файл')
        except requests.exceptions.ConnectTimeout:
            print('Проблема с соединением, не смог скачать файл')

    def get_image_name_from_url(self, url: str) -> str:
        split_result = parse.urlsplit(url)
        url_path = split_result.path
        return url_path.split('/')[-1]
