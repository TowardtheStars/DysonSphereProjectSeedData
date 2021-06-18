import yaml, json

from os import listdir
from os.path import join, splitext, isfile
from typedef import protos
from data_loader import proto_types
import struct

def interprete_list(v):
    if isinstance(v, (list, tuple, dict)):
        return v
    if v is None:
        return []
    if not isinstance(v, str):
        v = hex(v)[2:]
        while len(v) % 8 != 0:
            v = "0" + v
    result = []
    for index in range(0, len(v), 8):
        result.append(int(int(v[index:index+8], base=16).to_bytes(4, byteorder='little').hex(), base=16))
        # v = v[index+4:]
    return result

def getDefaultValue(k):
    if k == 'list':
        return list()
    elif k in ('int', 'float'):
        return 0
    elif k == 'str':
        return ''

def process_yaml_data(data):
    dataArray = data['MonoBehaviour']['dataArray']
    dataType = data['MonoBehaviour']['TableName'] + "Proto"
    proto = protos[dataType]
    # for item in dataArray:
    #     for k, v in item:
    #         if proto[k] == 'list':
    #             item[k] = inteprete_list(v)

    dataArray = [{k : (v if proto[k] != 'list' else interprete_list(v)) for k, v in item.items()} for item in dataArray]
    dataArray = [{k : (v if v is not None else getDefaultValue(k)) for k, v in item.items()} for item in dataArray]
    with open(
        join(
            data_root, 
            data['MonoBehaviour']['m_Name']) + '.json', 
            'w', encoding='utf-8'
            ) as file:
        json.dump(dataArray, file, ensure_ascii=False, indent=2)

assets_root = 'prototypes'
data_root = 'data'

for name in proto_types:
    with open(join(assets_root, name + "ProtoSet.asset"), encoding='utf-8') as file:
        file.readline()
        file.readline()
        file.readline()
        data = yaml.load(file.read(), Loader=yaml.FullLoader)
        process_yaml_data(data)

