class AwsEmrStep:
    def __init__(self, step_name, arguments: []):
        self.step_name = step_name
        self.arguments = arguments

    def get_step(self):
        return {
            'Name': self.step_name,
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': self.arguments
            }
        }
