import json
import os
from collections import defaultdict
from datetime import datetime

cuenta_path = "cuentas.json"
transacciones_path = "transacciones.csv"

class Cuenta:
    def __init__(self, nombre, divisa, balance=0):
        self.nombre = nombre
        self.divisa = divisa
        self.balance = balance

    def accreditar(self, debito, cantidad):
        fecha = input("cual es la fecha de una transaccion? ")
        fecha = fecha if fecha != "" else str(datetime.today())[:10]
            
        self.balance = float(self.balance) - cantidad

        transaccion = f"{fecha},{self.nombre},{debito},{self.divisa},{cantidad}"
        rec_csv(transaccion, transacciones_path)

        return None

    def debitar(self, credito, cantidad):
        fecha = input("cual es la fecha de una transaccion? ")
        fecha = fecha if fecha != "" else str(datetime.today())[:10]

        self.balance = float(self.balance) + cantidad
        
        transaccion = f"{fecha},{credito},{self.nombre},{self.divisa},{cantidad}"
        rec_csv(transaccion, transacciones_path)

        return None

def rec_csv(str_item, f_path):
    with open(f_path, "a") as f:
        f.write("\n"+str_item)
    print(f"record {str_item} added to {f_path.split('.')[0]}")
    
    return None

def cuenta_anadir(cuentas, start_cuentas_list):
    cuentas = {nombre: cuentas[nombre].__dict__ for nombre in start_cuentas_list}
    cuenta_nuevo = Cuenta(
        input("que es nombre del cuenta? "), 
        input("que es diviso del cuenta? ")
    )

    if cuenta_nuevo.nombre in cuentas:
        print(
            f"la {cuenta_nuevo.divisa} cuenta '{cuenta_nuevo.nombre}' ya existe"
        )
    else:
        cuentas[cuenta_nuevo.nombre] = {
            "nombre": cuenta_nuevo.nombre,
            "divisa": cuenta_nuevo.divisa,
            "balance": 0
        }
        json.dump(cuentas, open(cuenta_path, "w"))
        print(
            f"la {cuenta_nuevo.divisa} cuenta '{cuenta_nuevo.nombre}' esta lista"
        )

        return None

def cuentas_enumerar(cuentas):
    print("todas las cuentas disponsibles estan:")
    for n, cuenta in enumerate(cuentas):
        print(n, cuenta,":",cuentas[cuenta].__dict__)

    return None

def debitar(cuentas, start_cuentas_list):
    cuenta_nombre = input("que es nombre del cuenta? ")
    if cuenta_nombre in start_cuentas_list:
        cuentas[cuenta_nombre].debitar(
            input("que es debito? "),
            float(input("que cantidad quieres debitar? "))
        )
        cuentas = {nombre: cuentas[nombre].__dict__ for nombre in start_cuentas_list}
        json.dump(cuentas, open(cuenta_path, "w"))
    else:
        print(f"cuenta {cuenta_nombre} no existe")

    return Nonecr

def accreditar(cuentas, start_cuentas_list):
    cuenta_nombre = input("que es nombre del cuenta? ")
    if cuenta_nombre in start_cuentas_list:
        cuentas[cuenta_nombre].accreditar(
            input("que es debito? "),
            float(input("que cantidad quieres accreditar? "))
        )
        cuentas = {nombre: cuentas[nombre].__dict__ for nombre in start_cuentas_list}
        json.dump(cuentas, open(cuenta_path, "w"))
    else:
        print(f"cuenta {cuenta_nombre} no existe")

    return None

def cuentas_obtener():
    cuentas = dict()
    cuentas_todos = json.load(open(cuenta_path, "rb"))
    for cuenta_nombre in cuentas_todos:
        cuentas[cuenta_nombre] = Cuenta(
            cuenta_nombre,
            cuentas_todos[cuenta_nombre]["divisa"],
            cuentas_todos[cuenta_nombre]["balance"]
            )
    start_cuentas_list = list(cuentas_todos.keys())

    return cuentas, start_cuentas_list

def entre_cuentas_transferir(cuentas, start_cuentas_list, fecha=None):
    cuenta_credito = input("que es nombre del cuenta credito? ")
    cuenta_debito = input("que es nombre del cuenta debito? ")
    
    if (cuenta_credito in start_cuentas_list) & (cuenta_debito in start_cuentas_list):
        cantidad = int(input("que candidad transferir? "))
        cuentas[cuenta_credito].balance = int(cuentas[cuenta_credito].balance) - cantidad
        cuentas[cuenta_debito].balance = int(cuentas[cuenta_debito].balance) + cantidad
        fecha = fecha if fecha else str(datetime.today())[:10]
        transaccion = f"{fecha},{cuenta_credito},{cuenta_debito},{cuentas[cuenta_credito].divisa},{cantidad}"
        cuentas = {nombre: cuentas[nombre].__dict__ for nombre in start_cuentas_list}
        json.dump(cuentas, open(cuenta_path, "w"))
        rec_csv(transaccion, transacciones_path)
    else:
        print(f"cuenta {[x for x in [cuenta_credito,cuenta_debito] if x not in start_cuentas_list]} no existe")
        
    return None
       
