from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# TODO: Create endpoints

# Create a user POST /users
# Update a user PATCH /users/:id
# Fetch a user GET /users/:id
# Add role to a user auth.set_custom_user_claims(uid, {'engage_admin': True})
# Create JWT token for Collectr


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.get('/hi/')
async def hi():
    return {'message': 'Hi TA team!'}


handler = Mangum(app)
