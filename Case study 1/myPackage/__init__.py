from .utils import *
import json

class Person:
    target1 = 1
    def __init__(self, name):
        self.target2 = name

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.target3 = "change this"