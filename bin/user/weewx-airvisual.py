# weewx data service to read air quality information from the airvisual api
# Dan Seibel, July 2019


import syslog
import weewx
import requests
from weewx.wxengine import StdService
__version__ = 0.3

'''

Read airvisual api for AQI info


https://api.airvisual.com/v2/nearest_city?lat=<LAT>&lon=<LONG>&key=<API KEY>

API info here:  https://www.airvisual.com/air-pollution-data-api

response returns:

{
  "status": "success",
  "data": {
    "city": "Edmonton",
    "state": "Alberta",
    "country": "Canada",
    "location": {
      "type": "Point",
      "coordinates": [
        -xxxxx,
        yyyyy
      ]
    },
    "current": {
      "weather": {
        "ts": "2019-06-18T01:00:00.000Z",
        "tp": 24,
        "pr": 1013,
        "hu": 36,
        "ws": 6.7,
        "wd": 150,
        "ic": "02n"
      },
      "pollution": {
        "ts": "2019-06-18T01:00:00.000Z",
        "aqius": 45,
        "mainus": "p2",
        "aqicn": 33,
        "maincn": "o3"
      }
    }
  }
}


Interested in aqius

Value range:  "http://support.airvisual.com/knowledgebase/articles/1185775-what-is-aqi"

0-50, "Good"
51-100, "Moderate"
101-150, "Unhealthy for Sensitive Groups"
151-200, "Unhealthy"
201-300, "Very Unhealthy"
301-500+, "Hazardous"
'''


class AQService(StdService):
    def __init__(self, engine, config_dict):
        super(AQService, self).__init__(engine, config_dict)

        try:
            # Grab the needed options out of the configuration dictionary.
            # If a critical option is missing, an exception will be raised

            self.api_key        = config_dict['AQService']['api_key']
            self.latitude       = config_dict['Station']['latitude']
            self.longitude      = config_dict['Station']['longitude']

            syslog.syslog(syslog.LOG_DEBUG, "weewx-airvisual: using api_key: '%s'" % self.api_key)
            syslog.syslog(syslog.LOG_DEBUG, "weewx-airvisual: using latitude: '%s'" % self.latitude)
            syslog.syslog(syslog.LOG_DEBUG, "weewx-airvisual: using longitude: '%s'" % self.longitude)

            self.bind(weewx.NEW_ARCHIVE_RECORD, self.read_data)

        except KeyError as e:
            syslog.syslog(syslog.LOG_INFO, "weewx-airvisual: No values parsed  Missing parameter: %s" % e)

    def read_data(self, event):

        try:
            url = "https://api.airvisual.com/v2/nearest_city?lat=%s&lon=%s&key=%s" % (self.latitude, self.longitude, self.api_key)
            headers = { "Content-Type": "application/json" }
            r = requests.get(url, headers=headers)
            response = r.json()
        except requests.exceptions.RequestException as e:
            syslog.syslog(syslog.LOG_INFO, "weewx-airvisual: exception: %s" % str(e))

        # parse out AQI values.

        try:
            aqi = response['data']['current']['pollution']['aqius']
            syslog.syslog(syslog.LOG_INFO, "weewx-airvisual: aqi value: '%s'" % aqi)

            # record values to database

            event.record['aqi'] = float(aqi)

        except Exception, e:

            syslog.syslog(syslog.LOG_INFO, "weewx-airvisual: exception: %s" % e)
