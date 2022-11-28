import pandas as pd
from lxml import etree as et

root = et.Element('CalidadDeDatos')
files = ['order_details_informe.csv','data_dictionary_informe.csv','orders_informe.csv','pizza_types_informe.csv','orders_informe_2016.csv','order_details_informe_2016.csv']
for csv in files:
    raw_data = pd.read_csv(csv)

    for row in raw_data.iterrows():
        root_tags = et.SubElement(root, str(csv))

        column_heading_1 = et.SubElement(root_tags,'Field')
        column_heading_2 = et.SubElement(root_tags,'DataType')
        column_heading_3 = et.SubElement(root_tags,'DataCount')
        column_heading_4 = et.SubElement(root_tags,'NullCount')
        column_heading_5 = et.SubElement(root_tags,'NullPercentage')
        column_heading_6 = et.SubElement(root_tags,'NaNCount')
        column_heading_7 = et.SubElement(root_tags,'NaNPercentage')
        column_heading_8 = et.SubElement(root_tags,'UniqueValues')

        column_heading_1.text = str(row[1][0])
        column_heading_2.text = str(row[1]['Data Type'])
        column_heading_3.text = str(row[1]['Data Count'])
        column_heading_4.text = str(row[1]['Null Count'])
        column_heading_5.text = str(row[1]['Null Percentage (%)'])
        column_heading_6.text = str(row[1]['NaN Count'])
        column_heading_7.text = str(row[1]['NaN Percentage (%)'])
        column_heading_8.text = str(row[1]['Unique Values'])

    tree = et.ElementTree(root)
    et.indent(tree, space='\t',level=0)
    tree.write('Calidad_de_datos.xml', encoding='utf-8')