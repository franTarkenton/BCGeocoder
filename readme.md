#BC Geocoder

## Introduction

A geocoder web application for BC has been created [more info on the geocoder available here] (http://www.data.gov.bc.ca/dbc/geographic/locate/geocoding.page)
Within the BC provincial government there is a desire to make the BC geocoder 
more accessible to arcgis desktop users as well as potentially to other non 
gis staff. The vision would be to create the following components:
  
  - A python api that allows addresses to be sent to the geocoding 
    web service and have the geocoding web service return the 
    results of the geocoding back to the user.
   
  - A linkage between the arcgis desktop and the python api.  In theory 
    the easiest way to glue this together would be to use a toolbox, 
    and tool.  The only dependency this version would have is on the 
    arcgis toolbox.  No other arcgis components will be used.
    
  - A stand along tool that would allow anyone to run the geocoder. This 
    version would be totally independent of arcgis.  
    
The focus of this project initially be primarily with the construction of a python 
api that brokers the communication between strngs that are to be geocoded and the 
results of the submitting those results to a geocoder.

## BC Geocoding API

For now going to keep this as simple as possible.  At this stage
things are more of a proof of concept idea.  

###Requirements for initial stage:

  - input: address string
  - input: projection Albers or Geographic
  - input: distance from curb (default is 0)
  - ouput: csv or xls file with these parameters:
     - lat, long
     - projection srs code
     - score (an indication of the strength of the match)
     
  
In the future we may want to add the following options:
  - Ability to communicate with the Batch geocoder. Current version 
    is just iterating over a list of values and sending them individually 
    to the geocoder.  Batch would send a batch file.
  - Currently all communication is over http.  May want to 
    add https support.  Some issues with https and python 
    but nothing that can't be resolved. (based on communications
    sent to me by Michael Ross)
  - Reverse Geocoding.
  - Ability to send more precise information.  Instead of sending 
    a single address string, add the ability to separate the 
    parts of the address string and send those individually:
      - siteName
      - unitDesignator
      - unitNumber 
      - etc...
      
   More Info on individual values available [here] (http://www.data.gov.bc.ca/local/dbc/docs/geo/services/standards-procedures/online_geocoder_rest_api.pdf)
  
### Code

Api is currently all in one file.  bcgeocoder.py



##### Notes from Brian and Mike - MUST FORMAT THIS

Here's an example of how to request a Geomark in GeoJSON format. Similar approach for KML or SHP.

<Geomark URL><Format><Coord System>
http://apps.gov.bc.ca/pub/geomark/geomarks/gm-5DF698C668B7431E8BD2EBC1BA67DF34/parts.geojson?srid=3005


__________________________________________________________________________________
Brian 


From: Kelsey, Brian GCPE:EX 
Sent: Tuesday, June 10, 2014 3:34 PM
To: Netherton, Kevin J FLNR:EX
Subject: Geocoder request URLs

Kevin,


Here’s a quick example of how to request a csv from one of our APIs. Although there are API docs on our website in the ‘ Reference Guides ’ section, I usually just execute a request with the Online Geocoder and have Fiddler running to capture the request URL.


CSV:
http://apps.gov.bc.ca/pub/geocoder/addresses.csv?setBack=0&minScore=1&maxResults=1&interpolation=adaptive&echo=true&outputSRS=4326&addressString=525%20Superior%20St%2C%20victoria&locationDescriptor=any&ver=1.2

GeoJSON:
http://apps.gov.bc.ca/pub/geocoder/addresses.geojson?setBack=0&minScore=1&maxResults=1&interpolation=adaptive&echo=true&outputSRS=4326&addressString=441%20Columbia%20St%2C%20Kamloops&locationDescriptor=any&ver=1.2

KML:
http://apps.gov.bc.ca/pub/geocoder/addresses.kml?setBack=0&minScore=1&maxResults=1&interpolation=adaptive&echo=true&outputSRS=4326&addressString=441%20Columbia%20St%2C%20Kamloops&locationDescriptor=any&ver=1.2


Regards,
__________________________________________________________________________________
Brian Kelsey | Architecture Analyst | Spatial Architecture and Strategic Initiatives | DataBC, Enterprise Data Services | Government Communication and Public Engagement Office
PHONE: (250) 387-9710


 has been built and exists.  This project aims
to create a python script or api that can use the backend geocoder api to 
perform geocoding tasks.



