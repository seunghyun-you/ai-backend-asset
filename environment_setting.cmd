@echo off
set "USER_ID_VALUE=USER_ID_VALUE"
set "USER_NAME=USER_NAME"
set "EMAIL=USER_EMAIL_INFORMATION"
set "PASSWORD=HASHED_PASSWORD"
set "OWNER_NAME=OWNER_NAME"
set "SECRET_KEY=YOUR_SECRET_KEY"
set "ALGORITHM=HASH_ALGORITHM"

:: 로그인 접속에 사용할 초기 계정을 AWS Systems Manager Parameter Store에 구성
aws ssm put-parameter --name "/generative_ai_app/user01/userid" --value "%USER_ID_VALUE%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"
aws ssm put-parameter --name "/generative_ai_app/user01/username" --value "%USER_NAME%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"
aws ssm put-parameter --name "/generative_ai_app/user01/email" --value "%EMAIL%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"
aws ssm put-parameter --name "/generative_ai_app/user01/hashed_password" --value "%PASSWORD%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"

:: 로그인 인증 과정에 사용할 보안 관련 설정 값
aws ssm put-parameter --name "/SECRET_KEY" --value "%SECRET_KEY%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"
aws ssm put-parameter --name "/ALGORITHM" --value "%ALGORITHM%" --type "SecureString" --tags "Key=Owner,Value=%OWNER_NAME%"