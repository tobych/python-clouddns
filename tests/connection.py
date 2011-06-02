# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
import os
from clouddns.connection import Connection

c = Connection(os.environ.get('US_RCLOUD_USER'),
                  os.environ.get('US_RCLOUD_KEY'))

#print c.list_domains_info()
d = c.get_all_domains()
x = d[0]
print x.list_records()
