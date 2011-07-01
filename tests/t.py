# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
import clouddns
import os
import sys

REGION = "UK"

US_RCLOUD_USER = os.environ.get("US_RCLOUD_USER")
US_RCLOUD_KEY = os.environ.get("US_RCLOUD_KEY")

UK_RCLOUD_USER = os.environ.get("UK_RCLOUD_USER")
UK_RCLOUD_KEY = os.environ.get("UK_RCLOUD_KEY")

CNX = None
DOMAIN = "chmoutesting-%s.com" % (REGION)
FORCE_DBG = True


def dbg(msg, force_dbg=FORCE_DBG):
    if ('PYTHON_CLOUDDNS_DEBUG' in os.environ and \
            os.environ['PYTHON_CLOUDDNS_DEBUG'].strip()) or \
            force_dbg:
        print "****** %s ******" % msg

if not US_RCLOUD_KEY or not US_RCLOUD_USER:
    print "API Keys env not defined"
    sys.exit(1)


def auth():
    global CNX
    if not CNX:
        if REGION == "US":
            dbg("Authing to US cloud")
            CNX = clouddns.connection.Connection(US_RCLOUD_USER, US_RCLOUD_KEY)
        elif REGION == "UK":
            dbg("DBG: Authing to UK cloud")
            CNX = clouddns.connection.Connection(
                UK_RCLOUD_USER,
                UK_RCLOUD_KEY,
                authurl=clouddns.consts.uk_authurl)
    return CNX


def test():
    cnx = auth()

    # Domain list
    all_domains = cnx.get_domains()
    if all_domains:
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
                dbg("Deleting domain: %s" % x.name)
                cnx.delete_domain(x.id)

    # Create Domain
    dbg("Creating domain: %s" % (DOMAIN))
    domain_created = cnx.create_domain(name=DOMAIN,
                                       ttl=300,
                                       emailAddress="foo@foo.com")

    # Get domain by id.
    dbg("GETting domain by ID: %s" % (domain_created.id))
    sDomain = cnx.get_domain(domain_created.id)
    assert(sDomain.id == domain_created.id)

    # Get domain by name.
    dbg("GETting domain by Name: %s" % (DOMAIN))
    sDomain = cnx.get_domain(name=DOMAIN)
    assert(sDomain.id == domain_created.id)

    domain = domain_created

    ttl = 500
    # Update Domain
    domain.update(ttl=ttl)

    record = "test1.%s" % (DOMAIN)
    # Create Record
    dbg("Creating Record: %s" % (record))
    newRecord = \
        domain.create_record(record, "127.0.0.1", "A")

    # Get Record by ID
    dbg("Get Record By ID: %s" % (newRecord.id))
    record = domain.get_record(newRecord.id)
    assert(record.id == newRecord.id)

    # Get Record by name
    dbg("Get Record By Name: %s" % (record))
    record = domain.get_record(name=record.name)
    assert(record.id == newRecord.id)

    # Modify Record data
    newRecord.update(data="127.0.0.2", ttl=1300)

    # Delete Record
    domain.delete_record(newRecord.id)

test()
