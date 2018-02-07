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

        ndb_army = dao_collection.GetNdbArmy(army_id)

        if ndb_army: 
            self.renderResponse(
                'collection/army.html',
                categories=['Leaders', 'Units', 'Behemoths', 'War Machines'],
                #TODO make the category list relate to the system the army belongs to
                ndb_army=ndb_army,
            )
        else:
            self.renderResponse(
                'error.html',
                error_msg='Army not found',
                debug_msg=army_id
            )
# [END army_page]

# [START unit_page]
class UnitPage(BaseHandler):

    def get(self):
        army_id = self.request.get('army_id')
        unit_id = self.request.get('unit_id')
        # Test space in name
        # Test sheet not found
        # Test id is missing

        army = dao_collection.GetNdbArmy(army_id)
        for u in army.units:
            if u.key == unit_id:
                unit = u

        if army and unit:
            self.renderResponse(
                'collection/unit.html',
                army=army,
                unit=unit,
            )
        else:
            self.renderResponse(
                'error.html',
                error_msg='Unit not found',
                debug_msg='army_id: %s, unit_id: %s' % (army_id, unit_id),
            )
# [END unit_page]