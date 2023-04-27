import random
import csv

# Dati di produzione cumulativa mensili in kWh per un impianto di 5kW posto a Salerno
prod_mensili = [235, 293, 466, 595, 772, 864, 933, 811, 588, 435, 262, 208]

#test
giorni_mensili = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Calcolo della produzione giornaliera in kWh, in questo modo abbiamo la produzione totale media di un giorno per ogni mese dell'anno
prod_giornaliera_media = [prod_mensili[i]/giorni_mensili[i] for i in range(len(prod_mensili))]

# Approssimiamo alla seconda cifra decimale e calcoliamo i watt per ora
prod_giornaliera_media_rounded = [int(elem*1000) for elem in prod_giornaliera_media]
print("prod giornaliera", prod_giornaliera_media_rounded)

# Aggiunta della variazione giornaliera
prod_giornaliera_variata = []
for i in range(365):
    prod_giornaliera_variata.append(round(prod_giornaliera_media_rounded[i%12] * (1 + random.uniform(-0.1, 0.1)), 2))

#print("VARIATA: ", prod_giornaliera_variata)

def calcolo_prod_oraria(tot_produzione_giornaliera):
    # Definiamo l'irradianza media oraria durante la giornata
    # con valori in Watt/m^2
    irradianza = [0, 0, 0, 80, 140, 200, 230, 250, 230, 200, 140, 60, 0]

    # Calcoliamo la somma delle irradiazioni orarie
    irradianza_sommata = sum(irradianza)

    # Calcoliamo il fattore di scala per la produzione totale giornaliera
    factor = tot_produzione_giornaliera / irradianza_sommata

    # Calcoliamo la produzione oraria
    prod_oraria = [x * factor for x in irradianza]

    return prod_oraria

valori_orari = [int(elem) for elem in calcolo_prod_oraria(prod_giornaliera_media_rounded[0])]
print("produzione oraria", valori_orari)
print("sum", sum(valori_orari))

def produzione_mensile(profilo_giornaliero, mese):
    """Genera un array di produzione mensile leggermente variato rispetto al profilo base"""
    profilo_mensile = profilo_giornaliero.copy()
    if mese == 1 or mese == 2 or mese == 12:  # inverno
        variance = random.uniform(-0.3, 0.3)
    elif mese >= 3 and mese <= 5:  # primavera
        variance = random.uniform(-0.2, 0.2)
    elif mese >= 6 and mese <= 8:  # estate
        variance = random.uniform(-0.1, 0.1)
    else:  # autunno
        variance = random.uniform(-0.2, 0.2)
        
    for i in range(len(profilo_mensile)):
        profilo_mensile[i] += profilo_mensile[i] * variance
        
    return profilo_mensile

prod_mensile = [int(elem) for elem in produzione_mensile(valori_orari,1)]
print("array variato", prod_mensile)

"""
# Calcolo della produzione oraria
prod_oraria = []
for i in range(365):
    for j in range(24):
        if j < 6 or j > 18:  # ore notturne
            prod_oraria.append(0)
        else:
            prod_oraria.append(round(prod_giornaliera_variata[i] * (j-5) / 7, 2))

# Scrittura del file CSV
with open('produzione_oraria.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Data', 'Ora', 'Produzione'])
    for i in range(365):
        for j in range(24):
            date = '2023-{0:02d}-{1:02d}'.format(i//31+1, i%31+1)
            hour = '{0:02d}:00'.format(j)
            writer.writerow([date, hour, prod_oraria[i*24+j]*1000])"""
