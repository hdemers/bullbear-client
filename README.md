Description
===========

This is an example client endpoint written in python for receiving real-time
updates from [BullBear](www.bullbear.ca).

BullBear uses Amazon Simple Notification Service (SNS) to send update, in
real-time, for each processed document and for each commodity update.

You must have a webserver listening on some port for POST requests. This is
easily achievable through a library like [web.py](http://webpy.org/).

Requirements
------------
 - python
 - [web.py](http://webpy.org/)
 - simplejson


Data format
-----------
BullBear sends JSON formated data. There are two endpoints:

 - the *documents* endpoint
 - the *commodities* endpoint

### Document endpoint
The first will receive updates each time a document is analyzed. It contains
information about the title, the URL, and the commodities mentionned in the
document. The format of a document update is:

    {
        'id': 'f90c28d4-f868-430d-867e-142e3c7ca143',
        'title': 'Today's Copper and Gold Outlook', 
        'entities': [
            {'key': 'copper', 'value': 100, 'nbull': 1, 'nbear': 0},
            {'key': 'gold', 'value': -100, 'nbull': 0, 'nbear': 1},
        ], 
        'url': 'http://example.com/copper-gold-outlook.html',
        'source': 'example.com', 
        'published': '2011-11-24T19:51:54Z',
        'added': '2011-11-24T19:52:07Z', 
        'analyzed': '2011-11-24T19:52:11Z', 
        'author': 'Mr Author', 
        'leading': True, 
        'rights': 'Mr Author', 
        'acl': {
            'owner': 'rw', 
            'all': 'r'
        }, 
        'clusters': [], 
        'status': 2, 
    }

Most of the above fields should be self-explanatory. 

### Commodities endpoint
The second endpoint, commodities, receives updates each time a commodity is
updated. It contains the bullbear index, the change, the frequency, etc.

The format of a commodity update is:

    {
        'key': 'crude_oil',
        'name': 'Crude Oil',
        'depth': 1,
        'parent': 'energy',
        'latest': {
            'value': 67,
            'nbull': 24,
            'nbear': 2,
            'change': 1,
            'frequency': 3.5,
            'buzz': False,
        }
    }

The fields are:

 - **key**: the commodity key value, similar to the name but machine
   processable.
 - **name**: the name of the commodity.
 - **depth**: the depth of that commodity, in the overall commodity tree. Crude
   oil is under Energy, thus has a depth of 1. Energy would have a depth of 0.
 - **parent**: the parent commodity. Value 'top', means no parent.
 - **value**: the bullbear index: between -100 and +100.
 - **nbull**: the number of bull mentions in the last 20 documents
 - **nbear**: the number of bear mentions in the last 20 documents
 - **change**: the change of the bullbear index computed over the last 24 hours.
   Possible values are -1 means a negative trend, +1 means a positive trend, 0
   means mostly stable.
 - **frequency**: the number of documents per hour received in the last 24 hours.
 - **buzz**: unused for now. Always False.
