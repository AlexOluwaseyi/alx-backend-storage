#!/usr/bin/env python3

"""
a Python function that returns all students sorted by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    pipeline = [{"$addFields": {"averageScore": {"$avg": "$topics.score"}}},
                {"$sort": {"averageScore": -1}}]

    return list(mongo_collection.aggregate(pipeline))
