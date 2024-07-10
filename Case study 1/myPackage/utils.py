import os
import glob
import time

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

def save_feedback_to_disk(feedback_obj):
    feedback = ""
    for attr in dir(feedback_obj): # dir will find the attributes in an object (object.name etc)
        if not attr.startswith('__') and not callable(getattr(feedback_obj, attr)):
            feedback += f"{attr}: {getattr(feedback_obj, attr)}\n"
        # getaatr(object, fieldName) returns the contents of the field (LIke object.fieldName)
        # callable() checks if the object can be called (Like Javascript function-objects)
    feedback_dir = 'feedback'
    print(feedback, flush=True)
    if not os.path.exists(feedback_dir):
        os.makedirs(feedback_dir)
        print(f"Directory {feedback_dir} created.")
    else:
        print(f"Directory {feedback_dir} already exists.")
    files = glob.glob(os.path.join(feedback_dir, '*'))
    if len(files) >= 5:
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)
        print(f"Deleted oldest file: {oldest_file}")
    new_file_name = os.path.join(feedback_dir, f"feedback_{int(time.time())}.txt")
    with open(new_file_name, 'w') as file:
        file.write(feedback)
    print(f"Saved feedback to {new_file_name}")
    return True