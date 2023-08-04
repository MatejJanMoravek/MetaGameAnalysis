import os
import logging
import requests
from time import sleep

URL = "https://api.scryfall.com/cards/search"


def add_colors(colors, list):
    for item in list:
        if item not in colors:
            colors.append(item)


def dotaz_color(cardname):
    cardcolors = []
    query = f'!"{cardname}"'  # '(fo:/\\b(' + tribe + '|' + tribe + 's)\\b/ OR t:' + tribe + ') AND -t:creature AND f:commander'
    r = requests.get(url=URL, params={'q': query})
    app_log.debug(cardname)
    # app_log.debug(r.json())
    # print(query)
    # print(r.url)
    if r.status_code == 200:
        data = r.json()
        if 'card_faces' in data:
            app_log.debug(data['data'][0]['card_faces'][0]['colors'])
            app_log.debug(data['data'][0]['card_faces'][1]['colors'])
            add_colors(cardcolors, data['data'][0]['card_faces'][0]['colors'])
            add_colors(cardcolors, data['data'][0]['card_faces'][1]['colors'])
        else:
            if 'colors' in data['data'][0]:
                app_log.debug(data['data'][0]['colors'])
                add_colors(cardcolors, data['data'][0]['colors'])
    return cardcolors


if __name__ == '__main__':
    output_dir = os.path.join(os.getcwd(), '..', 'vysledky')

    os.makedirs(output_dir, exist_ok=True)

    # Nastaveni Logovani ---------------------------------------------------
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s',
                                      datefmt='%d-%m-%Y %H:%M:%S')

    # File to log to
    logFile = os.path.join(output_dir, 'MetaAnalyza.log')

    # Setup File handler
    file_handler = logging.FileHandler(logFile)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Setup Stream Handler (i.e. console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)

    # Get our logger
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)

    # Add both Handlers
    app_log.addHandler(file_handler)
    app_log.addHandler(stream_handler)

    # ===============================================================================================

    cards = {}
    colors = {}
    CardsNo = open(os.path.join(os.getcwd(), 'CardsNo.csv'), 'w+', errors='ignore', encoding='cp1250')
    Colors = open(os.path.join(os.getcwd(), 'Colors.csv'), 'w+', errors='ignore', encoding='cp1250')

    # Nacteme postupne vsechny sql s vkladanymi zpravami a spustime je
    for sql_soubor in os.listdir(os.path.join(os.getcwd(), 'decklists')):
        # msgFile.write(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ';' + sql_soubor.split('.')[0] + ';')
        decklist = open(os.path.join(os.getcwd(), 'decklists', sql_soubor), 'r')
        logging.info(f'Kontroluji deck {decklist.name}...')

        deckcolors = []

        for line in decklist:
            cardname = line.strip()
            logging.debug(cardname)
            if cardname not in cards:
                cards.update({cardname: 1})
            else:
                cards[cardname] += 1

            add_colors(deckcolors, dotaz_color(line))

        app_log.info(decklist.name + ' > ' + ''.join(deckcolors))
        Colors.write(decklist.name + '; ' + ''.join(deckcolors) + '\n')
        decklist.close()

    logging.info('Vysledne pocty karet > 1...')
    logging.info('---------------------------------------------------------------')
    for item in cards:
        if cards[item] > 1:
            logging.info(f'{item} : {cards[item]}')
            CardsNo.write(f'{item}; {cards[item]}\n')
    CardsNo.close()
    Colors.close()
