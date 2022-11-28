import pandas as pd
import regex as re
import numpy as np
import os, img2pdf
from PyPDF2 import PdfMerger
import matplotlib.pyplot as plt
from xhtml2pdf import pisa       

class Pizza():
    def __init__(self, idp, cantidad):
        self.idp = idp
        self.cantidad = cantidad 
        self.precio = None 
        self.ingresos = None
        self.ingredientes = None 

def plot(data, filename,mes):
    plt.figure(figsize=(12, 4))
    plt.grid(color='#F2F2F2', alpha=1, zorder=0)
    plt.plot(data['Pizza'], data['Ingresos'], color='#087E8B', lw=3, zorder=5)
    plt.title(f'Ingresos por Pizza: {mes}', fontsize=15)
    plt.xlabel('Pizza', fontsize=13)
    plt.xticks(fontsize=7, rotation=90, ha='right')
    plt.ylabel('Ingresos', fontsize=13)
    plt.yticks(fontsize=9)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return

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

    nombres_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    tipos_ingr_df = pd.read_csv('pizza_types.csv')
    cantidades_df = pd.read_csv('order_details.csv',delimiter=';')
    fechas = pd.read_csv('orders.csv',delimiter=';')
    precios_df = pd.read_csv('pizzas.csv')
    
    dics_ingred = []

    
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
            for clave in precios.keys():
                if clave in pizzas[i].idp:
                    pizzas[i].precio = precios.get(clave)
                    pizzas[i].ingresos = pizzas[i].precio*pizzas[i].cantidad


        ingresos_mes = dict()
        for i in range(len(pizzas)):
            ingresos_mes[pizzas[i].idp] = pizzas[i].ingresos
        
        df = pd.DataFrame()
        df['Pizza'] = ingresos_mes.keys()
        df['Ingresos'] = ingresos_mes.values()
        
        plot(data=df, filename=f'{nombres_mes[j-1]}.png', mes=nombres_mes[j-1])

        ingred = dict()
        for i in tipos_ingr_df['pizza_type_id']:
            ingred[re.match("(.*?),",i).group()[:-1]] = re.findall('(?<=").*$', i)[0]
        for i in range(len(pizzas)):
            for j in ingred.keys():
                if j in pizzas[i].idp:
                    pizzas[i].ingredientes = ingred.get(j)[:-1]

        ingredientes_cant = dict()
        for i in range(len(pizzas)):
            prod = pizzas[i].ingredientes.split(',')
            for j in range(len(prod)):
                pr = prod[j].strip()
                if pr in ingredientes_cant.keys():
                    # si el ingrediente ya esta en el diccionario se suma la cantidad que corresponde a las ventas de la pizza
                    ingredientes_cant[pr] = ingredientes_cant.get(pr)+pizzas[i].cantidad
                else:
                    ingredientes_cant[pr] = pizzas[i].cantidad

        for k, v in ingredientes_cant.items():
            ingredientes_cant[k] = int(v//4.4)

        dics_ingred.append(ingredientes_cant)

    ingreds_mes = []
    for i in range(12): 
        string = ''
        for k, v in dics_ingred[i].items():
            string += f'{k}: {v}, '
        ingreds_mes.append(string)

    # to open/create a new html file in the write mode
    f = open('Ingredientes.html', 'w')
    html_template = """<html>
    <head>
    <title>Title</title>
    </head>
    <body>
    <h2>COMPRA DE INGREDIENTES POR MES</h2>"""

    for i in range(12):
        html_template+= f"<br>{nombres_mes[i]}<br><p>{ingreds_mes[i]}</p>"
    
    html_template += "</body> </html>"
   
    text_file = open('Ingredientes.pdf', 'w+b')
    p = pisa.CreatePDF(html_template, text_file)
    text_file.close()

    merger = PdfMerger()
    merger.append('Ingredientes.pdf')

    for i in range(12):
        with open(f'{nombres_mes[i]}.pdf', "wb") as documento:
	        documento.write(img2pdf.convert(f'{nombres_mes[i]}.png'))

    

    for i in range(12):
            merger.append(f'{nombres_mes[i]}.pdf')
    
    merger.write("Reporte_Ejecutivo.pdf")
    merger.close()



    