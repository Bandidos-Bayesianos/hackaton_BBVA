import csv
import time
import re
from utils_dask import compute_everything

frecuencias = {}

# # passaporte

# leetCodec = {"O": 0, "l": 1, "I": 1, "Z": 2, "E": 3, "A": 4, "S": 5, "B": 8}


# def hexToDec(value):
#     x = int(value, 16)
#     return x

# # correo_id


# def reverseSeparateCamelCase(value):
#     str1 = str(value)[::-1]
#     str2 = re.sub(r'([A-Z])', r' \1', str1)
#     return str2

# # stats


# def addToFrequency(value):
#     if(value in frecuencias):
#         frecuencias[value] += 1
#     else:
#         frecuencias[value] = 1
#     pass

# # desc_text con desc_id


# def splitNameWithInitials(value, initials):
#     str1 = re.sub(r'([a-z])+([A-Z])', r'\1|\2', initials).lower()
#     regex = r"("+str1+")"
#     str2 = re.sub(regex, r' \1', value)
#     return str2


# def iterateString(value):
#     for char in value:
#         addToFrequency(char)

# # clave secundaria text clave primaria text


# def leet(value):
#     str1 = ""
#     for char in value:
#         if(char in leetCodec):
#             str1 += str(leetCodec[char])
#         else:
#             str1 += str(char)
#     return str1


# def replaceCom(value):
#     res = re.sub('!$', '.com', re.sub('.!.', 'com', value))
#     return res


# def contenido(largo, corto):
#     x = 0
#     for char in corto:
#         if char in largo:
#             x += 1
#     addToFrequency(x)


def decodeCCC(value, key):
    str1 = ""
    str2 = ""
    dic = []
    for char in key:
        dic.append(ord(char))

    for char in value:
        # print(dic)
        a = [abs(x - ord(char)) for x in dic]
        # print(a)
        minA = min(a)
        # print(minA)
        str2 += str(minA)
    return str2


def parseCsv():
    start = time.time()
    with open('results.csv', 'w') as test_file:
        file_writer = csv.writer(test_file)
        with open('moriarty.csv', newline='') as csvfile:

            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            reader = csv.DictReader(csvfile)
            count = 0
            for x in range(100):
                row = next(reader)
                file_writer.writerow(compute_everything(row))
                # print(row["id_cliente"], row["nombre_text"],
                #       row["apellid@_text"], getEmail(row["id_cliente"], row["nombre_text"],
                #                                      row["apellid@_text"]))

    end = time.time()
    print(end-start)
    pass


parseCsv()

# print(str(count))

# s3_object = s3client.Object(
#     Bucket='bbva-hack-2020',
#     Key='moriarty.csv'
#     #Key='6147553971.jpg'
# )
# botocoreStreamBody=s3_object['Body']
# botocoreStreamBody=s3_object.get(Range=f'bytes={1024}-')
# lines=[]
# lines=botocoreStreamBody.iter_lines(chunk_size=1024)
# body=[]
# for x in range(100):
#     row=next(lines)
#     body.append(row.decode("utf-8").split(","))
