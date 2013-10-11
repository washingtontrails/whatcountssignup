# Register our skins directory - this makes it available via portal_skins.
# register our profile

from Products.CMFCore.DirectoryView import registerDirectory

from Products.GenericSetup import EXTENSION, profile_registry
from Products.CMFPlone.interfaces import IPloneSiteRoot

from config import GLOBALS
registerDirectory('skins', GLOBALS)

profile_registry.registerProfile(
                    'whatcountssignup',                           # name
                    'WhatCounts Signup',                           # title
                    'Extension profile for WhatCounts Signup',     # description
                    'profile/default',                            # path
                    'whatcountssignup',                           # product=None
                    EXTENSION,                                    # profile_type=BASE
                    for_=IPloneSiteRoot                           # for_=None
                    )

profile_registry.registerProfile(
                    'whatcountssignup-uninstall',                 # name
                    'WhatCounts Signup Uninstall',                # title
                    '"Uninstall" profile for WhatCounts Signup',  # description
                    'profile/uninstalled',                        # path
                    'whatcountssignup',                           # product=None
                    EXTENSION,                                    # profile_type=BASE
                    for_=IPloneSiteRoot                           # for_=None
                    )
