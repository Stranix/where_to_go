# Куда пойти

Сайт о самых интересных местах **_Москвы_**.  
**Требования для запуска**: `python=>3.10`

![screenshot site](https://github.com/Stranix/where_to_go/blob/master/static/promo.jpg?raw=true)

[Демка сайта](https://stranix.pythonanywhere.com/).  
[Демка админки сайта](https://stranix.pythonanywhere.com/admin/).


## Доступные переменные окружения
`SECRET_KEY` - секретный ключ проекта. Сгенерировать можно [здесь](https://djecrety.ir/).  
`DEBUG` - Режим работы локального сервера. По умолчанию `True`.  
`ALLOWED_HOSTS` - Список разрешенных хостов. Подробности [тут](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts).  
`STATIC_URL` - Папка со статикой. По умолчанию `static/`.  
`STATIC_ROOT` - Папка для статики на **prod** сервере. По умолчанию `assets/`.  
`MEDIA_URL` - Папка с медия файлами. По умолчанию `media/`.  
`MEDIA_ROOT` - Расположение папки media для **dev(runserver)** сервера. По умолчанию `media/`.

_При использовании локального сервера **обязательно** требуется переменная окружения `SECRET_KEY`_  
На **prod** сервере обязательное заполнение `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` 


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
```shell
python3 manage.py load_place -l https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9F%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BE%D0%BD%20%C2%AB%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%C2%BB%20%D0%BD%D0%B0%20%D0%92%D0%94%D0%9D%D0%A5.json
```
_Подробнее о процессе ниже. В разделе [Источник данных для автозагрузки](https://github.com/Stranix/where_to_go/blob/master/README.md#data-sources)_
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


<a href="#" id="data-sources"></a>

## Источники данных для автозагрузки
Источник данных — `json` c подробными сведениями о локации.  
**!!! Главное правило - один json одно место !!!**  
Формат:

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
* `Json` можно зачитать по ссылке  
```shell
python3 manage.py load_place -l https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9F%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BE%D0%BD%20%C2%AB%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%C2%BB%20%D0%BD%D0%B0%20%D0%92%D0%94%D0%9D%D0%A5.json
```
 * Получить из локальной папки
```shell
python3 manage.py load_place -f  downloads
```
Пример содержимого папки:   
![example folder](https://github.com/Stranix/where_to_go/blob/master/static/ex_folder.jpg?raw=true)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).