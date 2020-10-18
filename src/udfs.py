from pyspark.sql.functions import udf
from calcule import CalculeCURP, CalculeRFC
import re

leetCodec = {"O": 0, "l": 1, "I": 1, "Z": 2, "E": 3, "A": 4, "S": 5, "B": 8}

@udf
def getNames(desc_text, desc_id):
    try: 
        desc_id = re.sub(r'([a-z])+([A-Z])', r'\1|\2', desc_id).lower()
        pattern = r"("+desc_id+")"
        names = re.sub(pattern, r' \1', desc_text)
        return names
    except:
        return None 
    
@udf
def getAddress(correo_id):
    try:
        correo_id = str(correo_id)[::-1]
        address = re.sub(r'([A-Z])', r' \1', correo_id)
        return address
    except:
        return None

@udf
def getPhone(clave_text):
    try:
        phone = ""
        for char in clave_text:
            if(char in leetCodec):
                phone += str(leetCodec[char])
            else:
                phone += str(char)
        return phone
    except:
        return None
    
@udf
def getBirthday(registro,clave_id):
    try:
        yyyymm = re.findall("\d+", registro)[0] 
        yyyymmdd = yyyymm[:4], yyyymm[4:], str(clave_id)[-2:]
        birthday = "-".join(yyyymmdd)
        return birthday
    except:
        None

@udf
def getNSS(NSS):
    try:
        ssn = ""
        if(NSS and NSS != ''):
            ssn = str(int(str(NSS), 8)).rjust(11, '0')
        return ssn
    except:
        None

@udf
def getPassport(pasaporte):
    try: 
        passport = ""
        if(pasaporte and pasaporte != ''):
            passport = str(int(str(pasaporte), 16)).rjust(17, '0')
        return passport
    except:
        None

@udf
def getCreditCard(producto_1, bin_2, tel_id):
    creditCardNumber = ""
    try:
        if producto_1 != "" and bin_2 != "":
            initial6 = int(str(producto_1)+str(bin_2), 2)
            last10 = "".join(re.split('-| ', tel_id))
            creditCardNumber = str(initial6)+str(last10)
            creditCardNumber = creditCardNumber[:4]+" "+creditCardNumber[4:8] + \
            " "+creditCardNumber[8:12]+" "+creditCardNumber[12:]
        return creditCardNumber
    except:
        return None

@udf
def getEmail(id_cliente, nombre_text, apellidos):
    
    def int_digits(value, digits):
        base = len(digits)
        result = []
        while value:
            value, r = divmod(value, base)
            result.append(digits[r])
        return ''.join(reversed(result))

    def getUsername(id_cliente, nombre_text):
        username = ""
        basura = int_digits(
        int(id_cliente), '0123456789abcdefghijklmnopqrstuvwxyz')
        username = nombre_text[:-len(basura)]
        return username

    def getUrl(apellidos):
        url = re.sub(r'(.)!(.)', r'\1com\2', re.sub(r'!.','.com.', re.sub('!$', '.com', apellidos)))
        if url and url != '':
            url = str("@")+str(url)
        return url
    
    try:
        Email = getUsername(id_cliente, nombre_text)+getUrl(apellidos)
        return Email
    except:
        return None
    
@udf
def getCURP(Names, Birthday, agrupacion_id):
    '''curp = CalculeCURP(nombres='Pablo',
            paterno='Campos',
            materno=None,
            fecha='10-04-1989',
            genero='H',
            estado='DISTRITO FEDERAL').data
    '''
    try:
        curp = CalculeCURP(nombres=Names.split()[0], 
                paterno=Names.split()[1], 
                materno=None, 
                fecha="-".join(Birthday.split("-")[::-1]), 
                genero=agrupacion_id[0], 
                estado='DISTRITO FEDERAL').data
        return curp
    except:
        return None
    
@udf
def getRFC(Names, Birthday, agrupacion_id):
    '''curp = CalculeRFC(nombres='Pablo',
            paterno='Campos',
            materno=None,
            fecha='10-04-1989',
            genero='H',
            estado='DISTRITO FEDERAL').data
    '''
    try:
        rfc = CalculeRFC(nombres=Names.split()[0], 
                paterno=Names.split()[1], 
                materno=None, 
                fecha="-".join(Birthday.split("-")[::-1]), 
                genero=agrupacion_id[0], 
                estado='DISTRITO FEDERAL').data
        return rfc
    except:
        return None

@udf
def getINE(curp, cvv_secreto, agrupacion_id):
    ine = ""
    try:
        ine = curp[0] + curp[13] + curp[2] + curp[14] + curp[3] + curp[15] + \
            curp[4:10] + '09' + \
            curp[10] + str(cvv_secreto).rjust(3, "0")
        return ine
    except:
        return None