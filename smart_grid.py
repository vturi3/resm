import numpy as np
from scipy.optimize import minimize

# Funzione di costo da minimizzare
def objective(x, load_profile, pv_profile, battery_initial_charge, energy_source_profile):
    x = np.array(x)
    load_profile = np.array(load_profile)
    pv_profile = np.array(pv_profile)
    energy_source_profile = np.array(energy_source_profile)
    
    # Estraiamo i valori di input dalla soluzione corrente
    battery_charge = battery_initial_charge
    power_grid = energy_source_profile - pv_profile - x
    
    # Inizializziamo il valore della funzione di costo a 0
    cost = 0
    
    # Iteriamo attraverso tutte le ore del giorno
    for i in range(len(load_profile)):
        # Calcoliamo il nuovo stato di carica della batteria
        battery_charge += x[i]
        
        # Verifichiamo che il valore di stato di carica della batteria sia valido
        if battery_charge < 0 or battery_charge > 100:
            return np.inf
        
        # Aggiungiamo il costo del prelievo di energia dalla rete elettrica
        if power_grid[i] > 0:
            cost += power_grid[i]
        
        # Aggiungiamo il costo dell'energia immagazzinata nella batteria
        elif power_grid[i] < 0:
            cost -= power_grid[i] * battery_charge
        
        # Aggiungiamo il costo di una eventuale sovrapproduzione di energia da fotovoltaico
        if pv_profile[i] - x[i] > 0:
            cost -= (pv_profile[i] - x[i]) * 0.1
        
        # Aggiorniamo il valore della batteria
        battery_charge = min(max(battery_charge, 20), 80)
    
    return cost

# Dati di input
load_profile = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 0, 0, 0, 0]
pv_profile = [0, 0, 0, 0, 0, 0, 0, 20, 50, 70, 90, 100, 100, 90, 70, 50, 20, 0, 0, 0, 0, 0, 0, 0]
energy_source_profile = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
battery_initial_charge = 70

# Vincoli sui valori di input
bounds = [(0, 50) for i in range(24)]

# Risoluzione del problema di ottimizzazione
sol = minimize(objective, np.zeros(24), args=(load_profile, pv_profile, battery_initial_charge, energy_source_profile), bounds=bounds)

# Stampa della soluzione
print(sol.x)
