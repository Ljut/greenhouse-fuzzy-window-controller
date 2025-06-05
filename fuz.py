import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json

with open("paradajz.json", "r") as json_file:
    paradajzDict = json.load(json_file)

varijable = {
    "TemperaturaZraka":4,
    "VlaznostZraka":84,
    "BrzinaVjetra":2.65,
    "AQI":3,
    "DaLiPadaKisa":False,
    "VrijemeDana":1,
}

"""
varijable = {
    "TemperaturaZraka":70.5,
    "VlaznostZraka":94,
    "BrzinaVjetra":2.65,
    "AQI":499,
    "DaLiPadaKisa":False,
    "VrijemeDana":1,
}
"""

vektor = np.array(list(varijable.values()))

"""vektor = []
for a in varijable:
    vektor.append(varijable[a])"""

"""vektor = [
    varijable["AQI"],
    varijable["BrzinaVjetra"],
    varijable["DaLiPadaKisa"],
    varijable["TemperaturaZraka"],
    varijable["VlaznostZraka"]
]"""
print(varijable)
print(vektor)

def paradajz_fuzzy(vektor):
    print(vektor)
    val = 0

    # Define input variables
    lista_inputa = []
    for uvjet in paradajzDict["uvjeti"]:
        od = uvjet["Domen"][0]
        do = uvjet["Domen"][1]
        delta = uvjet["Domen"][2]
        lista_inputa.append(ctrl.Antecedent(np.arange(od,do,delta), uvjet["Varijabla"]))



    # Define output variable with more points
    prozor = ctrl.Consequent(np.arange(0, 1.1, 0.5), 'prozor')

    # Membership functions
    for i in range(len(lista_inputa)):
        lin_var = paradajzDict["uvjeti"][i]["Lingvisticki model varijable"]
        for e in lin_var:
            if e["ime"]=="noc":
                noc_morning = fuzz.trapmf(lista_inputa[i].universe, e["domen"][0])
                noc_evening = fuzz.trapmf(lista_inputa[i].universe, e["domen"][1])
                lista_inputa[i][e["ime"]] = np.fmax(noc_morning, noc_evening)
            elif len(e["domen"])==3:
                lista_inputa[i][e["ime"]]= fuzz.trimf(lista_inputa[i].universe, e["domen"])
            elif len(e["domen"])==4:
                lista_inputa[i][e["ime"]]= fuzz.trapmf(lista_inputa[i].universe, e["domen"])

    #prozor['zatvori'] = fuzz.trimf(prozor.universe, [0, 0, 0.5])
    #prozor['nista ne radi'] = fuzz.trimf(prozor.universe, [0.4, 0.5, 0.6])
    #prozor['otvori'] = fuzz.trimf(prozor.universe, [0.5, 1, 1])
    prozor = ctrl.Consequent(np.arange(0, 1.001, 0.001), 'prozor')
    prozor['zatvori'] = fuzz.trimf(prozor.universe, [0, 0, 0.3])
    prozor['nista ne radi'] = fuzz.trimf(prozor.universe, [0.2, 0.3, 0.4])
    prozor['otvori'] = fuzz.trapmf(prozor.universe, [0.3, 0.6, 1, 1])

    prozor.view()

    temperatura = lista_inputa[0]
    vlaznost = lista_inputa[1]
    brzinaVjetra = lista_inputa[2]
    aqi = lista_inputa[3]
    daLiKisaPada = lista_inputa[4]
    vrijemeDana = lista_inputa[5]
    # Rules
    pravila = []
    #pravila.append(ctrl.Rule())
    """pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"]) & temperatura['vruce'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(~aqi["dobro"] & ~aqi["umjereno"],prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-noc'] & vlaznost["suho"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['vruce'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['hladno'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-dan'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & brzinaVjetra["umjeren"] & temperatura['taman-za-dan'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['vruce'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-noc'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-dan'] & vlaznost["taman-za-noc"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & daLiKisaPada["pada kisa"] & brzinaVjetra["opasan"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prevruce"] & vrijemeDana["podne"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['opasno'], prozor["zatvori"]))
    pravila.append(ctrl.Rule(daLiKisaPada["pada kisa"] & brzinaVjetra["jako-opasan"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(temperatura["prehladno"] & vrijemeDana["noc"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(vlaznost["prevlazno"] & temperatura["hladno"] & vrijemeDana["jutro"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi["pravo nezdravo"] & daLiKisaPada["pada kisa"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(temperatura["prevruce"] & vrijemeDana["podne"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(brzinaVjetra["kritican"] & temperatura["hladno"] & vrijemeDana["noc"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi["blago nezdravo"] & vlaznost["prevlazno"] & vrijemeDana["poslijepodne"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(brzinaVjetra["opasan"] & daLiKisaPada["pada kisa"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi["nezdravo"] & temperatura["taman-za-dan"] & ~daLiKisaPada["ne pada kisa"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["hladno"] & vlaznost["prevlazno"] & vrijemeDana["jutro"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prehladno"] & brzinaVjetra["slab"] & vrijemeDana["noc"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["prevruce"] & vlaznost["prevlazno"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & vlaznost["prevlazno"] & vrijemeDana["noc"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & daLiKisaPada["pada kisa"] & temperatura["hladno"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prehladno"] & vlaznost["presuho"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & brzinaVjetra["jako-opasan"], prozor["zatvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["taman-za-dan"] & daLiKisaPada["pada kisa"] & vlaznost["prevlazno"], prozor["zatvori"]))
    """
    """pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"]) & temperatura['vruce'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(~aqi["dobro"] & ~aqi["umjereno"],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-noc'] & vlaznost["suho"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['vruce'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['hladno'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-dan'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & brzinaVjetra["umjeren"] & temperatura['taman-za-dan'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['vruce'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-noc'] & vlaznost["taman-za-dan"] & daLiKisaPada["ne pada kisa"] & vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"])  & temperatura['taman-za-dan'] & vlaznost["taman-za-noc"] & daLiKisaPada["ne pada kisa"] & ~vrijemeDana['noc'],prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & daLiKisaPada["pada kisa"] & brzinaVjetra["opasan"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prevruce"] & vrijemeDana["podne"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(aqi['opasno'], prozor["zatvori"]))#
    
    pravila.append(ctrl.Rule(daLiKisaPada["pada kisa"] & brzinaVjetra["jako-opasan"], prozor["otvori"]))
    pravila.append(ctrl.Rule(temperatura["prehladno"] & vrijemeDana["noc"], prozor["otvori"]))
    pravila.append(ctrl.Rule(vlaznost["prevlazno"] & temperatura["hladno"] & vrijemeDana["jutro"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi["pravo nezdravo"] & daLiKisaPada["pada kisa"], prozor["otvori"]))
    pravila.append(ctrl.Rule(temperatura["prevruce"] & vrijemeDana["podne"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(brzinaVjetra["kritican"] & temperatura["hladno"] & vrijemeDana["noc"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi["blago nezdravo"] & vlaznost["prevlazno"] & vrijemeDana["poslijepodne"], prozor["otvori"]))
    pravila.append(ctrl.Rule(brzinaVjetra["opasan"] & daLiKisaPada["pada kisa"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi["nezdravo"] & temperatura["taman-za-dan"] & ~daLiKisaPada["ne pada kisa"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["hladno"] & vlaznost["prevlazno"] & vrijemeDana["jutro"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prehladno"] & brzinaVjetra["slab"] & vrijemeDana["noc"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["prevruce"] & vlaznost["prevlazno"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & vlaznost["prevlazno"] & vrijemeDana["noc"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(aqi['umjereno'] & daLiKisaPada["pada kisa"] & temperatura["hladno"], prozor["otvori"]))#
    pravila.append(ctrl.Rule(aqi['dobro'] & temperatura["prehladno"] & vlaznost["presuho"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['dobro'] & brzinaVjetra["jako-opasan"], prozor["otvori"]))
    pravila.append(ctrl.Rule(aqi['umjereno'] & temperatura["taman-za-dan"] & daLiKisaPada["pada kisa"] & vlaznost["prevlazno"], prozor["otvori"]))
    """
    
    pravila.append(ctrl.Rule(vrijemeDana['noc'] & temperatura['taman-za-dan'], prozor["otvori"]))
    pravila.append(ctrl.Rule(~vrijemeDana['noc'] & temperatura['taman-za-noc'], prozor["zatvori"]))
    pravila.append(ctrl.Rule(temperatura['prehladno'] | temperatura['hladno'],prozor["zatvori"]))
    pravila.append(ctrl.Rule(temperatura['vruce'] | temperatura['prevruce'],prozor["otvori"]))
    pravila.append(ctrl.Rule(~vrijemeDana['noc'] & temperatura['taman-za-dan'], prozor['nista ne radi']))
    pravila.append(ctrl.Rule(vlaznost['presuho'],prozor['otvori']))
    pravila.append(ctrl.Rule(vlaznost['suho'], prozor['otvori']))
    pravila.append(ctrl.Rule(vlaznost['prevlazno'] & ~daLiKisaPada["ne pada kisa"], prozor['otvori']))
    pravila.append(ctrl.Rule(~brzinaVjetra["nema"] & ~brzinaVjetra["slab"], prozor['zatvori']))
    pravila.append(ctrl.Rule(brzinaVjetra["slab"] & (vlaznost["suho"] | vlaznost["presuho"]), prozor['otvori']))
    pravila.append(ctrl.Rule(~brzinaVjetra["nema"] & (~vlaznost["taman-za-dan"] | ~vlaznost["taman-za-noc"]), prozor['zatvori']))
    #pravila.append(ctrl.Rule(~aqi["dobro"] | ~aqi["umjereno"],prozor["zatvori"]))
    pravila.append(ctrl.Rule(~(aqi["dobro"] | aqi["umjereno"]),prozor["zatvori"]))
    
    #for pravilo in pravila:
    #    aktivacija = pravilo.antecedent.evaluate(kontroler.input)
    #    if aktivacija > 0:
    #        print("Aktivirano pravilo:", pravilo)

    # Control system
    window_ctrl = ctrl.ControlSystem(pravila)
    window_sim = ctrl.ControlSystemSimulation(window_ctrl)

    # Set inputs

    #window_sim.input['temperature'] = 60
    #window_sim.input['humidity'] = 10
    i=0
    for e in paradajzDict["uvjeti"]:
        window_sim.input[e["Varijabla"]] = vektor[i]
        i+=1
    #window_sim.input["TemperaturaZraka"] = vektor[3]
    # Compute
    window_sim.compute()
    val = window_sim.output['prozor']


    #for pravilo in window_sim.ctrl.rules:
    #    print(f"Rule: {pravilo}")
    #    print(f"Firing strength: {pravilo.firing_strength}")
    prozor.view(sim=window_sim)
    temperatura.view(sim=window_sim)
    vlaznost.view(sim=window_sim)
    brzinaVjetra.view(sim=window_sim)
    aqi.view(sim=window_sim)
    daLiKisaPada.view(sim=window_sim)
    vrijemeDana.view(sim=window_sim)
    #Views
    #for e in lista_inputa:
    #    e.view()
    print("Window state (0=closed, 1=open):", val)

    mu_zatvori = fuzz.interp_membership(prozor.universe, prozor['zatvori'].mf, val)
    mu_otvori = fuzz.interp_membership(prozor.universe, prozor['otvori'].mf, val)
    mu_nista = fuzz.interp_membership(prozor.universe, prozor['nista ne radi'].mf, val)
    #mu_zatvori=0

    return val, mu_zatvori, mu_otvori, mu_nista
"""
fuzzy, zatvori, otvori, nista = paradajz_fuzzy(vektor)
print("fuzzy:",fuzzy)
print("zatvori:",zatvori)
print("otvori:",otvori)
print("nista:",nista)
"""