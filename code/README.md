# Code for Auth User Service

## Local development

### preconditions
Install awscli
```brew install awscli```

Check if aws is installed
```aws --version```

Create .env from .env.example
```cp .env.example .env```

### steps
1. Configure aws credentials and create a profile
```aws configure --profile localstack```

should be compleated like this:
```
AWS Access Key ID: test
AWS Secret Access Key: test
Default region name: us-east-2
Default output format [None]:
```
2. Set the profile in a terminal
```export AWS_PROFILE=localstack```
3. Create the table
```aws dynamodb create-table --cli-input-json file://utils/db.json --endpoint-url=http://localhost:4566```

## Testing
### preconditions
Docker project must be running using: ```docker-compose up```

### steps
1. Get into container
```make shell-web```
2. Run tests
```poetry run pytest```
