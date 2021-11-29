# Auth User Service
Project created to handle User data for others apps in TrueAccord

# Here's what it does
1. fits into CSDP's deployment pipeline. (dev, qa, staging to prod)
2. Also can be pushed into CNC for initial testing
3. Examples of different events (s3, dynamodb, web, etc)
4. python native and golang container examples
5. CDK template that uses variables for names, so it's always <env>-<application>-<thing> (IE: pcid-email-magic-doohickey)
6. Can be added to other deployments, can deploy multiple lambdas

  
# TODO: 
1. SAM/Secptre example? is it necessary?
2. Python example
3. Events
4. demonstration of multiple lambdas in a single deployment
5. Mutation examples (for SAML roles)

# Instructions
1. Create template:
    - From infrastructure folder run: ```aws-okta exec cnc -- cdk synth ```
2. Deploy project:
    - From infrastructure folder run: ```aws-okta exec cnc -- cdk deploy ```
