import alexandria.couch
import re

def perform_simple_search(string):
    """Does a simple search against the file index by intersecting
    the sets created by looking up each key in the search terms
    """

    keys = tokenize_string(string)
    db = alexandria.couch.getDatabase()
    sets = []
    for key in keys:
        results = db.view('files/index', key=key)
        sets.append(set([(x.id, x.value) for x in results]))
    final_set = sets[0]
    if len(sets) > 1:
        for result_set in sets[1:]:
            final_set = final_set & result_set
    return final_set

def tokenize_string(string):
    """Splits a string into a list of keys suitable for indexing/searching"""

    tokens = re.split('[^-A-Za-z0-9_]+', string.lower())
    return [x for x in tokens if x != '']
