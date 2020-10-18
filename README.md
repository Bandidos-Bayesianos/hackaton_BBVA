# hackaton_BBVA
Aquí se encuentra todo el código para reproducir el resultado del reto **Identificación de datos de fraude**

- Nombre: El nombre y apellido están concatenados en la columna desc_text. Usamos la información en la columna desc_id, que indican las 2 primeras letras del nombre y las 2 primeras letras del apellido.

 desc_text    |desc_id | Names
 -------------|--------|------------
 lisbethhallewell | LiHa	 | lisbeth hallewell
 mellielowde | MeLo	 | mellie lowde
 krispinmundie  | KrMu    |galen kayne
 galenkayne    |GaKa |   krispin mundie
  mellielowde   | MeLo  | maribel brecher
  natyeudall    |NaYe      | nat yeudall
 
- Tarjeta de crédito:	Concatenar columnas producto_1_number y bin_2 number, convertir el resultado de binario a decimal para obtener los primeros 6 dígitos de la TDC. Los 10 números restantes se obtienen de la columna tel_id.


| producto_1_number|bin_2_number |tel_id       |CreditCard          |
|-----------------:|:------------|:------------|:-------------------|
|        1000010001|0100111111   |45-0651 7589 |2721 8148 9697 2326 |
|        1000010011|0100110101   |48-9697 2326 |5224 9833 6970 6390 |
|        1000010011|0100110101   |17-1401 0250 |4180 7353 0770 1709 |
|        1100110000|100011001    |53-0770 1709 |2721 8117 1401 0250 |
|        1111111100|100000010    |33-6970 6390 |2711 6745 0651 7589 |
|        1000010110|1010100100   |10-4759 6597 |5474 9210 4759 6597 |


- Dirección:	Invertir dirección de la cadena de caracteres y separar números de letras, así como palabras mediante el uso de letras mayúsculas.

correo_id| Resultado
---------|---------
ecarreTevorglleB252 |252 Bellgrove Terrace
yellAokpohS315 | 513 Shopko Alley

- Fecha de nacimiento:	En el campo registro.xls, después de quitar las palabras "Version" y ".xls" encontramos el año_mes y después  en el campo clave_id corroboramos ambos datos y agregamos el día. Al final con el campo clave_id pasamos al formato yyyy-mm-dd. 


clave_id| registro.xls| Resultado
---------|------------|-------
 540417  |Version194302.xls |1954-04-17
771128|Version197711.xls |1977-11-28

- E-mail:	La parte identificadora del correo se conforma de la primera letra del nombre y el apellido. Para ocultar la información se añadieron caracteres al final en base 37 (0-9 y a-z). Para la parte del dominio combinamos con la columna apellido@_text en donde reemplazamos el caracter ! con '.com'. 

"nombre_text

nombre_text| apellid@_text| Resultado
---------|------------|-------
lhallewell3ub|discovery!  |lhallewell@discovery.com
mlowde5tb |163!  |mlowde@163.com

- Teléfono móvil:	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}.

clave_secundaria_text| Resultado
---------|---------
 +EBO AOl 99S 7769   |+56 823 794 8863
 +EBO AOl 99S 7769   |+56 823 794 8863

-Teléfono fijo:	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}.
clave_primaria_text| Resultado
---------|---------
 B6(A9A)E70-7A0B   |+56 823 794 8863
  B6(A9A)E70-7A0B  |86(494)370-7408 

- CURP:	Con el nombre y fecha de nacimiento calculados, más el campos agrupacion_id, en el que está el sexo y estado, utilizamos una función que calcula el CURP. *Sabemos que en los datos existe la columna CURP en la que están los cinco digitos asignados, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato.*

|desc_text        |desc_id |clave_id |registro.xls      |agrupacion_id |CURP |CURP_generado        |
|:----------------|:-------|:--------|:-----------------|:-------------|:------|:------------------|
|maribelbrecher   |MaBr    |761006   |Version197610.xls |HDF           |KJO13  |HAXL540417MDFLXS01 |
|lisbethhallewell |LiHa    |540417   |Version195404.xls |MDF           |DGV71  |LOXM771128MDFWXL08 |
|krispinmundie    |KrMu    |400829   |Version194008.xls |MDF           |PUR98  |KAXG480729HDFYXL07 |
|galenkayne       |GaKa    |480729   |Version194807.xls |HDF           |BTE45  |MUXK400829MDFNXR06 |
|mellielowde      |MeLo    |771128   |Version197711.xls |MDF           |ESM85  |BRXM761006HDFRXR03 |
|natyeudall       |NaYe    |960429   |Version199604.xls |HDF           |LIJ50  |YEXN960429HDFDX06  |

- INE:	Utilizando el curp que calculamos y el campo cvv_secreto en el que encontramos el número aleatorio de tres dígitos (relleno con ceros) calculamos la clave de elector. 

|desc_text        |desc_id |clave_id |registro.xls      |agrupacion_id |CURP_generado      | CVV_secreto|
|:----------------|:-------|:--------|:-----------------|:-------------|:------------------|-----------:|
|maribelbrecher   |MaBr    |761006   |Version197610.xls |HDF           |HAXL540417MDFLXS01 |         560|
|lisbethhallewell |LiHa    |540417   |Version195404.xls |MDF           |LOXM771128MDFWXL08 |         676|
|krispinmundie    |KrMu    |400829   |Version194008.xls |MDF           |KAXG480729HDFYXL07 |         808|
|galenkayne       |GaKa    |480729   |Version194807.xls |HDF           |MUXK400829MDFNXR06 |         373|
|mellielowde      |MeLo    |771128   |Version197711.xls |MDF           |BRXM761006HDFRXR03 |         906|
|natyeudall       |NaYe    |960429   |Version199604.xls |HDF           |YEXN960429HDFDX06  |         207|

- RFC:	Con el nombre y la fecha de nacimiento que obtuvimos utilizamos una función que calcula el RFC. *Sabemos que en la columna producto_id se encuentra la homoclave, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato.*

|desc_text        |desc_id |clave_id |registro.xls      |producto_id |RFC           |
|:----------------|:-------|:--------|:-----------------|:-----------|:-------------|
|maribelbrecher   |MaBr    |761006   |Version197610.xls |IO1         |HAXL540417I17 |
|lisbethhallewell |LiHa    |540417   |Version195404.xls |YY3         |LOXM771128Q67 |
|krispinmundie    |KrMu    |400829   |Version194008.xls |AS5         |KAXG480729ES8 |
|galenkayne       |GaKa    |480729   |Version194807.xls |LX4         |MUXK400829PK5 |
|mellielowde      |MeLo    |771128   |Version197711.xls |UZ1         |BRXM761006BR5 |
|natyeudall       |NaYe    |960429   |Version199604.xls |GP4         |YEXN960429ES3 |

- NSS:	Convertimos la columna NSS de octal a decimal.

|NSS_nuevo   |NSS_previo    |
|:-----------|:-------------|
|84805359957 |272573775210  |
|31150457917 |1167662614525 |
|26757289316 |461602433614  |
|41037739916 |307266752544  |
|25064110728 |350055442075  |
|43371167324 |503107677134  |

- Pasaporte:	Convertimos la columna pasaporte de hexadecimal a decimal. 

|Pasaporte_nuevo   |Pasaporte_previo |
|:-----------------|:----------------|
|53610393260829716 |CA15A2DBE83668   |
|94726758893539665 |BE765E5E94AC14   |
|86703408579733276 |DD7E9F3E8F057    |
|03896574516719703 |134084A6D35E71C  |
|56881734513866344 |150897C3E92D151  |
|78118704560401635 |115888C43A2ECE3  |

El cálculo del curp se hizo tomando como base https://github.com/epalomeque/py-curprfc
