## Script (Python) "isValidContact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validate required fields in email signup
##

# All form variables follow this pattern: contact_field_name
contact_first	= context.REQUEST.get('contact_first', None)
contact_last	= context.REQUEST.get('contact_last', None)
contact_email 	= context.REQUEST.get('contact_email', None)

from Products.CMFCore.utils import getToolByName
reg_tool=getToolByName(context, "portal_registration")

if not contact_first:
	state.setError('contact_first', 'Please enter your first name', new_status='failure')

if not contact_last:
	state.setError('contact_last', 'Please enter your last name', new_status='failure')

if not contact_email:
	state.setError('contact_email', 'Please enter your email address', new_status='failure')
elif not reg_tool.isValidEmail(contact_email):
	state.setError('contact_email', "Your email address doesn\'t seem valid.  Please re-enter it.", new_status='failure')

if state.getErrors():
	state.set(portal_status_message='Please correct the errors shown.')
	
return state
