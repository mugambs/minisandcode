#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib
import logging

from google.appengine.api import users

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build

from handlers_base import BaseHandler
import dao_collection

INVENTORY_SHEET_ID = '1W6TtessllUmYmqzps9Udi7OVLB5gQM_aRqQbFoNmulA'

def GetSpreadsheetValuesForRange(spreadsheetId, rangeName):
    credentials = GoogleCredentials.get_application_default()
    service = build('sheets', 'v4', credentials=credentials)
    rangeName = rangeName
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, 
        range=rangeName).execute()
    return result.get('values', [])

# [START collection_page]
class CollectionPage(BaseHandler):

    def get(self):
            
        armies = dao_collection.GetArmySummary()

        self.renderResponse(
            'collection/collection.html',
            categories=['AoS', '40K', 'Various'],
            armies=armies,
        )
# [END collection_page]

# [START army_page]
class ArmyPage(BaseHandler):

    def get(self):
        army_id = self.request.get('id')
        # Test space in name
        # Test sheet not found
        # Test id is missing

        rangeName = '%s!A2:O50' %army_id
        values = GetSpreadsheetValuesForRange(
            spreadsheetId=INVENTORY_SHEET_ID, 
            rangeName=rangeName)

        logging.debug('Spreadsheet values: %s' %values)

        # Test missing values in the data (e.g. no notes)
        units = []
        for row in values:
            if row and row[0]: # Check that the row has a unit name associated with it, else skip
                unit = {
                    'name': row[0],
                    'total': row[1],
                    'made': row[2],
                    'based': row[3],
                    'sanded': row[4],
                    'sprayed': row[5],
                    'magnetised': row[6],
                    'painted': row[7],
                    'to_make': row[8],
                    'to_base': row[9],
                    'to_sand': row[10],
                    'to_spray': row[11],
                    'to_magnetise': row[12],
                    'to_paint': row[13],
                }

                unit['percent_made'] = str((int(unit['made']) * 100.0) / int(unit['total']))
                unit['percent_based'] = str((int(unit['based']) * 100.0) / int(unit['total']))
                unit['percent_sanded'] = str((int(unit['sanded']) * 100.0) / int(unit['total']))
                unit['percent_sprayed'] = str((int(unit['sprayed']) * 100.0) / int(unit['total']))
                unit['percent_magnetised'] = str((int(unit['magnetised']) * 100.0) / int(unit['total']))
                unit['percent_painted'] = str((int(unit['painted']) * 100.0) / int(unit['total']))

                if unit['name'] == 'Total':
                    totals = unit
                else: 
                    units.append(unit)

        army = {
            'name': army_id,
            'units': units,
            'totals': totals,
        }

        self.renderResponse(
            'collection/army.html',
            categories=['Leaders', 'Units', 'Behemoths', 'War Machines'],
            #TODO make the category list relate to the system the army belongs to
            values= values,
            army=army,
            all_data=self.collection_data,
        )
# [END army_page]

# [START unit_page]
class UnitPage(BaseHandler):

    def get(self):
        unit_id = self.request.get('id')
        # Test space in name
        # Test sheet not found
        # Test id is missing

        unit = {
            'name': unit_id,
        }

        self.renderResponse(
            'collection/unit.html',
            unit=unit,
        )
# [END unit_page]
