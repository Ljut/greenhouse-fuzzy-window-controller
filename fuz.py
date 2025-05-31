import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json

with open("paradajz.json", "r") as json_file:
    paradajzDict = json.load(json_file)

varijable = {
    "TemperaturaZraka":0,
    "VlaznostZraka":0,
    "BrzinaVjetra":0,
    "AQI":0,
    "DaLiPadaKisa":True,
    "VrijemeDana":0,
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

    temperatura = lista_inputa[0]
    vlaznost = lista_inputa[1]
    brzinaVjetra = lista_inputa[2]
    aqi = lista_inputa[3]
    daLiKisaPada = lista_inputa[4]
    vrijemeDana = lista_inputa[5]

    # Define output variable with more points
    prozor = ctrl.Consequent(np.arange(0, 1.1, 0.5), 'prozor')

    # Membership functions
    
    i=0
    for i in range(len(lista_inputa)):
        lin_var = paradajzDict["uvjeti"][i]["Lingvisticki model varijable"]
        #for j in range(len(lin_var)):
        #    print(lin_var[j]["ime"])
        
        for e in lin_var:
            if e["ime"]=="noc":
                noc_morning = fuzz.trapmf(lista_inputa[i].universe, [0, 0, 4, 7])
                noc_evening = fuzz.trapmf(lista_inputa[i].universe, [19, 21, 24, 24])
                lista_inputa[i][e["ime"]] = np.fmax(noc_morning, noc_evening)
            elif len(e["domen"])==3:
                lista_inputa[i][e["ime"]]= fuzz.trimf(lista_inputa[i].universe, e["domen"])
            elif len(e["domen"])==4:
                lista_inputa[i][e["ime"]]= fuzz.trapmf(lista_inputa[i].universe, e["domen"])
        
            #fuzz.trapmf(var.universe, lin_var["Lingvisticki model varijable"][i]["domen"])
        #lista_inputa[i][paradajzDict["uvjeti"]["Lingvisticki model varijable"][i]["ime"]]
        
    """for var in lista_inputa:
        i=0
        for lin_var in paradajzDict["uvjeti"]:
            #print("\n",lin_var["Lingvisticki model varijable"][i]["ime"])
            #print(lin_var["Lingvisticki model varijable"][i]["domen"])
            #if(len(lin_var["Lingvisticki model varijable"][i]["domen"])==3):
            #    var[lin_var["Lingvisticki model varijable"][i]["ime"]] = fuzz.trimf(var.universe, lin_var["Lingvisticki model varijable"][i]["domen"])
            #else: #trapez
            #    var[lin_var["Lingvisticki model varijable"][i]["ime"]] = fuzz.trapmf(var.universe, lin_var["Lingvisticki model varijable"][i]["domen"])
            # Ako je noć
            #if isinstance(lin_var["Lingvisticki model varijable"][i]["domen"][0], list):
            
            print(lin_var["Lingvisticki model varijable"][i]["ime"])
            if lin_var["Lingvisticki model varijable"][i]["ime"]=="noc":
                noc_morning = fuzz.trapmf(var.universe, [0, 0, 4, 7])
                noc_evening = fuzz.trapmf(var.universe, [19, 21, 24, 24])
                var['noc'] = np.fmax(noc_morning, noc_evening)
            else:
                var[lin_var["Lingvisticki model varijable"][i]["ime"]] = fuzz.trimf(var.universe, lin_var["Lingvisticki model varijable"][i]["domen"]) if len(lin_var["Lingvisticki model varijable"][i]["domen"]) == 3 else fuzz.trapmf(var.universe, lin_var["Lingvisticki model varijable"][i]["domen"])
            i+=1"""
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