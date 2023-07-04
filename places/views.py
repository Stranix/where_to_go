from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from places.models import Place


def show_index(request):
    places = {'type': 'FeatureCollection'}
    features = []

    for place in Place.objects.all():
        features.append(
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.lng, place.lat]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.id,
                    'detailsUrl': reverse('show-place', args=[place.id])
                }
            }
        )
    places['features'] = features
    return render(request, 'index.html', context={'places': places})


def show_place(request, pk: int):
    place = get_object_or_404(Place, pk=pk)
    data = {
        'title': place.title,
        'imgs': [img.picture.url for img in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': str(place.lng),
            'lat': str(place.lat)
        }
    }
    return JsonResponse(
        data,
        json_dumps_params={'ensure_ascii': False, 'indent': 2},
    )
