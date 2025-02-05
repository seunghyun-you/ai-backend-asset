import boto3

ssm = boto3.client('ssm')

def get_admin_user_information(parameter_path):
    parameters = {}

    response = ssm.get_parameters_by_path(
        Path=parameter_path,
        Recursive=True,
        WithDecryption=True
    )

    for param in response['Parameters']:
        key = param['Name'].split('/')[-1]
        parameters[key] = param['Value']

    return parameters

def get_parameter_store_value(parameter_name):
    try:
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        print(f"Error occurred while querying the parameter: {parameter_name}")
    except Exception as e:
        print(f"Unexpected result: {str(e)}")

# user_parameters = get_parameter_store_value('/SECRET_KEY')
# print(user_parameters)