import requests
from bs4 import BeautifulSoup
import re
import time

# CREDENZIALI TELEGRAM
# INSERISCI QUI I TUOI DATI REALI (mantenendo le virgolette)
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
COGNOME_MEDICO = ""

# --- CONFIGURAZIONE SITO ---
URL_BASE = "https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri"

PARAMETRI_URL = {
    "p_p_id": "MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm",
    "p_p_lifecycle": "1",
    "p_p_state": "normal",
    "p_p_mode": "view",
    "p_p_col_id": "column-1",
    "p_p_col_count": "1",
    "_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action": "ricerca"
}

DATI_FORM = {
    "cambioProvincia": "false",
    "provincia": "PD",
    "comune": "PADOVA",
    "nome": "",
    "cognome": COGNOME_MEDICO,
    "indirizzoMedico": "",
    "tipologia": "000",
    "indirizzo": "",
    "distanza": "000",
    "invia": "CERCA"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": URL_BASE
}

def invia_notifica_telegram(posti):
    # Scegliamo il messaggio in base al numero di posti
    if posti > 0:
        messaggio = f"🚨 <b>DISPONIBILITÀ TROVATA!</b> 🚨\n\nMedico: MEDICO: \nPosti disponibili: <b>{posti}</b>\n\nVai subito sul portale della Regione per prenotare!"
    else:
        messaggio = f"ℹ️ <b>Controllo orario completato</b>\n\nMedico: MEDICO: \nPosti disponibili: <b>{posti}</b>\n\nNessuna novità al momento."

    url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": messaggio,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url_api, data=payload)
        print("📲 Notifica Telegram inviata con successo!")
    except Exception as e:
        print(f"❌ Errore nell'invio della notifica Telegram: {e}")    

def controlla_disponibilita():
    print(f"[{time.strftime('%H:%M:%S')}] Avvio controllo...")
    sessione = requests.Session()
    
    try:
        sessione.get(URL_BASE, headers={"User-Agent": HEADERS["User-Agent"]})
        risposta_ricerca = sessione.post(URL_BASE, params=PARAMETRI_URL, data=DATI_FORM, headers=HEADERS)
        risposta_ricerca.raise_for_status()

        soup_ricerca = BeautifulSoup(risposta_ricerca.text, 'html.parser')
        spans_link = soup_ricerca.find_all("span", class_="link")
        id_medico = None

        for span in spans_link:
            if "COGNOME_MEDICO" in span.get_text().upper():
                span_genitore = span.find_parent("span", class_="poi")
                if span_genitore and "onclick" in span_genitore.attrs:
                    testo_onclick = span_genitore["onclick"]
                    match = re.search(r"submitLuogo\('(\d+)'\)", testo_onclick)
                    if match:
                        id_medico = match.group(1)
                        break

        if not id_medico:
            print("❌ Errore: Non ho trovato l'ID nascosto per il medico specificato.")
            return

        form_dettaglio = soup_ricerca.find("form", id="formDettaglio")
        if not form_dettaglio:
            print("❌ Errore: Non trovo il form di dettaglio nella pagina.")
            return

        url_dettaglio = form_dettaglio["action"]
        dati_dettaglio = {"idLuogo": id_medico}

        risposta_dettaglio = sessione.post(url_dettaglio, data=dati_dettaglio, headers=HEADERS)
        risposta_dettaglio.raise_for_status()

        soup_dettaglio = BeautifulSoup(risposta_dettaglio.text, 'html.parser')
        cella_testo = soup_dettaglio.find(lambda tag: tag.name == "td" and "Disponibilità assistiti a termine" in tag.text)
        
        if cella_testo:
            cella_numero = cella_testo.find_next_sibling("td")
            if cella_numero:
                posti_disponibili = int(cella_numero.text.strip())
                print(f"✅ Medico trovato - Posti disponibili: {posti_disponibili}")
                
                # SE I POSTI SONO MAGGIORI DI ZERO, INVIA MESSAGGIO
                invia_notifica_telegram(posti_disponibili)
            else:
                print("❌ Errore: Trovata l'etichetta, ma non il numero dei posti.")
        else:
            print("❌ Errore: Impossibile trovare la tabella dei risultati.")

    except Exception as e:
        print(f"❌ Si è verificato un errore durante il controllo: {e}")

# --- CICLO PRINCIPALE ---
if __name__ == "__main__":
    print("🤖 Bot Medico avviato!\nPremi CTRL+C per fermarlo in qualsiasi momento.\n" + "-"*40)
    
    # Loop infinito
    while True:
        controlla_disponibilita()
        # Mette il programma in pausa per 3600 secondi (1 ora)
        time.sleep(21600)  # Controlla ogni 6 ore
        print(f" finito il timer 🕰")
