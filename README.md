# Black Widow
![image](https://www.relativeuniverse.net/black-widow.jpeg)

## CTF Tool (Language: [python3.7](https://www.python.org/downloads/))

#### Dipendenze:
 - [pyshark](https://pypi.org/project/pyshark/): `pip3 install pyshark`

#### Funzionalità:
 - Sniffing (anche con regex sul contenuto delle richieste/risposte) per rubare flag catturate da altri;
 - Invio automatico di flag al gaming server;
 - Invio stessa richiesta a terminali multipli (per sfruttare contemporaneamente le stesse vulnerabilità di più server);
 - Storico mappa {server -> vulnerabilità} sfruttate (condiviso) per evitare ripetizione attacchi già andati a buon fine;
 - Cluster per evitare di effettuare stessi attacchi contemporaneamente;
 - Il tool di ogni macchina comunicherà in modo criptato e autenticato (RSA) con gli altri tool nella rete;

Suggerite voi altre funzionalità (comunque ci verranno in mente con l'esperienza sulle CTF).

#### Modalità sviluppo:
* Modularizzato (root: **/app**, eseguibile: **/main.py**):
  * |
  * |-- /utils/
  * |&emsp;|-- /cluster/        &emsp;# Package che fornisce metodi per condividere e ricevere info
  * |&emsp;|-- /encryption/     &emsp;# Package per criptare/decriptare, utilizzato anche dal package @requests
  * |&emsp;|-- /helpers/        &emsp;# Package contenente helpers generici usati in più parti del programma
  * |&emsp;|-- /history/        &emsp;# Package che fornisce classi e funzioni per salvare cronologie di vario tipo
  * |&emsp;|-- /requests/       &emsp;# Package che fornisce metodi per effettuare richieste (anche multiple)
  * |&emsp;|-- /settings/       &emsp;# Package dedito al settaggio di parametri globali (es. IP gaming server, ...)
  * |&emsp;|-- /sniffing/       &emsp;# Package che fornisce metodi per sniffing in una rete
  * |
  * |-- /attack/                &emsp;# Package per modalità di attacco
  * |-- /defense/               &emsp;# Package per modalità di difesa

<hr/>

### [CyberChallenge.it 2019](https://www.cyberchallenge.it)
#### [© Link Campus University](https://www.unilink.it)
