# Enhanced phonetic reading NVDA Add-on #
Questo componente aggiuntivo aggiunge alcune funzionalità alla lettura fonetica di NVDA, come la lettura delle descrizioni istantanea e ritardata.

Copyright (C) 2022 David CM <dhf360@gmail.com>

Questo pacchetto è distribuito secondo i termini della GNU General Public License, versione 2 o successive.

## Download.
	L'ultima versione è disponibile per il
[download a questo link](https://davidacm.github.io/getlatest/gh/davidacm/EnhancedPhoneticReading)

## Funzionalità.

* Descrizione ritardata: annuncia la descrizione dell'ultimo carattere letto dopo n millisecondi quanto il carattere è stato letto con i comandi di revisione, come ad esempio frecce, comandi di carattere attuale, precedente, successivo ecc....  
* Descrizione istantanea del carattere: Legge da descrizione del carattere attuale invece del carattere stesso. Questa funzionalità deve essere abilitata manualmente e verrà disabilitata alla chiusura di NVDA.

## Note.

* Quando la descrizione istantanea è abilitata, la descrizione ritardata non verrà annunciata.
* Questo componente aggiuntivo considera anche il cambio automatico della lingua. Pertanto, se l'ultimo carattere letto rilevato dal componente è stato pronunciato in un'altra lingua rispetto a quella predefinita e la commutazione automatica  è attiva, la descrizione verrà letta nella lingua rilevata.
* Solo per descrizioni ritardate: tutti i caratteri che non hanno una descrizione disponibile per la lingua specificata (locale characterDescriptions.dic) verranno ignorati. PER ESEMPIO. se leggi il carattere "4" e la lingua predefinita o rilevata corrente è lo spagnolo, non otterrai una descrizione ritardata perché lo spagnolo non ha una descrizione pe.
* For developers: In generale, qualsiasi carattere inviato con l'argomento textInfos.UNIT_CHARACTER a speech.speakTextInfo attiverà una descrizione ritardata del carattere.

## Requisiti
  Si necessita di NVDA 2019.3 o successivo.

## Installazione
  Si installa come un qualsiasi componente aggiuntivo di NVDA.

## Utilizzo
  La funzionalità del componente aggiuntivo verrà abilitata dopo l'installazione.  
  Per abilitarlo o disabilitarlo, recarsi nelle impostazioni di NVDA e selezionare "Enhanced phonetic reading". In detta categoria è possibile impostare i seguenti parametri:

* Abilita la lettura ritardata delle descrizioni dei caratteri.
* Ritardo per l'annuncio della descrizione dei caratteri (in ms): il tempo che il componente aggiuntivo attende prima di pronunciare la descrizione del carattere letto. Non è possibile impostarlo ad un valore superiore a 20000 ms.

## Scripts

* Abilita o disabilita la descrizione istantanea dei caratteri: assegnato a "nvda + control + 2tn" o "nvda+ control + invio" per le tastiere laptop. Questo script Abilita o disabilita la descrizione istantanea dei caratteri.
* Abilita o disabilita la descrizione automatica dei caratteri: Nessuna combinazione assegnata. Questo script permette di abilitare o disabilitare la lettura ritardata dei caratteri.  

È possibile assegnare un gesto o una combinazione di tasti nella categoria "voce" in "gesti e tasti di immissione"!.

## Contributi, suggerimenti e donazioni

Se il mio progetto ti piace o questo software ti è utile nella vita quotidiana e vorresti contribuire in qualche modo, puoi donare con le seguenti modalità:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [Criptovalute ed altri metodi.](https://davidacm.github.io/donations/)

Se vuoi correggere bug, segnalare problemi o nuove funzionalità, puoi contattarmi a: <dhf360@gmail.com>.

  O nel repository  github di uesto progetto:
  [Enhanced phonetic reading in GitHub](https://github.com/davidacm/enhancedphoneticreading)

    Puoi ottenere l'ultima versione di questo componente aggiuntivo in detto repository.
