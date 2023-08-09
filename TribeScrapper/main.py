import requests
from time import sleep

URL = "https://api.scryfall.com/cards/search"


def dotaz_tribe_creature(tribe):
    count = 0
    query = '(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND t:creature AND f:commander'
    r = requests.get(url=URL, params={'q': query})
    # print(query)
    # print(r.url)
    data = r.json()
    if r.status_code == 200:
        count = data['total_cards']
    return count


def dotaz_tribe_commander(tribe):
    count = 0
    query = '(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND t:creature AND t:legendary AND f:commander'
    r = requests.get(url=URL, params={'q': query})
    # print(query)
    # print(r.url)
    data = r.json()
    # print(data)
    if r.status_code == 200:
        count = data['total_cards']
    return count


def dotaz_tribe_nonc(tribe):
    count = 0
    query = '(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND -t:creature AND f:commander'
    r = requests.get(url=URL, params={'q': query})
    # print(r.json())
    # print(query)
    # print(r.url)
    data = r.json()
    if r.status_code == 200:
        count = data['total_cards']
    return count


TList = open('tribesList.txt', 'r') # https://yawgatog.com/resources/magic-rules/#R2053m

output = open('Tribes-pocty-23-08-09.csv', 'w+')

# tribe = 'cleric'
# print('(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND t:creature AND f:commander')
# print(dotaz_tribe_creature('cleric'))
# print('(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND t:creature AND t:legendary AND f:commander')
# print(dotaz_tribe_commander('cleric'))
# print('(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND -t:creature AND f:commander')
# print(dotaz_tribe_nonc('cleric'))

for tr in TList.readlines():
    pocet_creature = dotaz_tribe_creature(tr.rstrip())
    sleep(0.1)
    # pocet_commander = dotaz_tribe_commander(tr.rstrip())
    # sleep(0.1)
    pocet_nonc = dotaz_tribe_nonc(tr.rstrip())
    print(f'{tr.rstrip()}:{pocet_creature}:{pocet_nonc}')
    output.write(f'{tr.rstrip()};{pocet_creature};{pocet_nonc}\n')
    sleep(0.1)

print('Hotovo.')
TList.close()
output.close()
