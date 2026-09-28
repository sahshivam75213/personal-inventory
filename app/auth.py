from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# password hashing configuration
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto") # password ko secure bana rahe hain q ki password ko plain text me store nahi karna chahiye

# JWT configuration
SECRET_KEY = "change-ths-key-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # kitne der tak token valid rahega

def hash_password(password: str): # ye function plain password ko hashed password me convert karta hai
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str): # ye function login ke time use hoga
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict): # ye function user ke liye JWT access token create karta hai aur function dictionary receive karega
    to_encode = data.copy() # Original dictionary ki copy banayi ja rahi hai

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # yaha expiry time ban raha hai
    to_encode.update({"exp": expire}) # yaha expiry time ko dictionary me add kiya ja raha hai JWT ke andar

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # yaha actual JWT token generate hota hai

    return encoded_jwt # ye JWT token ko return karta hai

def decode_access_token(token: str): # ye function received JWT token ko decode karega
    try:    # ye check karega token validity, matching secret key, token expiry, correct algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # agr token valid hai to payload return hoga
    except JWTError:
        return None # Invalid token par application crash nahi karega, balki None return karega
    
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return payload

    except JWTError:
        raise credentials_exception
