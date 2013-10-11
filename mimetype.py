from Products.MimetypesRegistry.interfaces import IClassifier
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from Products.MimetypesRegistry.common import MimeTypeException

from types import InstanceType

class WhatCountsWeb(MimeTypeItem):

    __name__   = "What Counts Web"
    mimetypes  = ('text/x-web-whatcounts',)
    extensions = ('whtml',)
    binary     = 0