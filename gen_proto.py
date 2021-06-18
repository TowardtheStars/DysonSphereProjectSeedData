import json
from os.path import join, isfile, splitext

def extract_class_code(data_instance, class_name):
    """
Extract Proto Class Code from data instance, Class name is required
Data instance must be read from json file
    """
    header = \
    """
class {class_name}(object):
    \"\"\"
    This class was generated from an json instance
    \"\"\"

    def __init__(self, **kwargs):
    """.format(class_name=class_name)

    ending = \
    """
        for k, v in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, v)
    """
    property_dict = {}
    # dump property names and default values
    def is_array(v):
        return (isinstance(v, dict) and "Array" in v.keys()) or isinstance(v, (list, tuple))

    for k, v in data_instance.items():
        if is_array(v):
            property_dict[k] = []
        elif isinstance(v, (int, float)):
            property_dict[k] = 0
        elif isinstance(v, (str,)):
            property_dict[k] = '\'\''
        elif isinstance(v, bool):
            property_dict[k] = False

    # generate code
    property_codes = [
        '        self.{k} = {v}'.format(k=k, v=v) for k, v in property_dict.items()
    ]

    code = '\n'.join(property_codes)
    code = '\n'.join([header, code, ending])

    return code


root = 'data'

def get_instance_name_pair(name):
    with open(join(root, '{name}ProtoSet.json'.format(name=name)), encoding='UTF-8') as file:
        instance = json.load(file)['dataArray']['Array']['data'][0]
    return instance, name + "Proto"

proto_types = [
    'Item',
    'Recipe',
    'Tech',
    'Theme',
    'Vein',
    'String'
]

with open(join('data', 'protos.py'), 'w', encoding='UTF-8') as file:

    for name in proto_types:
        instance, name = get_instance_name_pair(name)
        file.write(extract_class_code(instance, name))
        file.write('\n\n\n')

