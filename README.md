# networkProgramming-project
Server:
    • attende routers in entrata
    • registra i clients che entrano nella chat
    • elimina i clients che escono dalla chat
    • dato un pacchetto da consegnare (ricevuto da un router) controlla se il destinatario è online: se lo è, lo invia, altrimenti lo riporta indietro al mittente. Ogni messaggio inviato lo spedisce in broadcast ai routers cosicchè quello che ha il destinatario collegato lo consegnerà. 
Router:
    • si collega al server
    • accetta i clients in entrata, registra il loro IP e mac nell’ARP table e comunica il join al server
    • all’uscita di un client lo rimuove dall’ARP table e inoltra l’informazione al server
    • inoltra i pacchetti dei clients collegati al server
    • inoltra i pacchetti provenienti dal server al destinatario se presente nell’ARP table.
Client:
    • si collega al router
    • una volta collegato invia subito al router le sue coordinate (indirizzo IP e MAC)
    • può spedire messaggi ad altri clients specificando l’indirizzo IP
    • può ricevere messaggi
    • alla chiusura della finestra invia un messaggio di quit al router  
