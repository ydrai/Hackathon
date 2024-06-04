from boto3.session import Session
import streamlit as st
import uuid
import json

class AWSClient:
    """
    A class to create and manage AWS service clients using boto3, with the capability to interact with different services
    based on initialization parameters.
    
    Attributes:
        config (dict): Dictionary containing AWS credentials and configuration.
        service_name (str): The name of the AWS service for which the client is created.
        client: The boto3 client object for the specified AWS service.
        session_id (str): A unique identifier for the session, used for services like Amazon Lex.
    """

    def __init__(self, service_name='lexv2-runtime', session_id=None):
        """
        Initializes the AWSClient with specific service details and credentials loaded from streamlit secrets.
        
        Args:
            service_name (str): Specifies the AWS service for which the client will be created (default is 'lexv2-runtime').
            session_id (str, optional): A unique identifier for interactions with services that require session management.
                                       If not provided, a new UUID will be generated.
        """
        self.config = {
            'aws_access_key_id': st.secrets["aws_credentials"]["aws_access_key_id"],
            'aws_secret_access_key': st.secrets["aws_credentials"]["aws_secret_access_key"],
            'region_name': st.secrets["aws_credentials"]["region_name"]
        }
        self.service_name = service_name
        self.client = self.create_client(service_name)
        self.session_id = session_id if session_id else str(uuid.uuid4())

    def create_client(self, service_name):
        """
        Creates a boto3 client for the specified AWS service.
        
        Args:
            service_name (str): The name of the service for which the client should be created.
        
        Returns:
            A boto3 service client object configured for the specified service.
        """
        session = Session(
            aws_access_key_id=self.config['aws_access_key_id'],
            aws_secret_access_key=self.config['aws_secret_access_key'],
            region_name=self.config['region_name'],
        )
        return session.client(service_name)

    def send_lex_message(self, text):
        """
        Sends a message to the Amazon Lex service and returns the response.
        
        Args:
            text (str): The text message to send to the Amazon Lex bot.
        
        Returns:
            str: The content of the message returned by Amazon Lex.
        
        Raises:
            ValueError: If the service name is not 'lexv2-runtime'.
        """
        if self.service_name != 'lexv2-runtime':
            raise ValueError("This method is only valid for Lex service.")
        response = self.client.recognize_text(
            botId=st.secrets.aws_credentials["bot_id"],
            botAliasId=st.secrets.aws_credentials["bot_alias_id"],
            localeId=st.secrets.aws_credentials["locale_id"],
            sessionId=self.session_id,
            text=text
        )
        return response['messages'][0]['content']

    def invoke_lambda(self, function_name, payload):
        """
        Invokes an AWS Lambda function with the specified function name and payload.
        
        Args:
            function_name (str): The name of the Lambda function to invoke.
            payload (str): The JSON payload string to send to the Lambda function.
        
        Returns:
            bytes: The raw payload response from the Lambda function.
        
        Raises:
            ValueError: If the service name is not 'lambda'.
        """
        if self.service_name != 'lambda':
            raise ValueError("This method is only valid for Lambda service.")
        response = self.client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=payload
        )
        response_payload = response['Payload'].read()
        return response_payload.decode()
    
    def start_step_function_execution(self, state_machine_arn, input_data):
        """
        Starts an execution of the specified Step Functions state machine.
        
        Args:
            state_machine_arn (str): The ARN of the Step Functions state machine to start.
            input_data (dict): The input data for the state machine execution.
        
        Returns:
            dict: The response from the StartExecution API call.
        
        Raises:
            ValueError: If the service name is not 'stepfunctions'.
        """
        if self.service_name != 'stepfunctions':
            raise ValueError("This method is only valid for Step Functions service.")
        response = self.client.start_execution(
            stateMachineArn=st.secrets.aws_credentials["state_machine_arn"],
            # state_machine_arn,
            input=json.dumps(input_data)
        )
        return response

def create_client():
    """
    Creates and stores an AWSClient instance in the session state if it doesn't already exist.
    This function ensures that a client instance is available throughout the app's session.
    """
    if 'client' not in st.session_state:
        st.session_state['client'] = AWSClient()
    
def send_lex_message(message):
    try:
        bot_response = st.session_state.client.send_lex_message(message)
        hebrew_question = st.session_state.hebrew_questions.get(bot_response, bot_response)
        return hebrew_question
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Bot finished"

def invoke_lambda(function_name, payload):
    """
    Invokes an AWS Lambda function with the specified function name and payload.
    """
    try:
        lambda_response = st.session_state.client.invoke_lambda(function_name, payload)
        return lambda_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Lambda invocation failed"
