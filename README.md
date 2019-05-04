# Black Widow
## CTF Tool (Language: ***python3***)

#### Funzionalità:
 - Sniffing (anche con regex sul contenuto delle richieste/risposte) per rubare flag catturate da altri;
 - Invio automatico di flag al gaming server;
 - Invio stessa richiesta a terminali multipli (per sfruttare contemporaneamente le stesse vulnerabilità di più server);
 - Storico mappa {server -> vulnerabilità} sfruttate (condiviso) per evitare ripetizione attacchi già andati a buon fine;
 - Cluster per evitare di effettuare stessi attacchi contemporaneamente;
 - Il tool di ogni macchina comunicherà in modo criptato e autenticato (RSA) con gli altri tool nella rete;

Suggerite voi altre funzionalità (comunque ci verranno in mente con l'esperienza sulle CTF).

#### Modalità sviluppo:
 - Modularizzato (root: **/app**, eseguibile: **/main.py**):
      <ul>
        <li>|</li>
        <li>|-- /utils/</li>
        <li>|    &emsp;|-- /settings/    &emsp;# Package dedito al settaggio di parametri globali (es. IP gaming server, ...)</li>
        <li>|    &emsp;|-- /requests/    &emsp;# Package che fornisce metodi per effettuare richieste (anche multiple)</li>
        <li>|    &emsp;|-- /history/    &emsp;# Package che fornisce classi e funzioni per salvare cronologie di vario tipo</li>
        <li>|    &emsp;|-- /sniffing/    &emsp;# Package che fornisce metodi per sniffing in una rete</li>
        <li>|    &emsp;|-- /cluster/    &emsp;# Package che fornisce metodi per condividere e ricevere info</li>
        <li>|    &emsp;|-- /encryption/    &emsp;# Package per criptare/decriptare, utilizzato anche dal package @requests</li>
        <li>|</li>
        <li>|-- /attack/    &emsp;# Package per modalità di attacco</li>
        <li>|-- /defense/    &emsp;# Package per modalità di difesa</li>
     </ul>

<hr/>

### [CyberChallenge.it 2019](https://www.cyberchallenge.it)
#### [© Link Campus University](https://www.unilink.it)
