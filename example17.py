import json
import httplib
import pprint

from sys import exit

hostName   = "data.cityofchicago.org"
service    = "/views/INLINE/rows"
formatType = "json"
parameters = "method=index"
headers    = { "Content-type:" : "application/json" }
query = {
   "originalViewId": "7as2-ds3y",
   "name": "Nearby potholes",
   "query": {
       "filterCondition": {
	       "type": "operator",
           "value": "AND",
           "children": [
               {
                   "children": [
                       {
                           "type": "operator",
                           "value": "within_circle",
                           "metadata": {
                               "freeform": "true"
                           },
                           "children": [
                               {
                                   "type": "column",
                                   "columnId": 2793590
                               },
                               {
                                   "type": "literal",
                                   "value": 41.9249
                               },
                               {
                                   "type": "literal",
                                   "value":  -87.6876
                               },
                               {
                                   "type": "literal",
                                   "value": 100
                               }
                           ]
                       }
                   ],
                   "type": "operator",
                   "value": "OR"
               }
           ]
       }
   }
}

jsonQuery = json.dumps(query)
request = service + '.' + formatType + '?' + parameters 

conn = httplib.HTTPConnection(hostName)
conn.request("POST", request, jsonQuery, headers)
response = conn.getresponse()

if response.reason != 'OK':
	print "There was an error detected."
	print "Response status = %s.\n" % response.status
	print "Response reason = %s.\n" % response.reason
	raise SystemExit(1)

rawResponse = response.read()
jsonResponse = json.loads(rawResponse)

rowNum = 1
for rowData in jsonResponse['data']:
   print "\n===== Row %d ====" % (rowNum)
   colNum = 0
   for columnMeta in jsonResponse['meta']['view']['columns']:
      if columnMeta['id'] > 0:
         print columnMeta['name'], ' = ', rowData[colNum]
      colNum += 1
   rowNum += 1
