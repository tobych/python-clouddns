# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
from clouddns.authentication import Authentication
import os

auth = Authentication(os.environ.get('US_RCLOUD_USER'),
                      os.environ.get('US_RCLOUD_KEY'))

print auth.authenticate()
