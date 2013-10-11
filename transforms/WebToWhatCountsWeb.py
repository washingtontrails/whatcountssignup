from zope.interface import implements
from AccessControl import ClassSecurityInfo
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parseString
from xml.dom.minidom import Element
import logging

try:
    try:
        from Products.PortalTransforms.interfaces import ITransform
    except ImportError:
        from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

logger = logging.getLogger('whatcountssignup')
info = logger.info

class WebToWhatCountsWeb:
    """Transform which takes compliant HTML and produces HTML formatted expressly for use in a WhatCounts
    newsletter.
    """
    if ITransform is not None:
        implements(ITransform)
    __implements__ = itransform
    
    __name__ = 'WebToWhatCountsWeb'
    inputs=('text/html',)
    output = 'text/x-web-whatcounts'
    security = ClassSecurityInfo()
    
    DOUBLE_SMART_OPEN_QUOTE = "226,128,156,"
    DOUBLE_SMART_CLOSE_QUOTE = "226,128,157,"
    SINGLE_SMART_QUOTE = "226,128,153,"
    SINGLE_QUOTE = "39,"    
    DOUBLE_QUOTE = "34,"
    BAD_SPACE = "194,160,"
    
    def __init__(self, name=None, inputs=('text/html',), tab_width = 4):
        self.config = { 'inputs' : inputs,}
        self.config_metadata = {
            'inputs' : ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
            }
        if name:
            self.__name__ = name
    
    
    def name(self):
        return self.__name__
    
    security.declarePrivate('processDoc')
    def processDoc(self, value, data):
        """Process the text and returns a document object"""
        expatErrorResponse = '<p>Your html is not well formed. Please go back and correct.</p>'
        try:
            dom = parseString(value)
            doc = dom.documentElement
        except ExpatError:
            data.setData(expatErrorResponse)
            return None, data
        return dom, doc


    security.declarePrivate('convertDoubleSpoce')
    def convertDoubleSpace(self, value):
        """Converts double spaces to single spaces"""
        return value.replace('  ', ' ')

    
    security.declarePrivate('convertNonBreakingSpace')
    def convertNonBreakingSpace(self, value):
        """Converts non breaking spaces to single spaces"""
        value = value.replace('&nbsp;', ' ')
        return value.replace('&NBSP;', ' ')


    security.declarePrivate('convertMSQuotes')
    def convertMSQuotes(self, value):
        """Converts MS quote and double quotes into proper quotes and double quotes"""
        numString = ','.join([str(ord(ch)) for ch in value])
        #Trade opening smart quote ordinal values for double quote ordinal value
        numString = numString.replace(self.DOUBLE_SMART_OPEN_QUOTE, self.DOUBLE_QUOTE)
        #Trade closing smart quote ordinal values for double quote ordinal value
        numString = numString.replace(self.DOUBLE_SMART_CLOSE_QUOTE, self.DOUBLE_QUOTE)
        #Trade single smart quote ordinal values for quote ordinal value
        numString = numString.replace(self.SINGLE_SMART_QUOTE, self.SINGLE_QUOTE)
        return ''.join([chr(int(num)) for num in numString.split(',') if num.isdigit()])
        
        
    security.declarePrivate('cleanBreakSpaces')
    def cleanBreakSpaces(self, value):
        numString = ','.join([str(ord(ch)) for ch in value])
        numString = numString.replace(self.BAD_SPACE, '')
        return ''.join([chr(int(num)) for num in numString.split(',') if num.isdigit()])
        
    
    security.declarePrivate('convertImageFloat')
    def convertImageFloat(self, doc):
        """Converts images with class image-right or image-left to the appropriate align value"""
        imageElements = doc.getElementsByTagName('img')
        for image in imageElements:
            imageClasses = image.attributes.getNamedItem('class')
            if imageClasses:
                for CSSClass in imageClasses.value.split():
                    if CSSClass == 'image-left':
                        image.setAttribute('align', 'left')
                        break
                    if CSSClass == 'image-right':
                        image.setAttribute('align', 'right')
                        break


    security.declarePrivate('convertRelativeLinks')
    def convertRelativeLinks(self, doc, base):
        """Converts relative URL's in links and images into absolute URL's using a supplied base URL"""
        linkElements = doc.getElementsByTagName('a')
        imageElements = doc.getElementsByTagName('img')
        for image in imageElements:
            src = image.attributes.getNamedItem('src')
            if src:
                srcValue = src.value
                if 'http' not in srcValue:
                    image.setAttribute('src', base + srcValue)
        for link in linkElements:
            href = link.attributes.getNamedItem('href')
            if href:
                hrefValue = href.value
                if ('http' not in hrefValue) and ('mailto' not in hrefValue):
                    link.setAttribute('href', base + hrefValue)
            

    def convert(self, orig, data, **kwargs):
        """Performs the transformation"""
        base = kwargs['base']
        if base[-1] != "/": base += "/"
        text = '<div>' + orig + '</div>'
        
        
        #Clean double spaces
        text = self.convertDoubleSpace(text)
        #Clean non breaking spaces
        text = self.convertNonBreakingSpace(text)
        #Clean MS quote and double quotes
        text = self.convertMSQuotes(text)
        # Cleans out the spaces between break tags
        text = self.cleanBreakSpaces(text)
        
        #retrieve doc object or returns data obj on sax error
        dom, doc = self.processDoc(text, data)
        if not isinstance(doc, Element): return doc

        #img float / align properties        
        self.convertImageFloat(doc)
        #href and link relative values to absolute values
        self.convertRelativeLinks(doc, base)
        
        text = dom.toxml()
        data.setData(text)
        return data
        
        
        
    
def register():
    return WebToWhatCountsWeb()