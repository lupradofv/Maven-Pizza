# STOCK SEMANAL DE PIZZAS 2015 (INFORME DE CALIDAD; TRANSFORMA Y GENERA CSV)

Extraer:

Cargar los datos del archivo csv mediante la librería pandas. Empleamos los datos de los siguientes csv: - Pizza_types.csv: almacena el id de pizza, el nombre, la categoría asociada y los ingredientes. - Order_details: almacena todos los pedidos realizados (mantenemos únicamente las columnas de: id de la pizza y la cantidad solicitada). - Orders: almacena el id de cada pedido junto a la fecha en la que este se ha realizado

------------------------
Transformar:

Se solicita el mes para el que se quiere generar la previsión de existencias, introduciendo por pantalla el numero que corresponda al mes.

Función encontrar ids: Empleando el numero de mes, se iteran las filas del fichero que contiene las fechas de realización de pedidos, y devuelve el id del primer y último pedido realizado en dicho mes.

Función límites: Empleando los ids del primer y ultimo pedido del mes, se itera el fichero que contiene el id del pedido junto al id de la pizza, y devuelve el rango de pedidos en el fichero que corresponde al mes (posición inicial y final en el fichero). Para cada fila del fichero en el intervalo obtenido para el mes solicitado, se registra la cantidad de cada pizza que se ha consumido, almacenando el valor en la posición correspondiente de la lista pedidos. Procesamiento de la información obtenida a una lista de nodos: almacena el id de pizza junto a la cantidad. Procesamiento de los datos de pizza_types.csv para generar un diccionario con los ingredientes de las pizzas: asociar los ingredientes al nodo. Generar un diccionario con los pares ingrediente cantidad para los pedidos realizados a lo largo de 2015: procesar los nodos y sus ingredientes correspondientes y registrar según la cantidad que corresponde a las ventas de la pizza en cuestión.

Cargar:

Generar un Data Frame que contenga los ingredientes junto con su stock semanal: generar un csv con la compra semanal.

# STOCK SEMANAL DE PIZZAS 2016 (INFORME DE CALIDAD; TRANSFORMA Y GENERA CSV)

Extraer:

Cargar los datos del archivo csv mediante la librería pandas. Empleamos los datos de los siguientes csv: - Pizza_types.csv: almacena el id de pizza, el nombre, la categoría asociada y los ingredientes. - Order_details: almacena todos los pedidos realizados (mantenemos únicamente las columnas de: id de la pizza y la cantidad solicitada). - Orders: almacena el id de cada pedido junto a la fecha en la que este se ha realizado

---------------------------------
Transformar:

Se solicita el mes para el que se quiere generar la previsión de existencias, introduciendo por pantalla el numero que corresponda al mes.

Función encontrar ids: Empleando el numero de mes, se iteran las filas del fichero que contiene las fechas de realización de pedidos, y devuelve el id del primer y último pedido realizado en dicho mes.

Función límites: Empleando los ids del primer y ultimo pedido del mes, se itera el fichero que contiene el id del pedido junto al id de la pizza, y devuelve el rango de pedidos en el fichero que corresponde al mes (posición inicial y final en el fichero). Para cada fila del fichero en el intervalo obtenido para el mes solicitado, se registra la cantidad de cada pizza que se ha consumido, almacenando el valor en la posición correspondiente de la lista pedidos. Procesamiento de la información obtenida a una lista de nodos: almacena el id de pizza junto a la cantidad. Procesamiento de los datos de pizza_types.csv para generar un diccionario con los ingredientes de las pizzas: asociar los ingredientes al nodo. Generar un diccionario con los pares ingrediente cantidad para los pedidos realizados a lo largo de 2015: procesar los nodos y sus ingredientes correspondientes y registrar según la cantidad que corresponde a las ventas de la pizza en cuestión.

Cargar:

Generar un Data Frame que contenga los ingredientes junto con su stock semanal: generar un csv con la compra semanal

# ARCHIVO XML

El repositorio dispone además del código necesario para generar un reporte de tipología de datos en formato XML.

# ARCHIVO EXCEL

Incluye un reporte ejecutivo, un reporte de ingredientes y un reporte de pedidos para los datos registrados sobre ventas y existencias de Maven Pizzas (2016).

# ARCHIVO PDF

Reporte ejecutivo para el COO de Maven Pizzas: abarca las existencias necesarias por mes (2016) y los ingresos generados mediante la venta de cada tipo de pizza (2016).
