# API/configuration for communicating with google sheets

# import google.auth
# from google.auth.transport.urllib3 import AuthorizedHttp
# from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file(
#     '/path/to/key.json')


# SHEET_ID = "1XzQwktG5m132CkfkZdyBomx3nW3EItD286awMElRtio"

# def get_values(spreadsheet_id, range_name):

#   authed_http = AuthorizedHttp(credentials)

#   response = authed_http.request(
#     'GET', f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}')

from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import Cell
from . import models, utils

from django.http import JsonResponse
from django.core.serializers import serialize

sheet_cache = None

def parse_dnd_classes(dnd_class_str: str):
  if dnd_class_str == "All":
    return [obj.__str__() for obj in models.DndClass.objects.all()]
  else:
    return [item.strip() for item in dnd_class_str.split(',')]
  
# def parse_rolls(roll_str: str, form_name):
#   rolls = []
#   for roll in [item.strip() for item in roll_str.split(',')]:
#     if roll != "Depends":
#       try:
#         ndn, damage_type = roll.split()
#         num_dice, num_sides = ndn.split("d")
#         rolls.append(models.DndRoll.objects.get_or_create(
#           form=form_name,
#           damage_type=damage_type,
#           "num_sides": num_sides,
#           "num_dice": num_dice
#         ))
#       except ValueError:
#         print(roll)
#         continue
#   return rolls



def parse_saving_throws(saving_throw_str: str):
  throws = []
  for throw in unpack_comma_separated_list(saving_throw_str):
    if throw != "Depends" and throw != "N/A":
      if throw in models.DND_ABILITIES:
        throws.append(models.DndAbility.objects.get(name=throw))
      elif throw in models.DND_SKILLS:
        throws.append(models.DndSkill.objects.get(name=throw))
      else:
        throws.append(models.DndCombatDefense.objects.get(name=throw))
  return throws

def parse_disciplines(discipline_str: str, element: str):
  disciplines = []
  for discipline in unpack_comma_separated_list(discipline_str):
    if discipline != "Depends":
      disciplines.append(models.DndDiscipline.objects.get(name=discipline, element=element))
  return disciplines

def parse_casting_speeds(casting_speed_str: str):
  casting_speeds = []
  for casting_speed in unpack_comma_separated_list(casting_speed_str):
    if casting_speed != "Depends":
      casting_speeds.append(models.DndCastingSpeed.objects.get(name=casting_speed))
  return casting_speeds

def unpack_comma_separated_list(csl: str):
  return [word.strip() for word in csl.split(",")]

def get_sheet_data(sheet_path="forms/sheets/6-20.xlsx", cached=True):
  '''
  Retrieves the range of cells that contain all forms in the spreadsheet.
  '''
  global sheet_cache

  if cached and sheet_cache:
    return sheet_cache
  
  # Load the workbook
  wb = load_workbook(sheet_path)

  # Load the specified sheet
  form_sheet = wb['Forms']
  form_range: list[Cell] = form_sheet["3":"1000"]
  # header_range = form_sheet["2"]

  sheet_cache = form_range

  return form_range

def get_uniques_from_row(row_number: int):
  full_list = []
  for row in get_sheet_data():
    if row[row_number].value:
      for unpacked_value in unpack_comma_separated_list(row[row_number].value):
        full_list.append(unpacked_value)
  data = {"data":list(set(full_list))}  # Grabs all unique values from specified row
  return JsonResponse(data)

def get_forms():
  data = {"forms":[]}
  for row in get_sheet_data():

    if row[5].value:  # F corresponds to 5
      name = row[5].value # F corresponds to 5
      target = row[9].value # J corresponds to 9
      description = row[6].value # G corresponds to 6
      duration = row[11].value # L corresponds to 11
      # range = row[12].value # M corresponds to 12      
      special_reqs = row[18].value # S corresponds to 18
      costs_slot = bool(row[17].value) # R corresponds to 17
      concentration = bool(row[8].value) # I corresponds to 8
      element = models.DndElement.objects.get(name=row[2].value) # C corresponds to 2
      mastery = models.DndMasteryLevel.objects.get(name=row[4].value) # E corresponds to 4
      discipline : list[models.DndDiscipline] = parse_disciplines(discipline_str=row[3].value, element=element)  # D corresponds to 3      
      casting_speed : list[models.DndCastingSpeed]= parse_casting_speeds(casting_speed_str=row[10].value) # K corresponds to 10
      # components = models.DndComponent.objects.get(name=row[13].value) # N corresponds to 13
      saving_throws : list[models.DndCombatDefense] = parse_saving_throws(saving_throw_str=row[15].value) # P corresponds to 15
      classes = [models.DndClass.objects.get(name=c) for c in parse_dnd_classes(row[16].value)] # Q corresponds to 16


      form_dict = {
        "name": name,
        "element": serialize("json", utils.to_iter(element)),
        "discipline": serialize("json", utils.to_iter(discipline)),
        "mastery": serialize("json",utils.to_iter(mastery)),
        "description": description,
        "concentration": concentration,
        "target": target,
        "casting_speed": serialize("json", utils.to_iter(casting_speed)),
        "duration": duration,
        # "range": range,
        # "components": serialize("json", utils.to_iter(components)),
        "saving_throws": serialize("json", utils.to_iter(saving_throws)),
        "classes": serialize("json", utils.to_iter(classes)),
        "costs_slot": costs_slot,
        "special_reqs": special_reqs,
      }

      if row[7].value:
        form_dict.update({"has_higher_level_bonus": True, "higher_levels": row[7].value})
      else:
        form_dict.update({"has_higher_level_bonus": False})

      # for roll in parse_rolls(row[14].value, form_name=row[5].value):  # O corresponds to 14, F corresponds to 5
      #   data["rolls"].append(roll)

      data["forms"].append(form_dict)

  return JsonResponse(data)

def get_local_rolls(sheet_data):
  pass