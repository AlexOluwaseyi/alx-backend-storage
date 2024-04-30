#!/usr/bin/env python3

"""
A Python function that lists all documents in a collection:

Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""

from pymongo import MongoClient
client = MongoClient()


def list_all(mongo_collection):
    """
    Lists all documents in a collection:
    Checks if collection is empty using count_documents
    """
    if mongo_collection.count_documents({}) == 0:
        return []

    for docx in mongo_collection.find():
        return docx
