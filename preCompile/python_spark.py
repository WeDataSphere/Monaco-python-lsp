from pylsp.mix_pyspark import SparkConf, SparkContext, SparkSession, HiveContext
from pylsp.mix_pyspark import RDD, SQLContext, Row, show

conf = SparkConf()
conf.setMaster("local").setAppName("Editor Local Example")
sc = SparkContext(conf=conf)

sqlContext = HiveContext(sc)
spark = SparkSession(sc)