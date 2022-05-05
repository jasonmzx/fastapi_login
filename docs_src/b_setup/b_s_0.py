from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

@app.post('/auth/token')
async def login(req: Request, data: OAuth2PasswordRequestForm = Depends()): 
    #Depends is basically asserting the incoming request (If allowed to access or not)
    #Here it doesn't make much sense, but below you'll see a use case for it

    # These are from my frontend (I sent a JSON Post Body in)
    username = data.user
    password = data.passwd 

    #Search if the username exists as a row in my database (Or JSON if it's NoSQL) 
    user = auth.load_user(username) 

    #Raising some basic exceptions for cases we'll run into
    #Users typing in wrong user/pass combos, users trying to login as none existent profiles

    if user is None:
        return HTTPException(status_code=404, detail="Username wasn't found.")

    if not auth.verify_password(password, user[2]):
        return HTTPException(status_code=403, detail="Wrong password for this profile.")

    #Here is where We use fastapi_login's .create_access_token() function to generate a JWT with PK as username (in this case)

    access_token = auth.manager.create_access_token(
        data={
            "sub": username, #IMPORTANT: The Primary key here always needs to be titled "sub" (Further Explanation below)
        }
    )

    #Now it returns my JWT (access token) & the token type, in this case: "bearer" (bearer of token, bearer of profile)

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }