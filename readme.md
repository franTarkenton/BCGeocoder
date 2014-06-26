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

Have a very simple API that can be used to interact with the geocoder set up in the file bcgeocoder.py

The *main.py* wraps the geocoder functionality.  Its currently pretty simple.  It 
can receive 3 args
 - input csv file
 - name of the column in the csv file with the address string
 - output csv file
 
The script iterates through the first file, and duplicates it in the second file, with the 
addition of 3 columns
 - **x coordinate** (default projection at the moment is albers but would be easy to add this as an option)
 - **y coordinate** (ditto above for projection) 
 - **precision score** (geocoders response regarding its confidence in the location)
 
 






