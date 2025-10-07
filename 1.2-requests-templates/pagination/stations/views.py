import csv
import os

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))
    bus_stations = []
    count = 0
    with open("data-398-2018-08-30.csv", encoding="utf-8") as f:
        file_data = csv.DictReader(f, delimiter=',')
        for row in file_data:
            bus_stations.append(row)
    paginator = Paginator(bus_stations, 10)
    page = paginator.get_page(page_number)
    context = {'bus_stations': page.object_list,'page': page}
    return render(request, 'stations/index.html', context)

