# Black Widow
![image](https://www.relativeuniverse.net/black-widow.jpeg)

## CTF Tool (Language: [python3.7](https://www.python.org/downloads/))

#### Dipendenze:
 - [pyshark](https://pypi.org/project/pyshark/): `pip3 install pyshark`
 - [PyQt5](https://pypi.org/project/PyQt5/): `pip3 install PyQt5`

#### Funzionalità:
 - Sniffing (anche con regex sul contenuto delle richieste/risposte) per rubare flag catturate da altri;
 - Invio automatico di flag al gaming server;
 - Invio stessa richiesta a terminali multipli (per sfruttare contemporaneamente le stesse vulnerabilità di più server);
 - Storico mappa {server -> vulnerabilità} sfruttate (condiviso) per evitare ripetizione attacchi già andati a buon fine;
 - Cluster per evitare di effettuare stessi attacchi contemporaneamente;
 - Il tool di ogni macchina comunicherà in modo criptato e autenticato (RSA) con gli altri tool nella rete;

Suggerite voi altre funzionalità (comunque ci verranno in mente con l'esperienza sulle CTF).

#### Directories:
  * |-- /app            &emsp;# Package principale dell'applicazione
    * |
    * |-- /attack/                &emsp;# Package per modalità di attacco
    * |-- /defense/               &emsp;# Package per modalità di difesa
    * |-- /utils/
    * |
      * |&emsp;&emsp;|&emsp;&emsp;|-- /cluster/        &emsp;# Package che fornisce metodi per condividere e ricevere info
      * |&emsp;&emsp;|&emsp;&emsp;|-- /encryption/     &emsp;# Package per criptare/decriptare stringhe/files
      * |&emsp;&emsp;|&emsp;&emsp;|-- /exceptions/     &emsp;# Contine eventuali eccezioni personalizzate
      * |&emsp;&emsp;|&emsp;&emsp;|-- /helpers/        &emsp;# Package contenente helpers generici usati in più parti del programma
      * |&emsp;&emsp;|&emsp;&emsp;|-- /history/        &emsp;# Package che fornisce classi e funzioni per salvare cronologie di vario tipo
      * |&emsp;&emsp;|&emsp;&emsp;|-- /requests/       &emsp;# Package che fornisce metodi per effettuare richieste (anche multiple)
      * |&emsp;&emsp;|&emsp;&emsp;|-- /settings/       &emsp;# Package dedito al settaggio di parametri globali (es. IP gaming server, ...)
      * |&emsp;&emsp;|&emsp;&emsp;|-- /sniffing/       &emsp;# Package che fornisce metodi per sniffing in una rete
      * |&emsp;&emsp;|&emsp;&emsp;|-- /sql/            &emsp;# Package che fornisce metodi per sql injection
    * |&emsp;&emsp;



<hr/>

### [CyberChallenge.it 2019](https://www.cyberchallenge.it)
#### [© Link Campus University](https://www.unilink.it)
