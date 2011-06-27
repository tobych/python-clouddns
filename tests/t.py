# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
import clouddns
import os
import sys

US_RCLOUD_USER = os.environ.get("US_RCLOUD_USER")
US_RCLOUD_KEY = os.environ.get("US_RCLOUD_KEY")
CNX = None

if not US_RCLOUD_KEY or not US_RCLOUD_USER:
    print "API Keys env not defined"
    sys.exit(1)


def auth():
    global CNX
    if not CNX:
        CNX = clouddns.connection.Connection(US_RCLOUD_USER, US_RCLOUD_KEY)
    return CNX


def test():
    cnx = auth()

    # Domain list
    all_domains = cnx.get_domains()
    # __getitem__
    domain = all_domains[0]

    # __getslice__
    domain = all_domains[0:1][0]
    # __contains__
    assert(str(domain) in all_domains)
    # __len__
    len(all_domains)

    for x in all_domains:
        if str(x).startswith("chmoutest"):
            cnx.delete_domain(x.id)

    # Create Domain
    domain_created = cnx.create_domain(name="chmoutesting.com",
                                       ttl=300,
                                       emailAddress="foo@foo.com")

    # Get domain by id.
    sDomain = cnx.get_domain(domain_created.id)
    assert(sDomain.id == domain_created.id)

    # Get domain by name.
    sDomain = cnx.get_domain(name="chmoutesting.com")
    assert(sDomain.id == domain_created.id)

    domain = domain_created

    ttl = 500
    # Update Domain
    domain.update(ttl=ttl)

    assert(domain.ttl == ttl)

    # Create Record
    newRecord = \
        domain.create_record("test1.chmoutesting.com", "127.0.0.1", "A")

    # Get Record by ID
    record = domain.get_record(newRecord.id)
    assert(record.id == newRecord.id)

    # Get Record by name
    record = domain.get_record(name="test1.chmoutesting.com")
    assert(record.id == newRecord.id)

    # Modify Record data
    newRecord.update(data="127.0.0.2", ttl=1300)

    # Delete Record
    domain.delete_record(newRecord.id)

test()
