# -*- encoding: utf-8 -*-
__author__ = "Chmouel Boudjnah <chmouel@chmouel.com>"


class Record(object):
    def __init__(self, domain, record=None, name=None):
        self.domain = domain

        if record:
            self.data = record['data']
            self.name = record['name']
            self.id = record['id']
            self.type = record['type']
            self.ttl = record['ttl']
        else:
            self.data = None
            self.name = None
            self.id = None
            self.ttl = 1800
            self.type = None


class RecordResults(object):
    """
    An iterable results set records for Record.

    This class implements dictionary- and list-like interfaces.
    """
    def __init__(self, domain, records=None):
        if records is None:
            records = []
        self._names = []
        self._records = []
        for obj in records:
                self._names.append(obj['name'])
                self._records.append(obj)
        self.domain = domain

    def __getitem__(self, key):
        return Record(self.domain, record=self._records[key])

    def __getslice__(self, i, j):
        return [Record(self.domain, record_id=k) \
                    for k in self._records[i:j]]

    def __contains__(self, item):
        return item in self._records

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        return 'RecordResults: %s records' % len(self._records)
    __str__ = __repr__

    def index(self, value, *args):
        """
        returns an integer for the first index of value
        """
        return self._names.index(value, *args)

    def count(self, value):
        """
        returns the number of occurrences of value
        """
        return self._names.count(value)
