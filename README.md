# Progetto esame progammazione di reti (a.a. 2019 - 2020)
***Server:***
 - Attende routers in entrata;
 - Registra i clients che entrano nella chat;
 - Elimina i clients che escono dalla chat;
 - Dato un pacchetto da consegnare (ricevuto da un router) controlla se il destinatario è online: se lo è, lo invia, altrimenti lo riporta indietro al mittente. Ogni messaggio inviato lo spedisce in broadcast ai routers cosicchè quello che ha il destinatario collegato lo consegnerà. 
 
 ***Router:***
 
 - Si collega al server;
 - Accetta i clients in entrata, registra il loro *IP* e mac nell’*ARP* table e comunica il join al server;
 - All’uscita di un client lo rimuove dall’*ARP* table e inoltra l’informazione al server;
 - Inoltra i pacchetti dei clients collegati al server;
 - Inoltra i pacchetti provenienti dal server al destinatario se presente nell’*ARP* table.

***Client:***

 - Si collega al router;
 - Una volta collegato invia subito al router le sue coordinate (indirizzo *IP* e *MAC*);
 - Può spedire messaggi ad altri clients specificando l’indirizzo *IP*;
 - Può ricevere messaggi;
 - Alla chiusura della finestra invia un messaggio di quit al router.
