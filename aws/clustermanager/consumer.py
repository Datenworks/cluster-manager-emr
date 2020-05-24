import base64
import json


class EmrInputParser:
    def __init__(self, event_input):
        self.prefix = 'spark.hadoop.'
        self.name = ''
        self.resource = ''
        self.arguments = []
        self.pyfiles = []
        self.subnet = ''
        self.master_type = ''
        self.core_type = ''
        self.count = ''
        self.release = ''
        self.region = ''
        self.log_bucket = ''
        self.entrypoint = ''
        self.mem_executor = ''
        self.mem_driver = ''
        self.spark_packages = []
        self.jar_files = []
        self.bootstrap_steps = []
        self.multiple_steps = ''
        self.parse_input(self.decode_input(event_input))

    def decode_input(self, event_input):
        event_input = base64.b64decode(event_input)
        return json.loads(event_input.decode('utf-8'))

    def parse_input(self, decoded_input):
        self.name = decoded_input['name']
        self.resource = decoded_input['resource']
        self.arguments = self.__parse_arguments(decoded_input['arguments'])
        self.pyfiles = self.__parse_pyfiles(decoded_input['pyfiles'])
        self.subnet = decoded_input['subnet']
        self.master_type = decoded_input['master_type']
        self.core_type = decoded_input['core_type']
        self.count = decoded_input['count']
        self.release = decoded_input['release']
        self.region = decoded_input['region']
        self.log_bucket = decoded_input['log_bucket']
        self.entrypoint = decoded_input['entrypoint']
        self.mem_executor = decoded_input['mem_executor']
        self.mem_driver = decoded_input['mem_driver']
        self.spark_packages = \
            self.__parse_spark_packages(decoded_input['spark_packages'])
        self.jar_files = \
            self.__parse_jar_files(decoded_input['jar_files'])
        self.multiple_steps = decoded_input['multiple_steps']
        self.bootstrap_steps = \
            self.__parse_bootstrap_steps(decoded_input['bootstrap_steps'])

    def __parse_pyfiles(self, pyfiles):
        if pyfiles != "":
            return ['--py-files', pyfiles]
        return []

    def __parse_bootstrap_steps(self, bootstrap_steps):
        bootstrap = []
        if isinstance(bootstrap_steps, list) and bootstrap_steps != []:
            for bootstrap_step in bootstrap_steps:
                bootstrap.append(bootstrap_step.get("arguments"))
        return bootstrap

    def __parse_jar_files(self, jar_files: list):
        if isinstance(jar_files, list) and jar_files != []:
            jars = ['--jars']
            jars.append(" ".join(jar_files))
            return jars
        return []

    def __parse_spark_packages(self, spark_packages: list):
        if isinstance(spark_packages, list) and spark_packages != []:
            packages = ['--packages']
            packages.append(",".join(spark_packages))
            return packages
        return []

    def __parse_arguments(self, arguments: list):
        arg = []
        for custom_argument in arguments:
            arg.append(custom_argument['Key'])
            arg.append(f"{self.prefix}{custom_argument['Value']}")
        return arg
