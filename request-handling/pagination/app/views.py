from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator

import csv
from urllib.parse import urlencode


def index(request):
    return redirect(reverse(bus_stations))

def bus_stations(request):
    STATIONS_COUNT = 100
    with open(settings.BUS_STATION_CSV, 'r', encoding="cp1251") as csvfile:
        reader = csv.DictReader(csvfile)
        stations = [dict(station) for station in reader]

    paginator = Paginator(stations, STATIONS_COUNT)
    # print(paginator.num_pages)

    current_page = request.GET.get('page', 1)
    current_page = int(current_page)
    if current_page > paginator.num_pages:
        current_page = paginator.num_pages
    current_station = paginator.get_page(current_page)

    if current_station.has_previous():
        prev_page_url = reverse('bus_stations') + '?' + \
                        urlencode({'page': current_station.previous_page_number()})
    else:
        prev_page_url = None

    if current_station.has_next():
        next_page_url = reverse('bus_stations') + '?' + \
                        urlencode({'page': current_station.next_page_number()})
    else:
        next_page_url = None

    return render_to_response('index.html', context={
        'bus_stations': stations[(current_page - 1) * STATIONS_COUNT: current_page * STATIONS_COUNT],
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

