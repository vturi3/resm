import numpy as np

# Profilo di carico dell'utilizzatore in watt
carico = [1000, 1200, 1100, 900, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2000, 1800, 1600, 1400, 1200, 1100, 1000, 900, 800, 900, 1000, 1200]

# Profilo di produzione del campo fotovoltaico in watt
produzione = [0, 0, 0, 0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1400, 1200, 1000, 800, 600, 400, 200, 100, 0, 0, 0, 0]

# Capacità della batteria in wattora
capacita_batteria = 5000

# Dimensione del campo fotovoltaico in watt
dimensione_fotovoltaico = max(produzione)

# State of charge massimo e minimo della batteria in percentuale
soc_massimo = 80
soc_minimo = 20

# Energia totale consumata dall'utilizzatore in una giornata in wattora
energia_consumata = sum(carico)/1000

# Energia totale prodotta dal campo fotovoltaico in una giornata in wattora
energia_prodotta = sum(produzione)/1000

# Verifica se la capacità della batteria è sufficiente per accumulare tutta l'energia prodotta
if energia_prodotta > capacita_batteria:
    print("La capacità della batteria non è sufficiente per accumulare tutta l'energia prodotta.")
else:
    # Inizializza lo state of charge iniziale della batteria in wattora
    soc_iniziale = capacita_batteria*(soc_massimo/100)
    print("SOC INIZIALE DELLA BATTERIA: ",soc_iniziale)
    # Calcola la capacità massima e minima della batteria in wattora
    capacita_massima = capacita_batteria*(soc_massimo/100)
    capacita_minima = capacita_batteria*(soc_minimo/100)
    
    # Inizializza la capacità attuale della batteria in wattora
    capacita_attuale = soc_iniziale
    
    # Inizializza la potenza assorbita dalla rete in watt
    potenza_rete = 0
    
    # Ciclo di simulazione delle 24 ore
    for i in range(24):
        # Calcola la potenza disponibile dal campo fotovoltaico in watt
        potenza_disponibile = produzione[i]
        
        # Calcola la potenza richiesta dall'utilizzatore in watt
        potenza_richiesta = carico[i]
        
        # Calcola la potenza massima che può essere immagazzinata o prelevata dalla batteria in watt
        potenza_max_batteria = capacita_attuale - capacita_minima
        
        # Se la potenza disponibile dal campo fotovoltaico è maggiore della potenza richiesta dall'utilizzatore
        if potenza_disponibile >= potenza_richiesta:
            # Il surplus di energia prodotta viene immagazzinato nella batteria
            surplus = potenza_disponibile - potenza_richiesta
            if surplus > 0:
                if capacita_attuale + surplus > capacita_massima:
                    # Se la capacità attuale supera la capacità massima della batteria, la batteria viene caricata al massimo
                    capacita_attuale = capacita_massima
                else:
                    # Altrimenti la batteria viene caricata con tutto il surplus di energia prodotta
                    capacita_attuale += surplus
                        
            # La potenza richiesta viene soddisfatta dal campo fotovoltaico
            potenza_utilizzata = potenza_richiesta
                
        else:
            # Se la potenza disponibile dal campo fotovoltaico è inferiore alla potenza richiesta dall'utilizzatore
            # la batteria fornisce la differenza di potenza richiesta
            potenza_batteria = potenza_richiesta - potenza_disponibile
            if potenza_batteria <= potenza_max_batteria:
                # Se la potenza richiesta dalla batteria è inferiore o uguale alla potenza massima che può essere immagazzinata o prelevata dalla batteria, la batteria fornisce la potenza richiesta
                capacita_attuale -= potenza_batteria
                potenza_utilizzata = potenza_richiesta
            else:
                # Altrimenti la batteria fornisce la potenza massima che può essere immagazzinata o prelevata dalla batteria
                capacita_attuale -= potenza_max_batteria
                potenza_utilizzata = potenza_disponibile + potenza_max_batteria
                potenza_rete += potenza_richiesta - potenza_utilizzata
                    
        # Stampa il risultato della simulazione per ogni ora
        print("Ora:", i+1, "Potenza disponibile da fotovoltaico: ", potenza_disponibile, "Potenza richiesta dal carico: ", potenza_richiesta, "Potenza non esterna utilizzata:", potenza_utilizzata, "Capacità al termine dell'ora della batteria:", capacita_attuale, "Potenza assorbita dalla rete:", potenza_rete)
            
    # Stampa il risultato finale della simulazione
    print("Energia totale consumata:", energia_consumata, "Energia totale prodotta:", energia_prodotta, "Energia totale fornita dalla rete:", potenza_rete/1000)
    print("Capacità attuale della batteria alla fine della giornata:", capacita_attuale)

