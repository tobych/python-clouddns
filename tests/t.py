# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"
import clouddns
import os

US_RCLOUD_USER = os.environ.get("US_RCLOUD_USER")
US_RCLOUD_KEY = os.environ.get("US_RCLOUD_KEY")
CNX = None

def auth():
    global CNX
    if not CNX:
        CNX = clouddns.connection.Connection(US_RCLOUD_USER, US_RCLOUD_KEY)
    return CNX


def test_create_delete(cnx):
    # CREATE
    domain_created = cnx.create_domain(name="chmoutest21.com",
                                       ttl=300,
                                       emailAddress="foo@foo.com")
    # Delete
    cnx.delete_domain(domain_created.id)


def test():
    cnx = auth()
    #test_create_delete(cnx)

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
            print "Cleaning: %s" % (x.name)
            cnx.delete_domain(x.id)

    # Create Domain
    domain_created = cnx.create_domain(name="chmoutesting.com",
                                       ttl=300,
                                       emailAddress="foo@foo.com")

    domain = domain_created

    ttl = 500
    # Update Domain
    domain.update(ttl=ttl)

    assert(domain.ttl == ttl)

    # Get All records
    records = domain.get_records()
    record = records[0]

    # Get Record by ID
    record_id = record.id
    record = domain.get_record(record_id)

    from IPython.Shell import IPShellEmbed;IPShellEmbed()()
    
test()
