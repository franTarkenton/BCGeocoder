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
    
The focus of this project initially will primarily be with the construction of a python 
api that brokers the communication between address strings that are to be geocoded and the 
locations that the geocoder returns for those strings.

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
     
**6-26-2014** - All of the above, except the projection issue are complete
  
####Identified Changes Required
Based on feedback from meeting with DataBC on 8-7-2014 we should make the 
following changes to the existing script:

  - Currently the script duplicates an existing csv file and adds the columns
    x, y, and precision points.  Need to modify the script so that it also 
    returns the following:
    
    - **Address** that gets returned by the geocoder.  This can be different 
      from the address supplied.  It will include the changes that the 
      geocoder made to the address.
    	  
    - The script should also return the **Faults** and **Score**
    
  - Modify the code so that it can handle multiple returns for a single address
  
  - Currently the script requests that the geocoder returns the data in JSON
    format.  This has its advantages as the JSON can be very easily converted
    to python data structures which gives you complete control over where it
    goes and any transformations that need to take place in the process.  It 
    would be useful to investigate whether requesting the data to be returned
    as csv offers any efficiencies.
 
####In the future we may want to add the following options:

  - Ability to communicate with the Batch geocoder. Current version 
    is just iterating over a list of values and sending them individually 
    to the geocoder (each result currently involves a round trip from python 
    to the web service, and back).  Batch would send all the addresses at once to the 
    geocoder, then wait for the geocoder to return with those values.
    
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
    
  - Add more input file support. Add the ability to input the various 
    flavours of excel formats, and the ability to output spatial formats 
    like .shp, file geodatabase, gml, kml, etc.  Some of this (*kml*) can be
    addressed by the geocoder itself.  Doing the translation to the spatial
    formats in the client code gives more control though.  [GDAL/OGR](http://www.gdal.org) can 
    be used to write all the listed spatial files and [more](http://www.gdal.org/ogr_formats.html).
    
    [xlrd and xlwt](http://www.python-excel.org/) can be used to address
    excel reading in a platform independant manner.
      
  
### Code

Have a very simple API that can be used to interact with the geocoder set up in the file bcgeocoder.py

The *main.py* wraps the geocoder functionality.  Its currently pretty simple.  It 
can receive 3 args:

 - input csv file
 - name of the column in the csv file with the address string
 - output csv file
 
The script iterates through the first file, and duplicates it in the second file, with the 
addition of 3 columns containing the information retrieved from the geocoder.
 - **x coordinate** (default projection at the moment is albers but would be easy to add this as an option)
 - **y coordinate** (ditto above for projection) 
 - **precision score** (geocoders response regarding its confidence in the location)
 
 
#### testData.csv and testData.xlsx
Both of these are a set of random addresses that were harvested from google maps.  
The addresses in these files are completely random, based mostly on randomly 
grabbing addresses from various localities
 
 
#### Example run using test data:

```python
python main.py ./bcgeocoder_tests/testData.csv address outputFileWithCoords.csv
```





