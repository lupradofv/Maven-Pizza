import pandas as pd
import regex as re
from datetime import datetime as stp

class Pizza():
    def __init__(self, idp, cantidad):
        self.idp = idp
        self.cantidad = cantidad 
        self.ingredientes = None 

"""
Encontrar ids:
 - Argumentos:
    - fechas: DataFrame que contiene el id del pedido junto a la fecha de realización
    - mes: mes para el que se solicita el stock
 - Comprobaciones para añadir el id del pedido a la lista:
    - Si la fecha sigue el formato YYYY-MM-DD: comprobamos si coincide el mes
    - Si la fecha sigue el formaro DD-MM-YY H:M:S: comprobamos si coincide el mes 
    - Finalmente, si la fecha contiene el mes buscado en alguno de sus formatos, se añade
"""
def encontrar_ids(fechas, mes):
    ids_mes=[]
    meses = [' ', ['January','Jan'], ['February','Feb'], ['March','Mar'],['April','Apr'], ['May'], ['June','Jun'], ['July','Jul'], ['August','Aug'], ['September','Sep'], ['October','Oct'], ['November','Nov'], ['December','Dec']]
    for i in range(fechas.iloc[:,0].count()):
        if (pd.isna(fechas.loc[i,'date']) == False) and (fechas.loc[i,'date'] != ''):
            try:
                stp.strptime(fechas.loc[i,'date'],"%Y-%m-%d")
                month = '0'+mes
                if fechas.loc[i,'date'][5:7] == month[-2:]:
                    ids_mes.append(fechas.loc[i,'order_id'])
            except:
                ...
            try:
                stp.strptime(fechas.loc[i,'date'],"%d-%m-%y %H:%M:%S")
                month = '0'+mes
                if fechas.loc[i,'date'][3:5] == month[-2:]:
                    ids_mes.append(fechas.loc[i,'order_id'])
            except:
                ...
            for j in meses[int(mes)]:
                if j in fechas.loc[i,'date']:
                    ids_mes.append(fechas.loc[i,'order_id'])

    return ids_mes

"""
Procesar pizza:
"""
def procesar_pizza(p):
    fin = 0
    for char in p:
        if char.isalpha():
            fin += 1
        elif char == '@':
            p=p.replace('@','a')
            fin += 1
        elif char == '0':
            p=p.replace('0','o')
            fin += 1
        elif char =='3':
            p=p.replace('3','e')
            fin += 1
        else:
            if p[:fin] == 'ckn':
                if p[4]== 'p':
                    return 'ckn_p'
                else:
                    return 'ckn_a'
            else:
                return p[:fin]
   
    return p[:fin]

"""
Cantidades_ids:
 - Argumentos:
    - cantidades: DataFrame que contiene el id del pedido junto con el id de la pizza y la cantidad comprada
    - ids_mes: los ids de pedidos correspondientes al mes
 - Selección:
    Iteramos las filas del DataFrame y si el id del pedido se encuentra en la lista de ids del mes:
     - Si el id de la pizza no se encuentra en la lista, se añade, y se genera un nuevo contador para la centidad pedida en la lista de pedidos
     - Si el id de la pizza ya se encuentra en la lista, se suma la cantidad pedida al contador ya existente en la lista de pedidos según la posicion
 - Comprobaciones:
    - Es necesario asegurar que si la cantidad si introduce como un string esta se transforme al número correspondiente
    - Si no tiene un número asociado, no añadimos el id a la lista
"""
def cantidades_ids(cantidades_df,ids_mes):

    pizzas_id = []
    pedidos = []
    for i in range(cantidades_df.iloc[:,0].count()):
        p = cantidades_df.loc[i,'pizza_id']
        if not pd.isna(p):
            pizza = procesar_pizza(p)
            if (pd.isna(cantidades_df.loc[i,'order_id']) == False) and (cantidades_df.loc[i,'order_id'] in ids_mes):
                if pizza not in pizzas_id:
                    try:
                        pedidos.append(abs(int(cantidades_df.loc[i,'quantity'])))
                        pizzas_id.append(pizza)
                    except:
                        uno = ['One','one']
                        dos = ['Two','two']
                        if cantidades_df.loc[i,'quantity'] in uno:
                            pedidos.append(1)
                            pizzas_id.append(pizza)
                        elif cantidades_df.loc[i,'quantity'] in dos:
                            pedidos.append(2)
                            pizzas_id.append(pizza)
                else:
                    pos = pizzas_id.index(pizza)
                    try:
                        pedidos[pos] += abs(int(cantidades_df.loc[i,'quantity']))
                    except:
                        uno = ['One','one']
                        dos = ['Two','two']
                        if (cantidades_df.loc[i,'quantity']) in uno:
                            pedidos[pos]+=1
                        elif (cantidades_df.loc[i,'quantity']) in dos:
                            pedidos[pos]+=2

    return pizzas_id,pedidos

                
if __name__=='__main__':

    meses = [' ', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    tipos_ingr_df = pd.read_csv('pizza_types.csv')
    cantidades_df = pd.read_csv('order_details.csv',delimiter=';')
    fechas = pd.read_csv('orders.csv',delimiter=';')

    valido = False
    while not valido:
        mes = input('Select month to generate stock needed (1/12):')
        try: 
            if (int(mes) <= 12) and (int(mes) >= 1) and mes.isnumeric():
                valido = True
            else:
                print('Introduce a valid month number.')
        except:
            print('Introduce a valid month number.')

    ids_mes = encontrar_ids(fechas, mes)

    # Para cada fila del fichero, contamos las cantidades de cada pizza que se han consumido, almacenando el valor en la posición correspondiente de la lista pedidos.
    # si el id de la pizza no esta en la lista, se añade y se crea un nuevo registro para la cantidad de esta en la lis de pedidos
    # si si esta en la lista, sumas el valor de cantidad a la cantidad ya existente en la lista de pedidos
    # controlar si el numero se introduce como un string y solo añadir el id de la pizza a la lista en el caso de que 
    # esta tenga una cantidad asociada

    pizzas_id,pedidos = cantidades_ids(cantidades_df, ids_mes)

    # Generar nodos para cada pizza con sus cantidades
    pizzas = []
    for i in range(len(pizzas_id)):
        pizza = Pizza(pizzas_id[i], pedidos[i])
        pizzas.append(pizza)


    # Generar un diccionario con los ingredientes de cada pizza
    ingred = dict()
    for i in tipos_ingr_df['pizza_type_id']:
        try:
            pid = re.match("(.*?)_",i).group()[:-1]
            if pid == 'ckn':
                ingred[i[:5]] = re.findall('(?<=").*$', i)[0]
            else:
                ingred[pid] = re.findall('(?<=").*$', i)[0]
        except:
            ingred[re.match("(.*?),",i).group()[:-1]] = re.findall('(?<=").*$', i)[0]

    # Asociar los ingredientes a la pizza correspondiente (comparar los nodos ya existentes con las claves del diccionario)
    for i in range(len(pizzas)):
        for j in ingred.keys():
            if j in pizzas[i].idp:
                pizzas[i].ingredientes = ingred.get(j)[:-1]

    # Revisar todos los nodos añadiendo a una lista con los ingredientes
    # según se procesan (sumar si está, si no crear).
    ingredientes_cant = dict()
    for i in range(len(pizzas)):
        prod = pizzas[i].ingredientes.split(',')
        for j in range(len(prod)):
            if prod[j] in ingredientes_cant.keys():
                # si el ingrediente ya esta en el diccionario se suma la cantidad que corresponde a las ventas de la pizza
                ingredientes_cant[prod[j]] = ingredientes_cant.get(prod[j])+pizzas[i].cantidad
            else:
                ingredientes_cant[prod[j]] = pizzas[i].cantidad

    # Ingredientes_cant tiene 52 semanas de ingredientes: generar media de ingredientes semanales
    for k, v in ingredientes_cant.items():
        ingredientes_cant[k] = int(v//4.4)

    # Obtenemos un diccionario que contiene todos los ingredientes que se han consumido de media en todas las semanas de 2015

    compra_semanal = pd.DataFrame()
    compra_semanal['Ingrediente'] = ingredientes_cant.keys()
    compra_semanal['Cantidad (unidades)'] = ingredientes_cant.values()
    compra_semanal.to_csv(f'Compra_semanal_{meses[int(mes)]}.csv')