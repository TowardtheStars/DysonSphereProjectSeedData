import json
from os.path import join

data = join('data', 'ThemeProtoSet.json')
with open(data, encoding='UTF-8') as file:
    data = json.load(file)
data = data['dataArray']['Array']['data']

theme_ionheight = {}
for theme in data:
    theme_ionheight[theme['DisplayName']] = theme['IonHeight']

print(json.dumps(theme_ionheight, ensure_ascii=False, indent=2))


