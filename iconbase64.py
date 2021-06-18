import base64, json
from os.path import join, splitext, isfile, isdir, sep
from os import listdir
from PIL import Image
from io import BytesIO

root = 'data'
icon_root = join('raw_data', 'icons')

def recursive_import(path_stack:(list, tuple, str)):
    if isinstance(path_stack, str):
        return recursive_import(path_stack.split(sep))

    path = join(*path_stack)
    name = path_stack[-1]
    
    if isdir(path):
        result = {}
        for name1 in listdir(path):
            path_stack.append(name1)
            result.update(recursive_import(path_stack))
            path_stack.pop()
        return {name: result}
    elif isfile(path):
        name, ext = splitext(name)
        if ext == '.png':
            img = Image.open(path)
            img = img.resize((80, 80))
            # with open(path, 'rb') as file:
            #     result = base64.b64encode(file.read()).decode(encoding='UTF-8')
            # return {name: result}
            result = base64.b64encode(img.tobytes()).decode(encoding='UTF-8')
            return {name: result}
        else:
            return {}
        
target = join(root, 'icons.json')
dumpArgs = {'ensure_ascii':False, 'indent':2}


with open(target, 'w', encoding='UTF-8') as file:
    json.dump(recursive_import(icon_root), file, **dumpArgs)


