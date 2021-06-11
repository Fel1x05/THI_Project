from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.utils import translation
from .models import *
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login

from pprint import pprint


def index(request):
    return render(request, 'index.html')


def auth(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
    return HttpResponseRedirect(request.POST['next'])


def races(request):
    try:
        if str(request.user.groups.all()[0]) == "sportsmen":
            if request.method == "POST":
                try:
                    Race.objects.get(sportsmen=request.user.username, distance=int(request.POST["distance"]))
                except:
                    Race(sportsmen=request.user.username, distance=int(request.POST["distance"])).save()
                return HttpResponseRedirect("/races")
            else:
                return render(request, "races0.html", {"races": Race.objects.filter(sportsmen=request.user.username)})

        if str(request.user.groups.all()[0]) == "referee":
            if request.method == "POST":
                stime = datetime.strptime(request.POST["stime"], "%H:%M")
                temp_time = datetime.strptime(request.POST["btime"], "%M:%S")
                btime = timedelta(minutes=temp_time.minute, seconds=temp_time.second)
                tracks = int(request.POST["tracks"]) - 1

                time = stime - btime
                number = 0

                for d in ["100", "400", "1000"]:
                    track = -1
                    time += btime
                    number += 1
                    for race in Race.objects.filter(distance=d):
                        if track < tracks:
                            track += 1
                            Race.objects.filter(id=race.id).update(track=track + 1, number=number,
                                                                   time=time.strftime("%H:%M:%S"))
                        else:
                            number += 1
                            time += btime
                            track = 0
                            Race.objects.filter(id=race.id).update(track=track + 1, number=number,
                                                                   time=time.strftime("%H:%M:%S"))
                return HttpResponseRedirect("/races")

            return render(request, "races1.html", {"races": Race.objects.order_by("time")})
    except:
        return HttpResponseRedirect("/")


def results(request):
    try:
        if str(request.user.groups.all()[0]) == "referee":
            if request.method == "POST":
                if request.POST["but"] == "add":
                    Race.objects.filter(sportsmen=request.POST["sportsmen"], distance=request.POST["distance"]).\
                        update(result_time=request.POST["result_time"])
                if request.POST["but"] == "sort":
                    for d in ["100", "400", "1000"]:
                        i = 0
                        for race in Race.objects.filter(distance=d).order_by("result_time"):
                            i += 1
                            Race.objects.filter(id=race.id).update(place=i)
                return HttpResponseRedirect("/results")
            else:
                return render(request, "result1.html", {"races": Race.objects.order_by("time", "track")})

        if str(request.user.groups.all()[0]) == "sportsmen":
            return render(request, "result0.html", {"races": Race.objects.order_by("time", "track")})
    except:
        return HttpResponseRedirect("/")
