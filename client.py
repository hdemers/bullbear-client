#!/usr/bin/env python
"""Example webserver endpoint using the development server of web.py.

Use a real web server for production. See for example
http://webpy.org/install#prod 
"""
import urllib2
import web
import simplejson as json

class Commodities(object):
    """Receives commodity updates from SNS through POST.
    """
    def POST(self, key):
        try:
            data = json.loads(web.data())
            # Is this an SNS Notification?
            notif_type = data.get('Type', '')
            # Commodity updates are received with a type 'Notification'.
            if notif_type == "Notification":
                commodities = json.loads(data['Message'])
                for commodity in commodities:
                    print "Commodity received: %s" % commodity
            # SNS will verify this endpoint by sending a
            # SubscriptionConfirmation. To which you must answer by GETing the
            # given 'SubscribeURL'.
            elif notif_type == "SubscriptionConfirmation":
                print "Received SNS subscription confirmation to topic %s" % (
                      data['TopicArn'])
                urllib2.urlopen(data['SubscribeURL'])
            else:
                print "Unsupported notification type %s" % notif_type

        except Exception, exception:
            print exception

class Documents(object):
    """Receives document updates from SNS through POST.
    """
    def POST(self, doc_id):
        try:
            data = json.loads(web.data())
            # Is this an SNS Notification?
            notif_type = data.get('Type', '')
            # Document updates are received with a type 'Notification'.
            if notif_type == "Notification":
                docs = json.loads(data['Message'])
                for doc in docs:
                    print "Document received: %s" % doc
            # SNS will verify this endpoint by sending a
            # SubscriptionConfirmation. To which you must answer by GETing the
            # given 'SubscribeURL'.
            elif notif_type == "SubscriptionConfirmation":
                print "Received SNS subscription confirmation to topic %s" % (
                    data['TopicArn'])
                urllib2.urlopen(data['SubscribeURL'])
            else:
                print "Unsupported notification type %s" % notif_type

        except Exception, exception:
            print exception

# This is a regular expression for matching a UUID.
uuid_re = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

# URL mappings
urls = ("^/documents/?(%s)?/?$" % uuid_re, "Documents",
        "^/commodities/?(.*)/?$", "Commodities",
       )

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
