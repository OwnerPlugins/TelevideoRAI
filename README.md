# 📺 TelevideoRAI — Plugin Televideo per Enigma2

[![GitHub repo](https://img.shields.io/badge/GitHub-Belfagor2005%2FTelevideoRAI-blue)](https://github.com/Belfagor2005/TelevideoRAI)
[![Version](https://img.shields.io/badge/versione-v1.0-brightgreen)]()
[![License](https://img.shields.io/badge/licenza-GPL%20v3-lightgrey)]()

Plugin per decoder Enigma2 (OpenATV, OpenPLi, OpenBH, ecc.) che permette di consultare le pagine del Televideo RAI in tempo reale direttamente sul televisore. Scarica le immagini ufficiali in alta risoluzione e si adatta automaticamente alla risoluzione del tuo schermo.

> ⚠️ Questo plugin utilizza i server pubblici della RAI e non è affiliato alla Rai. Se la RAI dovesse cambiare nuovamente i server o introdurre blocchi, il plugin potrebbe richiedere un aggiornamento.

---

## ✨ Funzionalità principali

- **Navigazione Completa** — Tasti colorati standard (Rosso/Verde) per pagina precedente e successiva.
- **Salto Rapido** — Tasto Giallo (+10) e Tasto Blu (+100).
- **Selezione Regioni** — Premendo il tasto **MENU** si apre la lista di tutte le regioni italiane (dalla Lombardia alla Sicilia) per leggere il Televideo Regionale.
- **Inserimento Diretto** — Digita il numero di pagina a 3 cifre (es. `1`, `0`, `1`) sul telecomando per andare subito alla pagina.
- **Sottopagine** — Usa le frecce Destra/Sinistra per sfogliare le sottopagine (es. 100.01, 100.02).
- **Interfaccia Adattiva** — Si adatta automaticamente a risoluzioni 720p, 1080p, 1440p e 4K.
- **Barra dei Comandi** — Sfondo nero solido con indicatori colorati per una leggibilità perfetta e senza trasparenze.
- **Rollback Automatico** — Se una pagina non esiste per la regione selezionata, il plugin avvisa con un messaggio per 5 secondi e mantiene la pagina precedente, evitando di andare in errore.
- **Download Asincrono** — Il download avviene in background, l'interfaccia non si blocca mai durante il caricamento.
- **Memoria** — Salva l'ultima pagina visualizzata per ripartire da lì al prossimo avvio.

---

## 🚀 Installazione

1. Copia la cartella `TelevideoRAI` (con i file `plugin.py`, `__init__.py` e `plugin.png`) all'interno di `/usr/lib/enigma2/python/Plugins/Extensions/`.
2. Riavvia Enigma2 (o riavvia l'intero box) per far caricare il nuovo plugin.
3. Troverai **TelevideoRAI** nel menu delle Estensioni o nel Plugin Browser.

---

## 🎮 Comandi del Telecomando

| Tasto | Funzione |
|---|---|
| 🔴 **Rosso** | Pagina Indietro (es. da 201 a 200) |
| 🟢 **Verde** | Pagina Avanti (es. da 200 a 201) |
| 🟡 **Giallo** | Salta avanti di 10 pagine (+10) |
| 🔵 **Blu** | Salta avanti di 100 pagine (+100) |
| ◀️ **Freccia Sinistra** | Sottopagina precedente |
| ▶️ **Freccia Destra** | Sottopagina successiva |
| 🆗 **OK** | Apre la finestra per digitare il numero di pagina |
| 🔢 **0-9** | Digita il numero di 3 cifre per andare direttamente alla pagina |
| 🟩 **MENU** | Apre il menu a tendina per selezionare la Regione |
| 🚪 **EXIT** | Chiude il plugin e salva la pagina corrente |

---

## 📋 Changelog

### v1.0 — 2026-11-10
#### 🔧 Refactoring Completo e Nuove Funzioni
- **Riscrittura per Python 3** — Compatibilità totale con OpenATV 8.0 e Python 3.14. Sostituiti tutti i `print` e risolti i crash di sintassi.
- **Nuovi URL RAI** — Aggiornati i server da `servizitelevideo.rai.it` a `rainews.it/tlvd/`.
- **Bypass Anti-Bot** — Aggiunto header `User-Agent` (simula Google Chrome) per evitare il blocco 403 Forbidden da parte dei server RAI.
- **Addio Twisted per il Download** — Rimosso `twisted.web.client.downloadPage` che causava crash fatali (`write to closed file` e `bytes pattern`). Sostituito con `urllib.request`.
- **Selettore Regioni** — Aggiunto dizionario completo delle 20 regioni italiane e implementato il tasto MENU.
- **UI Rinnovata** — Rimossi i rettangoli colorati non supportati da alcune skin; aggiunta una barra inferiore nera solida con i testi dei comandi colorati (Rosso, Verde, Giallo, Blu).
- **Rollback e Gestione Errori** — Se una pagina non esiste, il plugin mostra un MessageBox di 5 secondi e torna all'ultima pagina funzionante, senza sballare il contatore.

---

## 🛠️ Tecnologie

- **Python 3** (Enigma2 API)
- `urllib.request` per il download asincrono delle immagini
- `twisted.internet.reactor` per la gestione dei thread in background (evita il blocco UI)
- `ePicLoad` per la decodifica nativa delle immagini PNG in memoria

---

## 👤 Autore

**Belfagor2005** — [@Belfagor2005](https://github.com/Belfagor2005)

Se questo plugin ti è utile, lascia una ⭐ sul repository GitHub!

---

*Dati © Rai Televideo · Solo uso personale · Questo plugin non ospita contenuti, ma effettua un semplice mirroring delle pagine pubbliche.*
