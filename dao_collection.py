from collections import defaultdict
import logging
import re
from google.appengine.ext import ndb

from googleapiclient.discovery import build
import models
from oauth2client.client import GoogleCredentials


INVENTORY_SHEET_ID = '1W6TtessllUmYmqzps9Udi7OVLB5gQM_aRqQbFoNmulA'

def _GetSpreadsheetValuesForRange(spreadsheetId, rangeName):
    credentials = GoogleCredentials.get_application_default()
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, 
        range=rangeName).execute()
    return result.get('values', [])

def _GetSpreadsheetValuesForMultipleRanges(spreadsheetId, ranges):
    credentials = GoogleCredentials.get_application_default()
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId, 
        ranges=ranges).execute()
    return result.get('valueRanges', [])

def GetArmySummary():
    rangeName = 'Summary!A2:J13'
    sheet = _GetSpreadsheetValuesForRange(spreadsheetId=INVENTORY_SHEET_ID, rangeName=rangeName)
    armies = []
    for row in sheet:  # This will break if we add a new army unless the query range changes too
        total = int(row[2])
        key = ''.join(row[0].split()).lower()
        army = models.CollectionArmy(
            key=key,
            name=row[0],
            description='TODO: Description',
            system=0,
            stats=models.CollectionStats(
                total=total,
                made=total - int(row[3]),
                based=total - int(row[4]),
                sanded=total - int(row[5]),
                sprayed=total - int(row[6]),
                magnetised=total - int(row[7]),
                painted=total - int(row[8]))
            )
        armies.append(army)
    return armies

def _ProcessArmyTab(army_id, sheet):
    army_key = ''.join(army_id.split()).lower()
    army = models.CollectionArmy(key=army_key, name=army_id, stats=models.CollectionStats())
    for row in sheet:
        if row and row[0]: # Check that the row has a unit name associated with it, else skip
            stats = models.CollectionStats(
                total=int(row[1]),
                made=int(row[2]),
                based=int(row[3]),
                sanded=int(row[4]),
                sprayed=int(row[5]),
                magnetised=int(row[6]),
                painted=int(row[7])
            )
            
            if row[0] == 'Total':
                army.stats = stats
            else: 
                unit_name = row[0]
                unit_key = ''.join(row[0].split()).lower()
                unit = models.CollectionUnit(key=unit_key, name=unit_name, stats=stats)
                army.units.append(unit)
    # logging.debug('Created Army object: %s' %army)            
    return army

def LoadCollectionDataFromSource():
    # logging.debug('Retrieving spreadsheet data')

    # armies = {}

    # # Get the summary data
    # army_ids = GetAllArmyIds()

    # # for each army returned in the previous call, get the sheet for that army
    # for army_id in army_ids:
    #     rangeName = '%s!A2:O99' %army_id
    #     armies[army_id] = _ProcessArmyTab(army_id, _GetSpreadsheetValuesForRange(spreadsheetId=INVENTORY_SHEET_ID, rangeName=rangeName))

    # return armies
    army_ids = [
        'Dwarves',
        'Beastclaw Raiders',
        'Empire',
        'High Elves',
        'Orcs and Goblins',
        'Seraphon',
        'Skaven',
        'Wood Elves',
        'Astra Militarum',
        'Orkz',
        'Space Wolves',
        'Other',]
    ranges = []
    # ranges.append('Summary!A2:J13')  # Summary Page
    for army_id in army_ids:
        ranges.append('%s!A2:O99' %army_id)

    result = _GetSpreadsheetValuesForMultipleRanges(spreadsheetId=INVENTORY_SHEET_ID, ranges=ranges)

    armies = []
    for sheet in result:
        try:
            army_id = re.search('\'?(.+?)\'?!A2', sheet['range']) .group(1)
        except AttributeError:
            continue

        army = _ProcessArmyTab(army_id, sheet['values'])
        armies.append(army)
        army.put()

    return armies

def GetNdbArmy(army_id):
  return models.CollectionArmy.query(models.CollectionArmy.key == army_id).get()

def GetAllNdbData():
  return models.CollectionArmy.query().fetch()

def DeleteAllNdbData():
  ndb.delete_multi(models.CollectionArmy.query().fetch(keys_only=True))