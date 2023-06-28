# Куда пойти

Сайт о самых интересных местах **_Москвы_**.

![screenshot site](https://github.com/Stranix/where_to_go/blob/master/static/promo.jpg?raw=true)

[Демка сайта](https://devmanorg.github.io/where-to-go-frontend/).  
[Демка админки сайта](https://devmanorg.github.io/where-to-go-frontend/).

## Как запустить

* Скачайте код
```shell
git clone https://github.com/Stranix/where_to_go.git
```

* Устанавливаем зависимости
```shell
pip3 install -r requirements.txt
```

* Создаем структуру базы
```shell
python3 manage.py migrate
```

* Заполняем сайт тестовыми данными с помощью json
* Запускаем локальный сервер
```shell
python3 manage.py runserver
```

* Открываем [сайт](http://127.0.0.1:8000/)

### Чтобы попасть в админку сайта надо:
* Создать админ пользователя
```shell
python3 manage.py createsuperuser
```
* Перейти по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)



## Доступные переменные окружения
`SECRET_KEY` - секретный ключ проекта. Сгенерировать можно [здесь](https://djecrety.ir/).  
`DEBUG` - Режим работы локального сервера. По умолчанию `True`.  
`ALLOWED_HOSTS` - Список разрешенных хостов. Подробности [тут](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts).  
`STATIC_URL` - Папка со статикой. По умолчанию `static/`.  
`MEDIA_URL` - Папка с медия файлами. По умолчанию `media/`.  
`MEDIA_ROOT` - Расположение папки media. По умолчанию `./корень_проекта/media/`.

_При использовании локального сервера переменные окружения можно не использовать._  
На **prod** сервере обязательное заполнение `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`   

## Источники данных

Данные записаны в [формате GeoJSON](https://ru.wikipedia.org/wiki/GeoJSON). Все поля здесь стандартные, кроме `properties`. Внутри `properties` лежат специфичные для проекта данные:

* `title` — название локации
* `placeId` — уникальный идентификатор локации, строка или число
* `detailsUrl` — адрес для скачивания доп. сведений о локации в JSON формате

Значение поля `placeId` может быть либо строкой, либо числом. Само значение не играет большой роли, важно лишь чтобы оно было уникальным. Фронтенд использует `placeId` чтобы избавиться от дубликатов — если у двух локаций одинаковый `placeId`, то значит это одно и то же место.

Второй источник данных — это те самые адреса в поле `detailsUrl` c подробными сведениями о локации. Каждый раз, когда пользователь выбирает локацию на карте, JS код отправляет запрос на сервер и получает картинки, текст и прочую информацию об объекте. Формат ответа сервера такой:

```javascript
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).