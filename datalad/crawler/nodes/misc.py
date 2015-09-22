# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Various small nodes
"""

from datalad.support.network import get_url_deposition_filename, get_url_straight_filename
from datalad.utils import updated

class Sink(object):
    """A rudimentary node to sink/collect all the data passed into it
    """

    # TODO: add argument for selection of fields of data to keep
    def __init__(self):
        self.data = []

    def get_fields(self, *keys):
        return [(d[k] for k in keys) for d in self.data]

    def __call__(self, **data):
        # ??? for some reason didn't work when I made entire thing a list
        self.data.append(data)
        yield data


class rename(object):
    """Rename fields in data for subsequent nodes
    """
    def __init__(self, mapping):
        """

        Use OrderedDict when order of remapping matters
        """
        self.mapping = mapping

    def __call__(self, **data):
        # TODO: unittest
        data = data.copy()
        for from_, to_ in self.mapping:
            if from_ in data:
                data[to_] = data.pop(from_)
        yield data


class assign(object):
    def __init__(self, assignments, interpolate=False):
        self.assignments = assignments
        self.interpolate = interpolate

    def __call__(self, **data):
        for k, v in self.assignments.items():
            data[k] = v % data if self.interpolate else v
        yield data

#class prune(object):

def get_url_filename(**data):
    yield updated(data, {'filename': get_url_straight_filename(data['url'])})

def get_deposition_filename(**data):
    """For the URL request content filename deposition
    """
    yield updated(data, {'filename': get_url_deposition_filename(data['url'])})