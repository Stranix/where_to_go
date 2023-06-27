from django.shortcuts import render

from places.models import Place


def show_index(request):
    places = {'type': 'FeatureCollection'}
    features = []

    for place in Place.objects.all():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.lng, place.lat]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": "https://raw.githubusercontent.com/devmanorg/where-to-go-frontend/master/places/moscow_legends.json"
                }
            }
        )
    places['features'] = features
    return render(request, 'index.html', context={'places': places})
