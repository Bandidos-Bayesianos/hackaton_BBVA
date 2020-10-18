from pyspark.sql import SparkSession
from udfs import getNames, getAddress, getPhone, getBirthday, getNSS, getPassport, getCreditCard, getEmail
from udfs import getCURP, getRFC, getINE
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--npartitions', action="store", type=int, default=10)
args = parser.parse_args()

inputPath = 'opt/ml/processing/input_data/sample_10K.parquet'
outputPath = 'opt/ml/processing/processed_data/reconstructed.parquet'

if __name__ == "__main__":
    
    spark = SparkSession.builder.master("local[*]").appName("ReconstructAPP").getOrCreate()

    start_time = time.time()
    
    df_first = spark.read.parquet(inputPath).repartition(args.npartitions)
    
    df_first = df_first \
        .withColumn('producto_1_number', df_first['producto_1_number'].cast("int")) \
        .withColumn('bin_2_number', df_first['bin_2_number'].cast("int"))
    
    df_second = df_first \
        .select(getNames('desc_text', 'desc_id').alias('Names'),
        getAddress('correo_id').alias('Address'),
        getPhone('clave_primaria_text').alias('Phone'),
        getPhone('clave_secundaria_text').alias('CellPhone'),
        getBirthday("`registro.xls`",'clave_id').alias('Birthday'),
        getEmail('id_cliente', 'nombre_text', 'apellid@_text').alias('Email'),
        getNSS('NSS').alias('NSS'),
        getPassport('pasaporte').alias('Passport'),
        getCreditCard('producto_1_number','bin_2_number','tel_id').alias('CreditCard'),
        'agrupacion_id','CVV_secreto')

    df_third = df_second \
         .withColumn("CURP", getCURP('Names', 'Birthday', 'agrupacion_id')) \
         .withColumn("RFC", getRFC('Names', 'Birthday', 'agrupacion_id')) \
         .withColumn("INE", getINE('CURP', 'CVV_secreto', 'agrupacion_id')) \
         .drop('agrupacion_id','CVV_secreto')
    
    df_third.printSchema()
    
    df_third.show(100,False)
    df_third.write.mode('overwrite').parquet(outputPath)
    print('SUCCESS!')
    print("--- %s seconds ---" % (time.time() - start_time))
    