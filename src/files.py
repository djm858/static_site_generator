import os
import shutil

def copy_files(from_path, to_path):
    if not os.path.exists(from_path):
        raise Exception('path to copy from does not exist')
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    os.mkdir(to_path)
    if os.path.exists(from_path):
        for item in os.listdir(from_path):
            item_from_path = os.path.join(from_path, item)
            item_to_path = os.path.join(to_path, item)
            print(f" * {item_from_path} -> {item_to_path}")
            if os.path.isfile(item_from_path):
                shutil.copy(item_from_path, item_to_path)
            else:
                copy_files(item_from_path, item_to_path)
