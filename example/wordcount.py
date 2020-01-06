from pyspark.sql import SparkSession


def run_word_count(spark, hadoop_conf):
    input_bucket = hadoop_conf.get('wordcount.input_bucket')
    output_bucket = hadoop_conf.get('wordcount.output_bucket')
    key_path = hadoop_conf.get('wordcount.key_path')

    filetxt_rdd = extract(spark, input_bucket, key_path)
    words = filetxt_rdd.flatMap(lambda line: line.split(" "))
    wordcount = words.map(lambda word: (word, 1))\
        .reduceByKey(lambda a, b: a + b)
    load(wordcount, output_bucket)


def load(wordcount, output_bucket):
    dataframe = wordcount.toDF()
    dataframe.write\
             .mode("overwrite")\
             .csv('s3a://{output_bucket}/output/wordcount.csv'
                  .format(output_bucket=output_bucket))


def extract(spark, input_bucket, key_path):
    path = 's3a://{bucket}/{key_path}'\
                .format(bucket=input_bucket,
                        key_path=key_path)
    rdd = spark.sparkContext.textFile(path)
    return rdd


if __name__ == "__main__":
    with SparkSession.builder\
            .appName("WordCount - Example").getOrCreate() as spark:
        sc = spark.sparkContext
        hadoopConf = sc._jsc.hadoopConfiguration()
        hadoopConf.set("com.amazonaws.services.s3.enableV4", "true")
        run_word_count(spark, hadoopConf)
