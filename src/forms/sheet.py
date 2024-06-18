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
from . import models

def parse_dnd_classes(dnd_class_str: str):
  if dnd_class_str == "All":
    return [obj.__str__() for obj in models.DndClass.objects.all()]
  else:
    return [item.strip() for item in dnd_class_str.split(',')]
  
def parse_rolls(roll_str: str, form_name):
  rolls = []
  for roll in [item.strip() for item in roll_str.split(',')]:
    if roll != "Depends":
      ndn, d_type = roll.split()
      num_dice, num_sides = ndn.split("d")
      rolls.append({
        "form": form_name,
        "damage_type": d_type,
        "num_sides": num_sides,
        "num_dice": num_dice
      })
  return rolls

def get_local_values(sheet_path="forms/sheets/6-17.xlsx"):
  # Load the workbook
  wb = load_workbook(sheet_path)

  # Load the specified sheet
  form_sheet = wb['Forms']
  form_range: list[Cell] = form_sheet["3":"10"]
  print(type(form_range))
  print(form_range)
  # header_range = form_sheet["2"]

  data = {"forms":[], "rolls":[]}
  for row in form_range:

    if row[5].value:  # F corresponds to 5
      form_dict = {
        "name": row[5].value,  # F corresponds to 5
        "element": row[2].value,  # C corresponds to 2
        "discipline": row[3].value,  # D corresponds to 3
        "mastery": row[4].value,  # E corresponds to 4
        "description": row[6].value,  # G corresponds to 6
        "has_higher_level": False,
        "concentration": bool(row[8].value),  # I corresponds to 8
        "target": row[9].value,  # J corresponds to 9
        "casting_speed": row[10].value,  # K corresponds to 10
        "duration": row[11].value,  # L corresponds to 11
        "range": row[12].value,  # M corresponds to 12
        "components": row[13].value,  # N corresponds to 13
        "saving_throw": row[15].value,  # P corresponds to 15
        "classes": parse_dnd_classes(row[16].value),  # Q corresponds to 16
        "costs_slot": bool(row[17].value),  # R corresponds to 17
        "special_reqs": row[18].value,  # S corresponds to 18
      }
      
      for roll in parse_rolls(row[14].value, form_name=row[5].value):  # O corresponds to 14, F corresponds to 5
          data["rolls"].append(roll)

      if row[7].value:  # H corresponds to 7
          form_dict.update({"has_higher_level": True, "higher_levels": row[7].value})  # H corresponds to 7

      data["forms"].append(form_dict)

  return data