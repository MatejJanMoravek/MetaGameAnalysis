import os
import json
import datetime
import sys
import shutil
import glob
import logging

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
    file_handler.setLevel(logging.DEBUG)

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

    # Nacteme postupne vsechny sql s vkladanymi zpravami a spustime je
    for sql_soubor in os.listdir(os.path.join(os.getcwd(),'decklists')):
        # msgFile.write(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ';' + sql_soubor.split('.')[0] + ';')
        decklist = open(os.path.join(os.getcwd(), 'decklists', sql_soubor), 'r')
        logging.info(f'Kontroluji deck {decklist.name}...')

        deckcolors = ''

        for line in decklist:
            cardname = line.strip()
            logging.debug(cardname)
            if cardname not in cards:
                cards.update({cardname: 1})
            else:
                cards[cardname] += 1

            # checkCardColor(cardname, deckcolors)

        decklist.close()

    logging.info('Vysledne pocty karet > 1...')
    logging.info('---------------------------------------------------------------')
    for item in cards:
        if cards[item] > 1:
            logging.info(f'{item} : {cards[item]}')
            CardsNo.write(f'{item}; {cards[item]}\n')
    CardsNo.close()