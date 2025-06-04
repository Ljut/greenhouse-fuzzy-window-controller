import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json

with open("paradajz.json", "r") as json_file:
    paradajzDict = json.load(json_file)

varijable = {
    "TemperaturaZraka":20,
    "VlaznostZraka":9,
    "BrzinaVjetra":5,
    "AQI":0,
    "DaLiPadaKisa":False,
    "VrijemeDana":13,
}

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
    
    prozor['zatvori'] = fuzz.trimf(prozor.universe, [0, 0, 0.5])
    prozor['nista ne radi'] = fuzz.trimf(prozor.universe, [0.4, 0.5, 0.6])
    prozor['otvori'] = fuzz.trimf(prozor.universe, [0.5, 1, 1])
    
    temperatura = lista_inputa[0]
    vlaznost = lista_inputa[1]
    brzinaVjetra = lista_inputa[2]
    aqi = lista_inputa[3]
    daLiKisaPada = lista_inputa[4]
    vrijemeDana = lista_inputa[5]
    # Rules
    pravila = []
    pravila.append(ctrl.Rule())
    pravila.append(ctrl.Rule(aqi['dobro'] & (brzinaVjetra["slab"] | brzinaVjetra["nema"]) & temperatura['vruce'] & vlaznost["suho"] & ~daLiKisaPada["ne pada kisa"] & vrijemeDana['noc'],prozor["otvori"]))
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

    """pravila.append(ctrl.Rule(vrijemeDana['noc'] & temperatura['taman-za-dan'], prozor["otvori"]))
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
    pravila.append(ctrl.Rule(~aqi["dobro"] | ~aqi["umjereno"],prozor["zatvori"]))"""
    
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

    # Compute
    window_sim.compute()
    val = window_sim.output['prozor']

    #Views
    for e in lista_inputa:
        e.view()
    print("Window state (0=closed, 1=open):", val)


    return val


def do_fuzzy(vektor):
    val = 0


    # Define input variables
    temperature = ctrl.Antecedent(np.arange(-40, 81, 1), 'temperature')
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

    # Define output variable with more points
    window = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'window')

    # Membership functions
    temperature['cold'] = fuzz.trimf(temperature.universe, [-40, -40, 15])
    temperature['warm'] = fuzz.trimf(temperature.universe, [10, 25, 40])
    temperature['hot'] = fuzz.trimf(temperature.universe, [35, 80, 80])

    humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 50])
    humidity['humid'] = fuzz.trimf(humidity.universe, [30, 100, 100])

    window['closed'] = fuzz.trimf(window.universe, [0, 0, 0.5])
    window['open'] = fuzz.trimf(window.universe, [0.5, 1, 1])

    # Rules
    rule1 = ctrl.Rule(temperature['hot'] & humidity['dry'], window['open'])
    rule2 = ctrl.Rule(temperature['cold'] | humidity['humid'], window['closed'])

    # Control system
    window_ctrl = ctrl.ControlSystem([rule1, rule2])
    window_sim = ctrl.ControlSystemSimulation(window_ctrl)

    # Set inputs
    window_sim.input['temperature'] = 60
    window_sim.input['humidity'] = 10

    # Compute
    window_sim.compute()
    print("Consequents:", [c.label for c in window_sim.ctrl.consequents])
    for var in window_sim.output:
        print("Window state (0=closed, 1=open):", var)

    print("Window state (0=closed, 1=open):", window_sim.output['window'])

    # View
    temperature.view()
    humidity.view()
    window.view()

    return val


#do_fuzzy(vektor)

print(paradajz_fuzzy(vektor))