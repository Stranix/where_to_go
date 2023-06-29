import os
import sys
import urllib
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.core.management.base import BaseCommand

from places.models import Place
from places.models import Image


class Command(BaseCommand):
    help = 'Загрузка информации о новых местах'

    def handle(self, *args, **options):
        if options['link']:
            self.download_new_place_from_url(options['link'])

        if options['folder']:
            self.download_new_place_from_folder(options['folder'])

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
        try:
            response = requests.get(url)
            response.raise_for_status()
            received_place = response.json()

            place, created = Place.objects.get_or_create(
                title=received_place['title']
            )

            if not created:
                print('Место уже существует в бд')
                sys.exit()

            place.description_short = received_place['description_short']
            place.description_long = received_place['description_short']
            place.lng = received_place['coordinates']['lng']
            place.lat = received_place['coordinates']['lat']
            place.save()

            for position, image_url in enumerate(received_place['imgs'],
                                                 start=1):
                image = Image.objects.create(position=position)
                image.get_remote_image(image_url)
                place.images.add(image)
        except requests.exceptions.HTTPError:
            print('Не смог загрузить файл. Проверьте ссылку и попробуйте еще')
            sys.exit()

    def download_new_place_from_folder(self, root_folder: str):
        self.check_exist_folder(root_folder)

        place_jsons = []

        for root, dirs, files in os.walk(root_folder):
            place_jsons = [os.path.join(root, name) for name in files if (name.split('.')[-1]) == 'json']

        if not place_jsons:
            print(f'Не нашел в папке {root_folder} json файлы')
            sys.exit()

    def check_exist_folder(self, folder: str):
        if not os.path.exists(folder):
            print('А нет такой папки')
            sys.exit()
        