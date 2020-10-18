# Hackaton BBVA. Bandidos Bayesianos

Aquí se encuentra el código para reproducir el resultado al reto **Identificación de datos de fraude** que generamos durante nuestra participación en el **Hackatón BBVA 2020**. Los resultados del trabajo se resumen en:
- [Reporte de resultados](https://docs.google.com/spreadsheets/d/1NIxdvoID99uY4LsrdYndkxtQMfldG1TB/edit#gid=1957317044). 
- [Vídeo](https://youtu.be/4LMIdqE8Urc).
- [Dataset](https://s3.console.aws.amazon.com/s3/buckets/bbva-hack-2020/outputs/reconstructed_full.parquet/?region=us-east-2&tab=overview). Para el cual se debe ocupar el usuario **guest** con clave **guesthack** y account alias **201513274994**.

### Descripción del reto y approach
En dicho reto se nos compartió una base de datos con 3M de registros y el objetivo era encontrar las reglas de identificación de algunos campos que un ente malicioso había ocultado, con la finalidad de robar la información. Nuestra solución utiliza herramientas de cómputo distribuido que desarrollamos en un entorno local, utilizando un contenedor con todas las herramientas y frameworks necesarios para que la solución sea portable y escalable en un entorno de computación en la nube. En particular, decidimos usar Amazon Sagemaker, por lo que el contenedor lo subimos a Amazon Container Registry.

Lo primero que hicimos para generar esta solución fue en un prototipo rápido y escalable basado en funciones lambdas que de manera secuencial recorren el archivo y generan un csv con los datos procesados; esto tiene como ventaja que hacer uso de tecnologías como aws batch se vuelve más facil para procesamiento posterior. Una vez hecha y probada la solución sobre una muestra de los datos, pusimos el código de nuestra solución en un repositorio público y lo clonamos en Amazon SageMaker Studio. Desde ahí, pudimos invocar el trabajo generado mediante ScriptProcessor utilizando el conjunto entero de los datos, que previamente alojamos en Amazon S3. Los datos reconstruidos después de aplicar nuestra solución los almacenamos también en Amazon S3 y los descargamos para inspeccionar. 

A continuación se describen las reglas generadas para encontrar campos, así como algunos ejemplos ilustrativos.  

- **Nombre:** El nombre y apellido están concatenados en la columna desc_text. Usamos la información en la columna desc_id, que indican las 2 primeras letras del nombre y las 2 primeras letras del apellido.

|desc_text        |desc_id |Names             |
|:----------------|:-------|:-----------------|
|galenkayne       |GaKa    |galen kayne       |
|krispinmundie    |KrMu    |krispin mundie    |
|lisbethhallewell |LiHa    |lisbeth hallewell |
|maribelbrecher   |MaBr    |maribel brecher   |
|mellielowde      |MeLo    |mellie lowde      |
|natyeudall       |NaYe    |nat yeudall       |
 
- **Tarjeta de crédito:**	Concatenar columnas producto_1_number y bin_2 number, convertir el resultado de binario a decimal para obtener los primeros 6 dígitos de la TDC. Los 10 números restantes se obtienen de la columna tel_id.

| producto_1_number|bin_2_number |tel_id       |CreditCard          |
|-----------------:|:------------|:------------|:-------------------|
|        1100110000|100011001    |53-0770 1709 |4180 7353 0770 1709 |
|        1000010011|0100110101   |17-1401 0250 |2721 8117 1401 0250 |
|        1000010011|0100110101   |48-9697 2326 |2721 8148 9697 2326 |
|        1000010001|0100111111   |45-0651 7589 |2711 6745 0651 7589 |
|        1111111100|100000010    |33-6970 6390 |5224 9833 6970 6390 |
|        1000010110|1010100100   |10-4759 6597 |5474 9210 4759 6597 |


- **Dirección:**	Invertir dirección de la cadena de caracteres y separar números de letras, así como palabras mediante el uso de letras mayúsculas.

|correo_id           |Address               |
|:-------------------|:---------------------|
|lliHssorCgnirahC97  |79 Charing Cross Hill |
|enaLuaedaB1         |1 Badeau Lane         |
|ecarreTevorglleB252 |252 Bellgrove Terrace |
|evirDenotsdleiF76   |67 Fieldstone Drive   |
|yellAokpohS315      |513 Shopko Alley      |
|noitcnuJtsaE4247    |7424 East Junction    |

- **Fecha de nacimiento:**	En el campo registro.xls, después de quitar las palabras "Version" y ".xls" encontramos el año_mes y después  en el campo clave_id corroboramos ambos datos y agregamos el día. Al final con el campo clave_id pasamos al formato yyyy-mm-dd. 

|clave_id |registro.xls      |Birthday   |
|:--------|:-----------------|:----------|
|480729   |Version194807.xls |1948-07-29 |
|400829   |Version194008.xls |1940-08-29 |
|540417   |Version195404.xls |1954-04-17 |
|761006   |Version197610.xls |1976-10-06 |
|771128   |Version197711.xls |1977-11-28 |
|960429   |Version199604.xls |1996-04-29 |

- **E-mail:**	La parte identificadora del correo se conforma de la primera letra del nombre y el apellido. Para ocultar la información se añadieron caracteres al final en base 37 (0-9 y a-z). Para la parte del dominio combinamos con la columna apellido@_text en donde reemplazamos el caracter ! con '.com'. 

|nombre_text   |apellid@_text |Email                    |
|:-------------|:-------------|:------------------------|
|gkayne52e     |ifeng!        |gkayne@ifeng.com         |
|kmundie4i8    |yolasite!     |kmundie@yolasite.com     |
|lhallewell3ub |discovery!    |lhallewell@discovery.com |
|mbrecherqe    |marketwatch!  |mbrecher@marketwatch.com |
|mlowde5tb     |163!          |mlowde@163.com           |
|nyeudall7bu   |artisteer!    |nyeudall@artisteer.com   |

- **Teléfono móvil:**	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}.

|clave_secundaria_text |CellPhone         |
|:---------------------|:-----------------|
|+SB ZZO B6l AZZ9      |+58 220 861 4229  |
|+ESl E99 B97 lESB     |+351 399 897 1358 |
|+EBO AOl 99S 7769     |+380 401 995 7769 |
|+6E l66 BSO 977B      |+63 166 850 9778  |
|+EE 6A7 ESS AZEA      |+33 647 355 4234  |
|+EBO 66E Zll lSBB     |+380 663 211 1588 |

- **Teléfono fijo:**	Convertir letras a números basados en LEET. Diccionario {'O':0,'I':1,'Z':2,'E':3,'A':4,'S':5,'B':8}.

|clave_primaria_text |Phone            |
|:-------------------|:----------------|
|A6(7SZ)1E9-AE19     |46(752)139-4319  |
|6E(EBA)1E6-9Z97     |63(384)136-9297  |
|ES1(16S)AA0-0ABA    |351(165)440-0484 |
|B6(7Z9)AB1-Z607     |86(729)481-2607  |
|B6(A9A)E70-7A0B     |86(494)370-7408  |
|6E(ZEB)ES9-6E79     |63(238)359-6379  |

- **CURP:**	Con el nombre y fecha de nacimiento calculados, más el campos agrupacion_id, en el que está el sexo y estado, utilizamos una función que calcula el CURP. **Sabemos que en los datos existe la columna CURP en la que están los cinco digitos asignados, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato.**

|desc_text        |desc_id |clave_id |registro.xls      |agrupacion_id |CURP.y |CURP.x             |
|:----------------|:-------|:--------|:-----------------|:-------------|:------|:------------------|
|galenkayne       |GaKa    |480729   |Version194807.xls |HDF           |BTE45  |KAXG480729HDFYXL07 |
|krispinmundie    |KrMu    |400829   |Version194008.xls |MDF           |PUR98  |MUXK400829MDFNXR06 |
|lisbethhallewell |LiHa    |540417   |Version195404.xls |MDF           |DGV71  |HAXL540417MDFLXS01 |
|maribelbrecher   |MaBr    |761006   |Version197610.xls |HDF           |KJO13  |BRXM761006HDFRXR03 |
|mellielowde      |MeLo    |771128   |Version197711.xls |MDF           |ESM85  |LOXM771128MDFWXL08 |
|natyeudall       |NaYe    |960429   |Version199604.xls |HDF           |LIJ50  |YEXN960429HDFDX06 

- **INE:**	Utilizando el curp que calculamos y el campo cvv_secreto en el que encontramos el número aleatorio de tres dígitos (relleno con ceros) calculamos la clave de elector. 

|desc_text        |desc_id |clave_id |registro.xls      |agrupacion_id |CURP_generado      | CVV_secreto|
|:----------------|:-------|:--------|:-----------------|:-------------|:------------------|-----------:|
|galenkayne       |GaKa    |480729   |Version194807.xls |HDF           |KAXG480729HDFYXL07 |         373|
|krispinmundie    |KrMu    |400829   |Version194008.xls |MDF           |MUXK400829MDFNXR06 |         808|
|lisbethhallewell |LiHa    |540417   |Version195404.xls |MDF           |HAXL540417MDFLXS01 |         676|
|maribelbrecher   |MaBr    |761006   |Version197610.xls |HDF           |BRXM761006HDFRXR03 |         560|
|mellielowde      |MeLo    |771128   |Version197711.xls |MDF           |LOXM771128MDFWXL08 |         906|
|natyeudall       |NaYe    |960429   |Version199604.xls |HDF           |YEXN960429HDFDX06  |         207|

- **RFC:**	Con el nombre y la fecha de nacimiento que obtuvimos utilizamos una función que calcula el RFC. **Sabemos que en la columna producto_id se encuentra la homoclave, pero decidimos no utilizar esta información dentro de nuestra respuesta pues consideramos más acertado hacerlo siguiendo las reglas estipuladas para calcular este dato.**

|desc_text        |desc_id |clave_id |registro.xls      |producto_id |RFC           |
|:----------------|:-------|:--------|:-----------------|:-----------|:-------------|
|galenkayne       |GaKa    |480729   |Version194807.xls |LX4         |KAXG480729ES8 |
|krispinmundie    |KrMu    |400829   |Version194008.xls |AS5         |MUXK400829PK5 |
|lisbethhallewell |LiHa    |540417   |Version195404.xls |YY3         |HAXL540417I17 |
|maribelbrecher   |MaBr    |761006   |Version197610.xls |IO1         |BRXM761006BR5 |
|mellielowde      |MeLo    |771128   |Version197711.xls |UZ1         |LOXM771128Q67 |
|natyeudall       |NaYe    |960429   |Version199604.xls |GP4         |YEXN960429ES3 |

- **NSS:**	Convertimos la columna NSS de octal a decimal.

|NSS_nuevo   |NSS_previo    |
|:-----------|:-------------|
|26757289316 |307266752544  |
|41037739916 |461602433614  |
|84805359957 |1167662614525 |
|25064110728 |272573775210  |
|31150457917 |350055442075  |
|43371167324 |503107677134  |

- **Pasaporte:**	Convertimos la columna pasaporte de hexadecimal a decimal. 

|Pasaporte_nuevo   |Pasaporte_previo |
|:-----------------|:----------------|
|86703408579733276 |134084A6D35E71C  |
|03896574516719703 |DD7E9F3E8F057    |
|53610393260829716 |BE765E5E94AC14   |
|56881734513866344 |CA15A2DBE83668   |
|94726758893539665 |150897C3E92D151  |
|78118704560401635 |115888C43A2ECE3  |

Nota: Para el cálculo del curp se hizo tomando como base https://github.com/epalomeque/py-curprfc



