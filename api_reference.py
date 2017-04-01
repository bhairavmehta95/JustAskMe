from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
from random import randint
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def cart(request):
    # TODO: Fix so it is not hard coded
    person = Person.objects.get(user_id_login = 987)
    id_string = str(request.user.id)
    id_string = Person.objects.get(user_id_login = id_string).person_id
    cart = Completion.objects.filter(person_id = id_string, cart = True)
    activities_as_json = []
        
    for item in cart:
        act_id = item.activity.activity_id
        act_title = item.activity.title
        act_city = item.activity.city.name
        act_country = item.activity.country.name

        activities_as_json.append(activity_dict.copy())
        data = json.dumps(activities_as_json)

    return HttpResponse(data, content_type = 'application/json')


def swipe(request):
    # TODO: Fix so it is not hardcoded
    person = Person.objects.get(user_id_login = 987)

    if request.method == 'POST' and request.POST.get('subyes'):
        category = request.POST.get('category')
        activity_id = request.POST.get('activity')
        
        activity = Activity.objects.get(activity_id = activity_id)
        Completion.objects.create(activity = activity, person = person, cart = True)
        if category == 'Food':
            person.food_count += 1
            print "FOOD", person.food_count
        elif category == 'Adventure':
            person.adventure_count += 1
            print "ADVENTURE", person.adventure_count
        else:
            person.attraction_count += 1
            print "ATTRACTION", person.attraction_count

        person.total_count += 1
        print "TOTAL", person.total_count

        person.save()


    elif request.method == 'POST' and request.POST.get('subno', None):
        category = request.POST.get('category')
        activity_id = request.POST.get('activity')

        activity = Activity.objects.get(activity_id = activity_id)
        Completion.objects.create(activity = activity, person = person)

    
    food_count = person.food_count
    attraction_count = person.attraction_count
    adventure_count = person.adventure_count
    total_count = person.total_count 

    # Pick which categories

    rand = randint(0, total_count)
    activity = None
    category = None

    if rand < food_count:
        while True:
            rand_idx = randint(0, Food.objects.count() - 1)
            food = Food.objects.all()[rand_idx]

            # check if the user has seen it 
            try:
                Completion.objects.get(activity = food.activity, person = person)
            
            # has not been seen by user, send to them
            except ObjectDoesNotExist:
                activity = food.activity
                category = 'Food'
                break


    elif rand >= food_count and rand < food_count + attraction_count:
        while True:
            rand_idx = randint(0, Attraction.objects.count() - 1)
            attr = Attraction.objects.all()[rand_idx]

            try:
                Completion.objects.get(activity = attr.activity, person = person)
            
            # has not been seen by user, send to them
            except ObjectDoesNotExist:
                activity = attr.activity
                category = 'Attraction'
                break

    else:
        while True:
            rand_idx = randint(0, Adventure.objects.count() - 1)
            adven = Adventure.objects.all()[rand_idx]

            try:
                Completion.objects.get(activity = adven.activity, person = person)
            
            # has not been seen by user, send to them
            except ObjectDoesNotExist:
                activity = adven.activity
                category = 'Adventure'
                break

    activities_as_json = []
    act_id = activity.activity_id
    act_title = activity.title
    act_descrip = activity.description
    album = Photo.objects.filter(activity = act_id)
    photos = {}

    for idx,pics in enumerate(album):
        photos[idx] = pics.photo_url

    activity_dict = {"data": {"id":act_id, "title":act_title, "description":act_descrip,"photos":photos}}
    activities_as_json.append(activity_dict.copy())

    data = json.dumps(activities_as_json)
    return HttpResponse(data, content_type = 'application/json')
