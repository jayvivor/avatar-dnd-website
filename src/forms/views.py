from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json
from . import sheet
from . import models

def index(request):
    return HttpResponse("This page is in progress, BITCH")

def info(request, dnd_form_name):
    # form_info = DndForm.objects.get(pk=dnd_form_name)

    return HttpResponse(f"This is the form description for {dnd_form_name}.")

def refresh(request):

    # Class, Ability, Damage Type, Element, Mastery Level, Casting Speed
    for c, name_list in models.edition_definition_dict.items():
        for name in name_list:
            c.objects.get_or_create(name=name)

    # Discipline
    for element, discipline_list in models.DISCIPLINE_DICT.items():
        for discipline in discipline_list:
            models.DndDiscipline.objects.get_or_create(name=discipline, element=models.DndElement.objects.get(pk=element), description=f"{discipline.upper()}")
    
    # Form, Roll

    form_data = json.loads(sheet.get_local_values().content)
    for form_dict in form_data["forms"]:
        models.DndForm.objects.get_or_create(**form_dict)
    for roll_dict in form_data["rolls"]:
        models.DndRoll.objects.get_or_create(**roll_dict)



    return HttpResponse(f"Database has been refreshed.")