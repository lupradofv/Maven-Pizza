import pandas as pd
import regex as re

class Pizza():
    def __init__(self, idp, cantidad):
        self.idp = idp
        self.cantidad = cantidad 
        self.ingredientes = None 


def encontrar_ids(fechas, mes):
    inicio = '0'+str(int(mes)-1)
    final = '0'+mes
    start_id = 1
    for i in range(fechas.iloc[:,0].count()):
        if fechas.loc[i,'date'][3:5] == inicio[-2:]:
            start_id = fechas.loc[i,'order_id']
        if fechas.loc[i,'date'][3:5] == final[-2:]:
            end_id = fechas.loc[i,'order_id']

    return start_id, end_id

def limites(cantidades_df, start_id,end_id):
    for i in range(cantidades_df.iloc[:,0].count()):
        if cantidades_df.loc[i,'order_id'] == start_id:
            inicio = cantidades_df.loc[i,'order_details_id']
        if cantidades_df.loc[i,'order_id'] == end_id:
            final = cantidades_df.loc[i,'order_details_id']

    return inicio, final

if __name__=='__main__':

    meses = [' ', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    tipos_ingr_df = pd.read_csv('pizza_types.csv')
    cantidades_df = pd.read_csv('order_details.csv')
    fechas = pd.read_csv('orders.csv')

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

    start_id, end_id = encontrar_ids(fechas, mes)
    inicio, final = limites(cantidades_df, start_id,end_id)
    cantidades = cantidades_df.loc[:,['pizza_id','quantity']]
    pizzas_id = []
    pedidos = []

    """ETL.
        Transformar:
        ---------
        Para cada fila del fichero, contamos las cantidades de cada pizza
        que se han consumido, almacenando el valor en la posición correspondiente
        de la lista pedidos.
        """
    for i in range(inicio,final):
        pizza = cantidades.loc[i,'pizza_id']
        if pizza not in pizzas_id:
            pizzas_id.append(pizza)
            pedidos.append(cantidades.loc[i,'quantity'])
        else:
            pos = pizzas_id.index(pizza)
            pedidos[pos] += (cantidades.loc[i,'quantity'])
    
    # Generar nodos para cada pizza con sus cantidades
    pizzas = []
    for i in range(len(pizzas_id)):
        pizza = Pizza(pizzas_id[i], pedidos[i])
        pizzas.append(pizza)


    # Generar un diccionario con los ingredientes de cada pizza
    ingred = dict()
    for i in tipos_ingr_df['pizza_type_id']:
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
    compra_semanal.to_csv(f'Compra_semanal_{meses[int(mes)]}_2015.csv')
