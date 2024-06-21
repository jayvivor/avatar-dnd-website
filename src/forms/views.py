from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json
from . import sheet
from . import models, utils

from django.core import serializers
from django.core.serializers.base import DeserializationError
from django.db.models import ManyToManyField


def index(request):
    context = {
        "title": "All Forms",
        "form_list": models.DndForm.objects.all(),
        "class_list": models.DndClass.objects.all(),
    }
    return render(request, "forms/form_list.html", context=context)

def info(request, dnd_form_name):
    # form_info = DndForm.objects.get(pk=dnd_form_name)
    
    return HttpResponse(f"This is the form description for {dnd_form_name}.")

def refresh(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Class, Ability, Damage Type, Element, Mastery Level
    for c, name_list in models.edition_definition_dict.items():
        for name in name_list:
            c.objects.get_or_create(name=name)

    # Discipline
    for element, discipline_list in models.DISCIPLINE_DICT.items():
        for discipline in discipline_list:
            models.DndDiscipline.objects.get_or_create(name=discipline, element=models.DndElement.objects.get(pk=element), description=f"{discipline.upper()}")
    
    # Casting Speed, Form, Roll

    casting_speed_data = json.loads(sheet.get_uniques_from_row(row_number=10).content)

    for speed in casting_speed_data["data"]:
        models.DndCastingSpeed.objects.using("default").get_or_create(name=speed)

    form_data = json.loads(sheet.get_forms().content)["forms"]

    m2m = models.DndForm

    for form_dict in form_data:
        trans_form_dict = {}
        for k, v in form_dict.items():
            try:
                v = [obj.object for obj in serializers.deserialize("json", v)] # Should raise a deserialization/attribute error if not a deserialized model
                trans_form_dict.update({k:v})
            except (DeserializationError, AttributeError):
                trans_form_dict.update({k:v})

        m2m = {key: utils.to_iter(value) for key, value in trans_form_dict.items() if isinstance(getattr(models.DndForm, key).field, ManyToManyField)}

        trans_form_dict = {key: utils.to_iter(value)[0] for key, value in trans_form_dict.items() if key not in m2m.keys()}

        new_model, _ = models.DndForm.objects.using("default").get_or_create(**trans_form_dict)
        for key, value in m2m.items():
            for v in value:
                # return HttpResponse(getattr(models.DndForm, key))
                # try:
                #     getattr(new_model, key).add(value)
                # except:
                #     return HttpResponse(f"{m2m}")
                v = v.__class__.objects.using("default").get(pk=v.pk)
                getattr(new_model, key).add(v)
    # for roll_dict in form_data["rolls"]:
    #     models.DndRoll.objects.get_or_create(**roll_dict)



    return HttpResponse(f"Database has been refreshed.")