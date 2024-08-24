import random
import os

carritosDisponibles = 6
listaNombres = ["Ana", "Joao", "Roberto", "Maria", "Pepe", "Dardo", "Coqui", "Maravilla"]

class Persona():
    def __init__(self, nombre = listaNombres[random.randint(0, len(listaNombres) - 1)]):
        self.nombre = nombre

class Nodo:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.next = None
 
 
class Queue:
    def __init__(self):
        self.final = None
        self.frente = None
        self.count = 0
 

    def sacarDeCola(self):          
        if self.frente is None:
            print('Cola vacia')
            exit(-1)
 
        actual = self.frente
        self.frente = self.frente.next

        if self.frente is None:
            self.final = None
 
        self.count -= 1
        return actual.data
 
    def agregarACola(self, item):    
        nodo = Nodo(item)

        if self.frente is None:
            self.frente = nodo
            self.final = nodo
        else:
            self.final.next = nodo
            self.final = nodo
 
        self.count += 1
 
 
    def isEmpty(self):
        return self.final is None and self.frente is None
 
    def size(self):
        return self.count

filaCaja1 = Queue()
filaCaja2 = Queue()
filaCarritos = Queue()


def displayEstadoGeneral():
    filaCarritosString = str()
    for i in range(filaCarritos.size()):
        filaCarritosString += "P "
    carritosDisponiblesString = "[CARRITOS]"
    for i in range(carritosDisponibles):
        carritosDisponiblesString += " [++]´ "
    print(carritosDisponiblesString + "\t" + filaCarritosString)

    filaCaja1String = "\n[CAJA]\t"
    filaCaja2String = "[CAJA]\t"

    for i in range(filaCaja1.size()):
        filaCaja1String += "0 "
    for i in range(filaCaja2.size()):
        filaCaja2String += "0 "
    print(filaCaja1String)
    print(filaCaja2String)




def filaConMenosCola():
    if filaCaja2.size() > filaCaja1.size():
        return filaCaja1
    elif filaCaja1.size() > filaCaja2.size():
        return filaCaja2
    else:
        return filaCaja1

def ingresoDeCliente():
    global carritosDisponibles
    filaCarritos.agregarACola(Nodo(Persona()))
    if carritosDisponibles >= 1:
        cliente = filaCarritos.sacarDeCola()
        carritosDisponibles -= 1
        filaConMenosCola().agregarACola(cliente)
    else:
        None

def cobrarEnCaja():
    global carritosDisponibles
    atenderEnCaja1 = not filaCaja1.isEmpty()
    atenderEnCaja2 = not filaCaja2.isEmpty()
    if atenderEnCaja1:
        filaCaja1.sacarDeCola()
        carritosDisponibles += 1
        if filaCarritos.isEmpty():
            None
        else:
            cliente = filaCarritos.sacarDeCola()
            carritosDisponibles -= 1
            filaConMenosCola().agregarACola(cliente)
    if atenderEnCaja2:
        filaCaja2.sacarDeCola()
        carritosDisponibles += 1
        if filaCarritos.isEmpty():
            None
        else:
            cliente = filaCarritos.sacarDeCola()
            carritosDisponibles -= 1
            filaConMenosCola().agregarACola(cliente)
        
    

    
while True:
    ans = int(input("Ingrese una opcion:\n(1) Ingreso de cliente\n(2) Cobro en caja\n"))
    if ans == 1:
        ingresoDeCliente()
        os.system("cls")
        displayEstadoGeneral()
        print("\n")
    elif ans == 2:
        cobrarEnCaja()
        os.system("cls")
        displayEstadoGeneral()
        print("\n")
    else:
        os.system("cls")
        print("Opción no válida")
