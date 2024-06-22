from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
import json
from . import sheet
from . import models
from commonutils import utils

from django.core import serializers
from django.core.serializers.base import DeserializationError
from django.db.models import ManyToManyField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string

def index(request):
    
    paginator = Paginator(sorted(models.DndForm.objects.all(), key=lambda obj: obj.name), per_page=10)
    page_number = request.GET.get("page",1)
    
    try:
        current_form_list_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_form_list_page = paginator.page(1)
    except EmptyPage:
        current_form_list_page = paginator.page(paginator.num_pages)
        
    form_data = serializers.serialize("json", current_form_list_page.object_list)

    current_form_list_page = paginator.page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print(page_number)
        data = {
            'form_list': form_data,
            'pagination_html': render_to_string('home/pagination.html', {'page_obj': current_form_list_page}, request=request)
        }
        return JsonResponse(data)
    
    context = {
        "title": "All Forms",
        "form_page": current_form_list_page,
        "page_obj": current_form_list_page,
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

# Helpers
