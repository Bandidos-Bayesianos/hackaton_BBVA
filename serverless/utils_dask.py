import re
from calcule import CalculeRFC, CalculeCURP


def getNames(desc_text, desc_id):
    desc_id = re.sub(r'([a-z])+([A-Z])', r'\1|\2', desc_id).lower()
    pattern = r"("+desc_id+")"
    names = re.sub(pattern, r' \1', desc_text).strip()
    return names


def getAddress(correo_id):
    correo_id = str(correo_id)[::-1]
    address = re.sub(r'([A-Z])', r' \1', correo_id)
    return address


leetCodec = {"O": 0, "l": 1, "I": 1, "Z": 2, "E": 3, "A": 4, "S": 5, "B": 8}
estadosCodec = {
    '': '',
    'AS': 'AGUASCALIENTES',
    'BC': 'BAJA CALIFORNIA',
    'BS': 'BAJA CALIFORNIA SUR',
    'CC': 'CAMPECHE',
    'CS': 'CHIAPAS',
    'CH': 'CHIHUAHUA',
    'CL': 'COAHUILA',
    'CM': 'COLIMA',
    'DF': 'DISTRITO FEDERAL',
    'DG': 'DURANGO',
    'GT': 'GUANAJUATO',
    'GR': 'GUERRERO',
    'HG': 'HIDALGO',
    'JC': 'JALISCO',
    'MC': 'MEXICO',
    'MN': 'MICHOACAN',
    'MS': 'MORELOS',
    'NT': 'NAYARIT',
    'NL': 'NUEVO LEON',
    'OC': 'OAXACA',
    'PL': 'PUEBLA',
    'QT': 'QUERETARO',
    'QR': 'QUINTANA ROO',
    'SP': 'SAN LUIS POTOSI',
    'SL': 'SINALOA',
    'SR': 'SONORA',
    'TC': 'TABASCO',
    'TS': 'TAMAULIPAS',
    'TL': 'TLAXCALA',
    'VZ': 'VERACRUZ',
    'YN': 'YUCATÁN',
    'ZS': 'ZACATECAS',
    'NE': 'NACIDO EXTRANJERO',
}
estadosCodec2 = {
    '': '',
    'AS': '01',
    'BC': '02',
    'BS': '03',
    'CC': '04',
    'CS': '05',
    'CH': '06',
    'CL': '07',
    'CM': '08',
    'DF': '09',
    'DG': '10',
    'GT': '11',
    'GR': '12',
    'HG': '13',
    'JC': '14',
    'MC': '15',
    'MN': '16',
    'MS': '17',
    'NT': '18',
    'NL': '19',
    'OC': '20',
    'PL': '21',
    'QT': '22',
    'QR': '23',
    'SP': '24',
    'SL': '25',
    'SR': '26',
    'TC': '27',
    'TS': '28',
    'TL': '29',
    'VZ': '30',
    'YN': '31',
    'ZS': '32',
    'NE': '33',
}


def getPhone(clave_text):
    phone = ""
    for char in clave_text:
        if(char in leetCodec):
            phone += str(leetCodec[char])
        else:
            phone += str(char)
    return phone


def getUrl(apellidos):
    url = re.sub(r'(.)!(.)', r'\1com\2', re.sub(r'!.',
                                                '.com.', re.sub('!$', '.com',  apellidos)))
    if url and url != '':
        url = str("@")+str(url)
    return url


def getBirthday(registro, clave_id):
    yyyymm = registro[7:13]
    yyyymmdd = yyyymm[:4], yyyymm[4:], str(clave_id)[-2:]
    birthday = "-".join(yyyymmdd)
    return birthday


# def getOfficialBirthdayDate(date):
#    officialDate = date.split('-')
#    officialDate = ''.join(officialDate)[2:]
#    return officialDate

def getNSS(NSS):
    ssn = ""
    if(NSS and NSS != ''):
        ssn = str(int(str(NSS), 8)).rjust(11, '0')
    return ssn


def getPassport(pasaporte):
    passport = ""
    if(pasaporte and pasaporte != ''):
        passport = str(int(str(pasaporte), 16)).rjust(17, '0')
    return passport


def getCreditCard(producto_1, bin_2, tel_id):
    creditCardNumber = ""
    if producto_1 != "" and bin_2 != "":
        initial6 = int(str(producto_1)+str(bin_2), 2)
        last10 = "".join(re.split('-| ', tel_id))
        creditCardNumber = str(initial6)+str(last10)
        creditCardNumber = creditCardNumber[:4]+" "+creditCardNumber[4:8] + \
            " "+creditCardNumber[8:12]+" "+creditCardNumber[12:]
    return creditCardNumber

# def getRfc(codigo_banco, producto_id, date):
#    rfc = ""
#    officialDate = getOfficialBirthdayDate(date)
#    rfc = codigo_banco + \
#        str(officialDate) + str(producto_id)
#    return rfc


# def getCurp(codigo_banco, date, agrupacion_id, curp):
#    parsedCurp = ""
#    officialDate = getOfficialBirthdayDate(date)
#    parsedCurp = codigo_banco + \
#        str(officialDate) + str(agrupacion_id) + str(curp)
#    return parsedCurp


def getIne(curp, cvv_secreto, agrupacion_id):
    ine = ""
    ine = curp[0] + curp[13] + curp[2] + curp[14] + curp[3] + curp[15] + \
        curp[4:10] + estadosCodec2[agrupacion_id[1:]] + \
        curp[10] + str(cvv_secreto).rjust(3, "0")
    return ine


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


def getEmail(id_cliente, nombre_text, apellidos):
    return getUsername(id_cliente, nombre_text)+getUrl(apellidos)


def compute_everything(row):
    Names = getNames(row["desc_text"], row["desc_id"])
    Address = getAddress(row["correo_id"])
    Phone_1 = getPhone(row['clave_primaria_text'])
    Phone_2 = getPhone(row['clave_secundaria_text'])
    Email = getEmail(row["id_cliente"], row["nombre_text"],
                     row["apellid@_text"])
    Birthday = getBirthday(row['registro.xls'], row['clave_id'])
    # Curp = getCurp(row['desc_id'], Birthday, row['agrupacion_id'], row['CURP'])
    Curp = ""
    try:
        Curp = CalculeCURP(nombres=Names.split()[0], paterno=Names.split()[
            1], materno=None, fecha="-".join(Birthday.split("-")[::-1]), genero=row['agrupacion_id'][0], estado=estadosCodec[row["agrupacion_id"][1:]]).data
    except:
        None
    # Rfc = getRfc(row['desc_id'], row['producto_id'], Birthday)
    # print("-".join(Birthday.split("-")[::-1]))
    Rfc = ""
    try:
        Rfc = CalculeRFC(nombres=Names.split()[0], paterno=Names.split()[1], materno=None,
                         fecha="-".join(Birthday.split("-")[::-1])).data
    except:
        None
    Ine = ""
    try:
        Ine = getIne(Curp, row["CVV_secreto"], row["agrupacion_id"])
    except:
        None
    Nss = getNSS(row["NSS"])
    Passport = getPassport(row["pasaporte"])
    CreditCard = getCreditCard(
        row['producto_1_number'], row['bin_2_number'], row['tel_id'])
    return [Names, Address, Phone_1, Phone_2, Birthday, Email, Rfc, Curp, Ine, CreditCard, Nss, Passport]
