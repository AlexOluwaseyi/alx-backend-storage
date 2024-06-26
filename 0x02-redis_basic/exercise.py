#!/usr/bin/env python3

"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns
a string. The method should generate a random key (e.g. using
uuid), store the input data in Redis using the random
key and return the key.

Type-annotate store correctly. Remember that data can
be a str, bytes, int or float.
"""

import redis
from functools import wraps
from uuid import uuid4
from typing import Callable, Union

union = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """incrememter"""
        # key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and outputs
    for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def historian(self, *args):
        """
        decorator to store the history of inputs and outputs
        for a particular function.

        Everytime the original function will be called, we
        will add its input parameters to one list in
        redis, and store its output into another list.
        """
        self._redis.rpush(inputs, str(args))

        # Calls the method and saves the output in result
        result = method(self, *args)

        self._redis.rpush(outputs, str(result))
        return result

    return historian


class Cache:
    """
    Class Definition for Cache for redis
    """
    def __init__(self):
        """
        the __init__ method, store an instance of the Redis
        client as a private variable named _redis
        (using redis.Redis()) and flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid), store
        the input data in Redis using the random key and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> union:
        """
        a get method that take a key string argument and an
        optional Callable argument named fn. This callable will
        be used to convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve data from the cache and convert to string
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieve data from the cache and convert to integer
        """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """
    Implement a replay function to display the
    history of calls of a particular function.
    """

    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    # Retrieve inputs and outputs from Redis
    input_list = method.__self__._redis.lrange(inputs, 0, -1)
    output_list = method.__self__._redis.lrange(outputs, 0, -1)

    # Zip inputs and outputs together
    zipped_data = list(zip(input_list, output_list))

    # Print the history of calls
    print("{} was called {} times:".format(key, len(zipped_data)))
    for input_data, output_data in zipped_data:
        input_str = input_data.decode("utf-8")
        output_str = output_data.decode("utf-8")
        print("{}(*{}) -> {}".format(key, input_str, output_str))
