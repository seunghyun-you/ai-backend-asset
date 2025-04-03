#!/bin/bash

# 실제 값으로 변경 후 스크립트 실행
USER_ID_VALUE="sh1517"
USER_NAME="SeungHyun.You"
EMAIL="sh1517.gmail.com"
PASSWORD="$2b$12$jHgKE/.zfC2OomLjm27.d.V72FD0rJxhBQnqMDBTDaZef.8AVsrMe"
OWNER_NAME="sh1517"
SECRET_KEY="YOUR_SECRET_KEY"
ALGORITHM="HS256"


# 로그인 접속에 사용할 초기 접속 계정을 AWS Systems Manager Parameter Store에 구성하기 위한 명령어
aws ssm put-parameter \
 --name "/generative_ai_app/user01/userid" \
 --value $USER_ID_VALUE \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME

aws ssm put-parameter \
 --name "/generative_ai_app/user01/username" \
 --value $USER_NAME \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME

aws ssm put-parameter \
 --name "/generative_ai_app/user01/email" \
 --value $EMAIL \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME

aws ssm put-parameter \
 --name "/generative_ai_app/user01/hashed_password" \
 --value $PASSWORD \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME

# 로그인 인증 과정에 사용할 보안 관련 설정 값
aws ssm put-parameter \
 --name "/SECRET_KEY" \
 --value $SECRET_KEY \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME

aws ssm put-parameter \
 --name "/ALGORITHM" \
 --value $ALGORITHM \
 --type "SecureString" \
 --tag Key=Owner,Value=$OWNER_NAME
