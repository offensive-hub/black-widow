# Black Widow
## CTF Tool

##### Funzionalità:
 - Sniffing (anche con regex sul contenuto delle richieste/risposte) per rubare flag catturate da altri;
 - Invio automatico di flag al gaming server;
 - Invio stessa richiesta a terminali multipli (per sfruttare contemporaneamente le stesse vulnerabilità di più server);
 - Storico mappa {server -> vulnerabilità} sfruttate (condiviso) per evitare ripetizione attacchi già andati a buon fine;
 - Cluster per evitare di effettuare stessi attacchi contemporaneamente;
 - Il tool di ogni macchina comunicherà in modo criptato e autenticato (RSA) con gli altri tool nella rete;

Suggerite voi altre funzionalità (comunque ci verranno in mente con l'esperienza sulle CTF).

##### Modalità sviluppo:
 - Modularizzato (root: /app):
        |
        |-- /settings/      # Package dedito al settaggio di parametri globali (es. IP gaming server, ...)
        |
        |-- /utils/
        |      |-- /requests/      # Package che fornisce metodi per effettuare richieste (anche multiple)
        |      |-- /history/       # Package che fornisce classi e funzioni per salvare cronologie di vario tipo
        |      |-- /sniffing/      # Package che fornisce metodi per sniffing in una rete
        |      |-- /cluster/       # Package che fornisce metodi per condividere e ricevere info
        |      |-- /encryption/    # Package per criptare/decriptare, utilizzato anche dal package @requests
        |
        |-- /attack/        # Package per modalità di attacco
        |-- /defense/       # Package per modalità di difesa
        |
        |-- main.py         # Eseguibile principale

<hr/>

### [CyberChallenge.it 2019](https://www.cyberchallenge.it)
#### [© Link Campus University](https://www.unilink.it)
