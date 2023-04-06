from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.rdd import RDD
from pyspark.sql import SQLContext, HiveContext, Row
from preCompile.mix_pyspark import UDF, showAlias, saveDFToCsv, spark, sqlContext, sc, show
from preCompile.linkis_python import handler_stop_signals, show_matplotlib, printlog, PythonContext, setup_plt_show

conf = SparkConf()
conf.setMaster("local").setAppName("Editor Local Example")
sc = SparkContext(conf=conf)

sqlContext = HiveContext(sc)
spark = SparkSession(sc)