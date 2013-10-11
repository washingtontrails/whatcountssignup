## Script (Python) "process_signup"
##bind container=container
##bind context=context
##bind namespace=
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=used to post form values to WhatCounts 
##

request = container.REQUEST
base_url = 'http://www.whatcounts.com/bin/listctrl'
args = {}
from ZTUtils import make_query 

for key in request.keys():
	if key[:8]=='contact_' and request[key]:
		args[key[8:]] = request[key].replace('#','')

url = '%s?%s' % (base_url, make_query(args))

state.setNextAction('redirect_to:string:%s' % url)

# Always make sure to return the ControllerState object
return state
