#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

Description: generating the requests for open-elevation, see: https://github.com/Jorl17/open-elevation/blob/master/docs/api.md 

'''

import requests
import json

class heighmapRequest:
    def __init__(self, hm: dict) -> None:
        """Requires a properly formatted dictionary to get the elevations at the given points, 
        for more details, see: https://github.com/Jorl17/open-elevation/blob/master/docs/api.md """
        self.url =  'https://api.open-elevation.com/api/v1/lookup'
        self.payload_json =json.dumps(hm)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def makeRequest(self):
        response = requests.post(url=self.url, headers=self.headers, data=self.payload_json)

        if response.status_code == 200: # i.e. request successful
            data = response.json()
            return data
        else:
            print(f'Failed fetching elevation data, response code: {response.status_code}')
            return None