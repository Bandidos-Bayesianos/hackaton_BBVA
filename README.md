# hackaton_BBVA
Aqui se encuentra todo el codigo para reproducir el resultado del reto **Identificacion de datos de fraude**

- Nombre: Nombre	El nombre y apellido están concatenados en la columna desc_text. Usamos la información en la columna desc_id, que indican las 2 primeras letras del nombre y las 2 primeras letras del apellido.
- Tarjeta de crédito:	Concatenar columnas producto_1_number y bin_2 number, convertir el resultado de binario a decimal para obtener los primeros 6 dígitos de la TDC. Los 10 números restantes se obtienen de la columna tel_id.
- Dirección:	Invertir dirección de la cadena de caracteres y separar números de letras, así como palabras mediante el uso de letras mayúsculas.
- Fecha de nacimiento:	En el campo registro.xls, después de quitar las palabras "Version" y ".xls" encontramos el año_mes y después  en el campo clave_id corroboramos ambos datos y agregamos el día. Al final con el campo clave_id pasamos al formato yyyy-mm-dd 
- E-mail:	La parte identificadora del correo se conforma de la primera letra del nombre y el apellido. Para ocultar la información se añadieron caracteres al final caracteres en base 37 (0-9 y a-z). Para la parte del dominio combinamos con la columna apellido@_text en donde reemplazamos el caracter ! con '.com' 
- Teléfono móvil:	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}
-Teléfono fijo:	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}
- CURP:	Con el nombre y fecha de nacimiento calculados más los campos agrupacion_id en el que está el sexo y estado utilizamos una función que calcula el CURP. Sabemos que en los datos existe la columna CURP en la que están los cinco digitos asignados, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato
- INE:	Utilizando el curp que calculamos y el campo cvv_secreto en el que encontramos el número aleatorio de tres dígitos (relleno con ceros) calculamos la clave de elector 
- RFC:	Con el nombre y la fecha de nacimiento que obtuvimos utilizamos una función que calcula el RFC. Sabemos que en la columna producto_id se encuentra la homoclave, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato
- NSS:	Convertimos la columna NSS de octal a decimal
- Pasaporte:	Convertimos la columna pasaporte de hexadecimal a decimal 
El calculo del curp se hizo tomando como base https://github.com/epalomeque/py-curprfc
