import boto3
import logging
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime
from botocore.exceptions import ClientError

from models.chat_requests import ChatRequest
from models.chat_history_model import ChatRoom, ChatRoomList, Message


CHAT_ROOM_LIST_TABLE_STRUCTURE = {
    'KeySchema': [
        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
        {'AttributeName': 'chat_room_id', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'user_id', 'AttributeType': 'S'},
        {'AttributeName': 'chat_room_id', 'AttributeType': 'S'},
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': 'ChatRoomIdIndex',
            'KeySchema': [
                {'AttributeName': 'chat_room_id', 'KeyType': 'HASH'}
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'IndexName': 'UserChatRoomIdIndex',
            'KeySchema': [
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}
CHAT_ROOM_TABLE = {
    'KeySchema': [
        {'AttributeName': 'chat_room_id', 'KeyType': 'HASH'},
        {'AttributeName': 'message_id', 'KeyType': 'RANGE'},
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'chat_room_id', 'AttributeType': 'S'},
        {'AttributeName': 'message_id', 'AttributeType': 'N'},
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 200,
        'WriteCapacityUnits': 100
    }
}

class ChatHistoryRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dynamodb_resource = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')
        self.chat_room_list_table = self.create_or_get_table('ChatRoomListTable')
        self.chat_room_table = self.create_or_get_table('ChatRoomTable')


    def create_or_get_table(self, table_name: str):
        if self.check_table_exists(table_name):
            self.logger.info(f"Table '{table_name}' already exists.")
            return self.dynamodb_resource.Table(table_name)

        table_structure = (
            CHAT_ROOM_LIST_TABLE_STRUCTURE 
            if table_name == "ChatRoomListTable" 
            else CHAT_ROOM_TABLE
        )
        table_structure['TableName'] = table_name

        try:
            table = self.dynamodb_resource.create_table(**table_structure)
            table.wait_until_exists()
            self.logger.info(f"Table '{table_name}' created successfully.")
            
            self.add_tags_to_table(table_name, {"Owner": "sh1517"})
            return table
        except ClientError as e:
            self.logger.error(f"Error creating table {table_name}: {str(e)}")
            return None


    def check_table_exists(self, table_name: str) -> bool:
        try:
            self.dynamodb_resource.Table(table_name).load()
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.logger.warning(f"Table '{table_name}' does not exist. Creating table...")
                return False
            else:
                self.logger.error(f"Unexpected error checking table existence: {e}")
                return False


    def add_tags_to_table(self, table_name: str, tags: dict):
        try:
            # 태그를 추가하는 API 호출
            self.dynamodb_client.tag_resource(
                ResourceArn=self.dynamodb_resource.Table(table_name).table_arn,
                Tags=[{'Key': key, 'Value': value} for key, value in tags.items()]
            )
            self.logger.info(f"Tags added to table '{table_name}': {tags}")
        except ClientError as e:
            self.logger.error(f"Error adding tags to table {table_name}: {str(e)}")


    def make_message(self, role: str, message: str):
        return Message(
            role=role,
            content=message,
            timestamp=datetime.now().isoformat() 
        )

    
    def save_user_message(self, chat_requests: ChatRequest):
        new_message = self.make_message('user', chat_requests.message)
        try:
            chat_room = ChatRoom(
                chat_room_id=chat_requests.chat_room_id,
                message_id=chat_requests.message_id,
                messages=[new_message],
            )
            self.chat_room_table.put_item(Item=chat_room.dict())
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")

    
    def save_ai_message(self, chat_requests: ChatRequest, ai_message: str):
        new_message = self.make_message('ai', ai_message)
        pre_messages = self.get_chat_message(chat_requests)

        try:
            updated_messages = pre_messages['messages'] + [new_message.dict()]
            self.chat_room_table.update_item(
                Key={
                    'chat_room_id': chat_requests.chat_room_id,
                    'message_id': chat_requests.message_id
                },
                UpdateExpression="SET messages = :chat_messages",
                ExpressionAttributeValues={':chat_messages': updated_messages}
            )
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")


    def get_chat_message(self, chat_requests: ChatRequest):
        try:
            response = self.chat_room_table.get_item(
                Key={
                    'chat_room_id': chat_requests.chat_room_id,
                    'message_id': chat_requests.message_id
                }
            )
            return response.get('Item')
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")
            return None


    def check_chat_room_exists(self, chat_requests: ChatRequest):
        try:
            response = self.chat_room_list_table.query(
                KeyConditionExpression=Key('user_id').eq(chat_requests.user_id) & 
                                       Key('chat_room_id').eq(chat_requests.chat_room_id)
            )

            if response.get('Items'):
                return True
            return False
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")
            return None


    def add_chat_room_list(self, chat_requests: ChatRequest, chat_room_title: str):
        try:
            chat_room_list = ChatRoomList(
                user_id=chat_requests.user_id,
                chat_room_id=chat_requests.chat_room_id,
                chat_room_title=chat_room_title,
                total_chat_count=chat_requests.message_id,
                created_at=datetime.now().isoformat() 
            )
            self.chat_room_list_table.put_item(Item=chat_room_list.dict())
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")


    def update_total_chat_count(self, chat_requests: ChatRequest):
        try:
            response = self.chat_room_list_table.query(
                KeyConditionExpression=Key('user_id').eq(chat_requests.user_id) & 
                                       Key('chat_room_id').eq(chat_requests.chat_room_id)
            )

            if response['Items']:
                pre_item = response['Items'][0]

                chat_room_list = ChatRoomList(
                    user_id=pre_item['user_id'],
                    chat_room_id=pre_item['chat_room_id'],
                    chat_room_title=pre_item['chat_room_title'],
                    total_chat_count=chat_requests.message_id,
                    created_at=pre_item['created_at'],
                )

                self.chat_room_list_table.put_item(Item=chat_room_list.dict())
        except ClientError as e:
            self.logger.error(f"An error occurred: {e.response['Error']['Message']}")
            return None