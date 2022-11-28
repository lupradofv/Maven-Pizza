import pandas as pd
import regex as re
from datetime import datetime as stp
from pandas import ExcelWriter

class Pizza():
    def __init__(self, idp, cantidad):
        self.idp = idp
        self.cantidad = cantidad 
        self.precio = None 
        self.ingresos = None
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
    p = p.strip()
    for char in p:
        if char == '@':
            p=p.replace('@','a')
        elif char == '0':
            p=p.replace('0','o')
        elif char =='3':
            p=p.replace('3','e')
        elif char == ' ':
            p=p.replace(' ','_')
        elif char == '-':
            p=p.replace('-','_')
   
    return p


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

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    tipos_ingr_df = pd.read_csv('pizza_types.csv')
    cantidades_df = pd.read_csv('order_details.csv',delimiter=';')
    fechas = pd.read_csv('orders.csv',delimiter=';')
    precios_df = pd.read_csv('pizzas.csv')

    dics_ingred = []
    dics_ingresos = []
    dics_ventas = []

    for j in range(1,13):
    
        ids_mes = encontrar_ids(fechas, str(j))

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

        # Generar un diccionario con los precios de cada pizza
        precios = dict()
        for row in precios_df.iterrows():
            precios[row[1]['pizza_id']] = row[1]['price']

        for i in range(len(pizzas)):
            for j in precios.keys():
                if j in pizzas[i].idp:
                    pizzas[i].precio = precios.get(j)
                    pizzas[i].ingresos = pizzas[i].precio*pizzas[i].cantidad

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

        dics_ingred.append(ingredientes_cant)

        ingresos_mes = dict()
        for i in range(len(pizzas)):
            ingresos_mes[pizzas[i].idp] = pizzas[i].ingresos
        dics_ingresos.append(ingresos_mes)

        ventas_mes = dict()
        for i in range(len(pizzas)):
            ventas_mes[pizzas[i].idp] = pizzas[i].cantidad
        dics_ventas.append(ventas_mes)


    for i in range(len(dics_ingred)): 
        df_ingresos = pd.DataFrame({'Pizza': dics_ingresos[i].keys(),f'{meses[i]}': dics_ingresos[i].values()})
        df_ingresos = df_ingresos[['Pizza', f'{meses[i]}']]
        sorted_df_ingresos = df_ingresos.sort_values(by='Pizza')

        df_ventas = pd.DataFrame({'Pizza': dics_ventas[i].keys(),f'{meses[i]}': dics_ventas[i].values()})
        df_ventas = df_ventas[['Pizza', f'{meses[i]}']]
        sorted_df_ventas = df_ventas.sort_values(by='Pizza')

        df_ingred = pd.DataFrame({'Ingrediente': dics_ingred[i].keys(),f'{meses[i]}': dics_ingred[i].values()})
        df_ingred = df_ingred[['Ingrediente', f'{meses[i]}']]
        sorted_df_ingred = df_ingred.sort_values(by='Ingrediente')


        if i == 0:
            df_final_ingresos = sorted_df_ingresos.reset_index(drop = True)
            df_final_ingred = sorted_df_ingred.reset_index(drop = True)
            df_final_ventas = sorted_df_ventas.reset_index(drop = True)
        else:
            df1_ingresos = sorted_df_ingresos.reset_index(drop = True)
            df_final_ingresos = pd.merge(df_final_ingresos, df1_ingresos,on='Pizza',how='inner')

            df1_ingred = sorted_df_ingred.reset_index(drop = True)
            df_final_ingred = pd.merge(df_final_ingred, df1_ingred,on='Ingrediente',how='inner')

            df1_ventas = sorted_df_ventas.reset_index(drop = True)
            df_final_ventas = pd.merge(df_final_ventas, df1_ventas,on='Pizza',how='inner')

    writer_ingresos = ExcelWriter('Ingresos_Mensuales_Pizzas.xlsx')
    df_final_ingresos.to_excel(writer_ingresos, 'Hoja de datos', index=False)
    writer_ingresos.save() 

    writer_ventas = ExcelWriter('Ventas_Mensuales_Pizzas.xlsx')
    df_final_ventas.to_excel(writer_ventas, 'Hoja de datos', index=False)
    writer_ventas.save() 

    writer_ingred = ExcelWriter('Compras_Mensuales_Ingredientes.xlsx')
    df_final_ingred.to_excel(writer_ingred, 'Hoja de datos', index=False)
    writer_ingred.save()