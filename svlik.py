
import json
from os.path import join

data_root = 'data'
svlik_root = 'svlik'

recipe_raw = json.load(open(join(data_root, 'RecipeProtoSet.json'), encoding='utf-8'))
item_raw = json.load(open(join(data_root, 'ItemProtoSet.json'), encoding='utf-8'))

items = {}  # ID: {name:..., type:...}
recipes = [] # {s: 结果{name:, n:}, q: 配方{name: , n: 数量(不提供就是1)}, m: 设备名字, t: (s)}
recipe_types = {
    0: 'None',
    1: '冶炼设备',
    2: '化工设备',
    3: "原油精炼机",
    4: "制作台",
    5: "粒子对撞机",
    6: "Exchange",
    7: "射线接收塔",
    8: "分馏塔",
    15: "研究站"
}


for item in item_raw:
    items[item['ID']] = {
        'name': item['Name'],
        'building': item['CanBuild'] == 1
    }
    mining_from = item['MiningFrom']
    if mining_from is not None:
        recipes.append(
            {
                's': [{'name': item['Name'], 'n': 1, 'id':item['ID']}],
                'q': [],
                'm': "采矿机" if mining_from.find('矿') != -1 else "抽水机" if mining_from.find('海洋') != -1 else None,
                't': 1
            })


for recipe in recipe_raw:
    results = recipe['Results']
    result_counts = recipe['ResultCounts']
    ingres = recipe['Items']
    ingres_counts = recipe['ItemCounts']

    s = [{'name': items[results[i]]['name'], 'n': result_counts[i], 'id': results[i]} for i in range(len(results))]
    q = [{'name': items[ingres[i]]['name'], 'n': ingres_counts[i], 'id': ingres[i]} for i in range(len(ingres))]
    m = recipe_types[int(recipe["Type"])]
    recipes.append(
            {
                's': s,
                'q': q,
                'm': m,
                't': recipe['TimeSpend'] / 60
            }
        )
recipes = [v for v in recipes if v['m']]

consumables = ["空间翘曲器", "氘核燃料棒", "引力透镜", "太阳帆", "小型运载火箭", "反物质燃料棒"]

for i in range(len(recipes)):
    recipes[i]['group'] = (
        "产品" if recipes[i]['m'] == '研究站' else
        "建筑" if items[recipes[i]['s'][0]['id']]['building'] else
        "消耗品" if recipes[i]['s'] in consumables else
        "组件"
        )


orbital_append = """
        {
            s: [{ name: "重氢" }], 
            group: "组件", 
            m: "轨道采集器2", 
            q: [], 
            t: 1  
        },
        {
            s: [
                { name: "临界光子", n: 1 }
            ], 
            group: "组件", 
            m: "射线接收塔",
            q: [
                { name: "引力透镜", n: 0.025 }
            ], 
            t: 6
        },
        {
            s: [
                { name: "氢" }
            ], 
            group: "组件", 
            m: "轨道采集器", 
            q: [], 
            t: 1
        },
        {
            s: [
            { name: "氢" }
            ], 
            group: "组件", 
            m: "轨道采集器2", 
            q: [], 
            t: 1
        }, 
        {
            s: [{name: "可燃冰"}], 
            group: "组件", 
            m: "轨道采集器", 
            q: [], 
            t: 1
        }
"""
tab = '    '

with open(join(svlik_root, 'recipes.js'), mode='w') as file:
    file.writelines('var data = [\n')
    for recipe in recipes:
        file.writelines(tab + '{\n')
        file.writelines(tab * 2 + 's: [\n')
        for result in recipe['s']:
            file.writelines(tab * 3 + '{\n')
            file.writelines(tab * 4 + 'name: "{name}",\n'.format(**result))
            file.writelines(tab * 4 + 'n: {n}\n'.format(**result))
            file.writelines(tab * 3 + '},\n')
        file.writelines(tab * 2 + '],\n')
        file.writelines(tab * 2 + 'q: [\n')
        for ingre in recipe['q']:
            file.writelines(tab * 3 + '{\n')
            file.writelines(tab * 4 + 'name: "{name}",\n'.format(**ingre))
            file.writelines(tab * 4 + 'n: {n}\n'.format(**ingre))
            file.writelines(tab * 3 + '},\n')
        file.writelines(tab * 2 + '],\n')
        file.writelines(tab * 2 + 'm: "{m}",\n'.format(**recipe))
        file.writelines(tab * 2 + 't: {t},\n'.format(**recipe))
        file.writelines(tab * 2 + 'group: "{group}"\n'.format(**recipe))
        file.writelines(tab + '},\n')


    file.write(orbital_append)
    file.writelines('];\n')