# 🩺 BotMedico - Regione Veneto

Uno script in Python che automatizza la ricerca di disponibilità per i Medici di Medicina Generale (e Pediatri) sul portale della Sanità della Regione Veneto. Quando si libera un posto (assistiti a termine o illimitati), il bot invia immediatamente una notifica su un canale o chat Telegram.

## 💡 Perché questo script?
Trovare posto presso un medico specifico può essere difficile. Invece di aggiornare la pagina manualmente ogni giorno, questo bot lavora in background, eseguendo un controllo orario e avvisandoti solo quando ci sono novità.

## 🛠️ Prerequisiti
Per far funzionare lo script, devi avere installato Python (versione 3.x) e le seguenti librerie:
* `requests`
* `beautifulsoup4`

## 🚀 Installazione e Uso

1. **Clona il repository:**
   `git clone https://github.com/TUO_NOME_UTENTE/NOME_REPO.git`

2. **Installa le dipendenze:**
   `pip install requests beautifulsoup4`

3. **Configura Telegram:**
   * Crea un bot tramite [@BotFather](https://t.me/botfather) su Telegram e ottieni il tuo `TOKEN`.
   * Avvia una chat con il bot e ottieni il tuo `CHAT_ID` tramite un bot come [@userinfobot](https://t.me/userinfobot).
   * Inserisci questi due dati all'interno del file `test_medico.py`.

4. **Avvia il bot:**
   `python test_medico.py`
   (Lo script eseguirà un controllo ogni ora).

## ⚠️ Disclaimer
Questo script è stato creato per uso personale e a scopo didattico. Assicurati di non abusare dei server istituzionali impostando intervalli di controllo troppo brevi (è consigliato mantenere un intervallo di almeno un'ora). L'autore non è responsabile per eventuali blocchi IP derivanti da un uso scorretto.
