from Products.CMFCore.utils import getToolByName
from Products.whatcountssignup.config import GLOBALS
from Products.whatcountssignup.mimetype import WhatCountsWeb

from types import InstanceType

from zope.component import getUtility, getMultiAdapter
from zope.app.container.interfaces import INameChooser

from plone.app.portlets.portlets import classic
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

class WhatCountsSignupGenerator:
    def addPortletToCol(self, portal):
        """Utility method to add a portlet to a column"""
        # this code borrowed from plone.app.portlets.utils' convert_legacy_portlets 
        right = getUtility(IPortletManager, name='plone.rightcolumn')
        rightAssignable = getMultiAdapter((portal, right),
                                           IPortletAssignmentMapping).__of__(portal)
        rightChooser = INameChooser(rightAssignable)
        newPortlet = classic.Assignment('portlet_email_capture', 'portlet')
        rightAssignable[rightChooser.chooseName(None, newPortlet)] = newPortlet

    def removePortlet(self, portal):
        """Remove the portlet from both columns, if it's still there"""
        # not sure if this is the best way to do things, but i think it works
        for side in ('left', 'right'):
            util = getUtility(IPortletManager, name='plone.%scolumn' % side)
            portlets = getMultiAdapter((portal, util), IPortletAssignmentMapping).__of__(portal)
            for name, val in portlets.items():
                if val.title == 'portlet_email_capture':
                    del portlets[name]

    def registerMimeType(self, portal, out, mimetype):
        if type(mimetype) != InstanceType:
            mimetype = mimetype()
        mimetypes_registry = getToolByName(portal, 'mimetypes_registry')
        mimetypes_registry.register(mimetype)
        out.append("Registered mimetype %s" % mimetype)

    def unregisterMimeType(self, portal, out, mimetype):
        if type(mimetype) != InstanceType:
            mimetype = mimetype()
        mimetypes_registry = getToolByName(portal, 'mimetypes_registry')
        mimetypes_registry.unregister(mimetype)
        out.append("Unregistered mimetype %s" % mimetype)

    def registerTransform(self, portal, out, name, module):
        transforms = getToolByName(portal, 'portal_transforms')
        if name not in transforms.objectIds():
            transforms.manage_addTransform(name, module)
            out.append("Registered transform %s" % name)
        else:
            out.append("Didn't registered transform %s (already existed)" % name)

    def unregisterTransform(self, portal, out, name):
        transforms = getToolByName(portal, 'portal_transforms')
        try:
            transforms.unregisterTransform(name)
            out.append("Removed transform %s" % name)
        except AttributeError:
            out.append("Could not remove transform %s (not found)" % name)

    def removeSkinLayer(self, portal, out):
        """In our profile we add the whatcounts layer to Plone Default.
        I don't believe GS allows you to REMOVE this later, so we're doing it in code"""
        skinstool = getToolByName(portal, 'portal_skins')

        for skinName in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skinName)
            path = [i.strip() for i in  path.split(',')]
            if 'whatcounts' in path:
                prev = len(path)
                path.remove('whatcounts')
                if prev != len(path):
                    path = ','.join(path)
                    skinstool.addSkinSelection(skinName, path)
        out.append("Removed whatcounts layer from all skin selections")
        

def finalInstallSteps(context):
    """
    The last bit of code that runs as part of this setup profile.
    """
    if context.readDataFile('whatcountssignup_final.txt') is None:
        return
    out = ["",]
    site = context.getSite()
    gen = WhatCountsSignupGenerator()
    out.append("Installing WhatCounts Signup")
    gen.addPortletToCol(site)
    gen.registerMimeType(site, out, WhatCountsWeb)
    gen.registerTransform(site, out, 'WebToWhatCountsWeb', 'Products.whatcountssignup.transforms.WebToWhatCountsWeb')
    return "\n--".join(out)
    
def uninstallSteps(context):
    """Clean up the things that Generic Setup can't handle for us
    (this is) called at the end of the "uninstalled" profile"""
    if context.readDataFile('whatcountssignup_uninstall.txt') is None:
        return

    out = ["",]
    site = context.getSite()
    gen = WhatCountsSignupGenerator()
    out.append("Uninstalling WhatCounts Signup")
    gen.removePortlet(site)
    gen.unregisterTransform(site, out, 'WebToWhatCountsWeb')
    gen.unregisterMimeType(site, out, WhatCountsWeb)
    gen.removeSkinLayer(site, out)
    return "\n--".join(out)
