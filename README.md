# hackaton_BBVA
Aqui se encuentra todo el codigo para reproducir el resultado del reto **Identificacion de datos de fraude**

- Nombre: Nombre	El nombre y apellido están concatenados en la columna desc_text. Usamos la información en la columna desc_id, que indican las 2 primeras letras del nombre y las 2 primeras letras del apellido.
- Tarjeta de crédito:	Concatenar columnas producto_1_number y bin_2 number, convertir el resultado de binario a decimal para obtener los primeros 6 dígitos de la TDC. Los 10 números restantes se obtienen de la columna tel_id.
- Dirección:	Invertir dirección de la cadena de caracteres y separar números de letras, así como palabras mediante el uso de letras mayúsculas.
- Fecha de nacimiento:	En el campo registro.xls, después de quitar las palabras "Version" y ".xls" encontramos el año_mes y después  en el campo clave_id corroboramos ambos datos y agregamos el día. Al final con el campo clave_id pasamos al formato yyyy-mm-dd 
- E-mail:	La parte identificadora del correo se conforma de la primera letra del nombre y el apellido. Para ocultar la información se añadieron caracteres al final caracteres en base 37 (0-9 y a-z). Para la parte del dominio combinamos con la columna apellido@_text en donde reemplazamos el caracter ! con '.com' 
