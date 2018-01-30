from collections import defaultdict
import logging

from googleapiclient.discovery import build
import models
from oauth2client.client import GoogleCredentials


INVENTORY_SHEET_ID = '1W6TtessllUmYmqzps9Udi7OVLB5gQM_aRqQbFoNmulA'

def _GetSpreadsheetValuesForRange(spreadsheetId, rangeName):
	credentials = GoogleCredentials.get_application_default()
	service = build('sheets', 'v4', credentials=credentials)
	rangeName = rangeName
	result = service.spreadsheets().values().get(
		spreadsheetId=spreadsheetId, 
		range=rangeName).execute()
	return result.get('values', [])

def GetArmyList(sheet):
	armies = []
	for row in sheet:  # This will break if we add a new army unless the query range changes too
		armies.append(row[0])
	return armies

def ProcessArmyTab(army_id, sheet):
    army = models.CollectionArmy(name=army_id, stats=models.CollectionStats())
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
                unit = models.CollectionUnit(name=row[0], stats=stats)
                army.units.append(unit)
	# logging.debug('Created Army object: %s' %army)			
    return army

def LoadCollectionDataFromSource():
	logging.debug('Retrieving spreadsheet data')

	armies = {}

	# Get the summary data
	rangeName = 'Summary!A2:J13'
	army_ids = GetArmyList(_GetSpreadsheetValuesForRange(spreadsheetId=INVENTORY_SHEET_ID, rangeName=rangeName))

	# for each army returned in the previous call, get the sheet for that army
	for army_id in army_ids:
		rangeName = '%s!A2:O99' %army_id
        armies[army_id] = ProcessArmyTab(army_id, _GetSpreadsheetValuesForRange(spreadsheetId=INVENTORY_SHEET_ID, rangeName=rangeName))

	return armies