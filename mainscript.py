import requests
import os
import json
import time

# Configurazione
API_KEY = '320466b042c54d53b58a1fcdb929a2f8'  # Inserisci qui la tua chiave API Twelve Data
OUTPUT_DIR = 'data'  # Cartella dove verranno salvati i JSON
INPUT_FILE = 'customSEP500.json'  # File JSON contenente i simboli e gli exchange

# Crea la cartella di output se non esiste
os.makedirs(OUTPUT_DIR, exist_ok=True)

def carica_titoli(file):
    """Carica i dati dei titoli da un file JSON."""
    try:
        with open(file, 'r') as f:
            titoli = json.load(f)
        return titoli
    except FileNotFoundError:
        print(f"Errore: File {file} non trovato.")
        return []
    except json.JSONDecodeError as e:
        print(f"Errore nel decodificare il file JSON: {e}")
        return []

def recupera_dati_titolo(symbol, exchange):
    """Recupera i dati a intervallo di 1 giorno per il simbolo e l'exchange specificati."""
    url = f'https://api.twelvedata.com/time_series'
    params = {
        'symbol': symbol,
        'exchange': exchange,
        'interval': '1day',
        'apikey': API_KEY,
        'outputsize': 1000  # Recupera fino a 1000 giorni di dati
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Errore nel recupero dei dati per {symbol} su {exchange}: {response.status_code}")
        return None

    data = response.json()
    if 'values' not in data:
        print(f"Nessun dato trovato per {symbol} su {exchange}: {data}")
        return None

    return data

def salva_dati_json(data, filename):
    """Salva i dati in un file JSON."""
    if data is None:
        print(f"Nessun dato da salvare in {filename}")
        return

    # Salva i dati JSON direttamente nel file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Dati salvati in {filename}")

def main():
    # Carica i titoli dal file JSON
    titoli = carica_titoli(INPUT_FILE)

    if not titoli:
        print("Nessun titolo da elaborare.")
        return

    request_count = 0  # Contatore delle richieste API

    for i, titolo in enumerate(titoli):
        symbol = titolo.get('Symbol')
        exchange = ''

        if not symbol:
            print(f"Titolo non valido: {titolo}")
            continue

        print(f"Recupero dei dati per il simbolo {symbol} su {exchange}...")
        dati = recupera_dati_titolo(symbol, exchange)

        if dati:
            filename = os.path.join(OUTPUT_DIR, f'{symbol}_{exchange}.json')
            salva_dati_json(dati, filename)

        request_count += 1

        # Attendi se sono state effettuate 8 richieste
        if request_count == 8 and i < len(titoli) - 1:  # Evita l'attesa dopo l'ultima richiesta
            print("Raggiunto il limite di 8 richieste. Attesa di 70 secondi...")
            time.sleep(70)  # Attendi 1 minuto e 10 secondi
            request_count = 0  # Resetta il contatore

if __name__ == '__main__':
    main()
