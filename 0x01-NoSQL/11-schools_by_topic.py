#!/usr/bin/env python3

"""
a Python function that returns the list of school having a specific topic:

Prototype: def schools_by_topic(mongo_collection, topic):
mongo_collection will be the pymongo collection object
topic (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic:
    """
    result = []
    cursor = mongo_collection.find({"topics": {"$in": [topic]}})
    for doc in cursor:
        result.append(doc)
    return result
