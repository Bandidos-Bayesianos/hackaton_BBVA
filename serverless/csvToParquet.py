import pyarrow.csv as pv
import pyarrow.parquet as pq
import s3fs

# fs = s3fs.S3FileSystem()
# bucket = "bbva-hack-2020"
# path = "denue.tsv"

# Python 3.6 or later
# p_dataset = pq.ParquetDataset(
#     f"s3://{bucket}/{path}",
#     filesystem=fs
# )

filename = "t_mdco_tfra400_Base3M_1.0.csv"
newFileName = filename.replace('csv', 'parquet')
opts = pv.ParseOptions(delimiter=',')
table = pv.read_csv(filename, None, parse_options=opts)
pq.write_table(table, newFileName)

schema = pq.read_schema(newFileName)
print("schema: {}".format(schema))
print("\n\n")
metadata = pq.ParquetFile(newFileName).metadata
print("metadata: {}".format(metadata))
pfile = pq.read_table(newFileName)
print("Column names: {}".format(pfile.column_names))
print("Schema: {}".format(pfile.schema))
