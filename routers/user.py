from passlib.context import CryptContext
from datetime import timedelta
from fastapi import APIRouter, Request, Response, status, Depends, \
    HTTPException

import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import AuthJWT
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.UserLoginCreate,
                db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(
        models.User.username == data.username)
    user = user_query.first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This username already exist')
    data.password = hash_password(data.password)
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'status': 'success', 'message': 'user created'}


@router.post('/login')
def login(data: schemas.UserLoginCreate, response: Response,
          db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = db.query(models.User).filter(
        models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect username or password')

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect username or password')

    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    response.set_cookie('access_token', access_token,
                        ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True,
                        'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60,
                        REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True,
                        'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False,
                        'lax')

    return {'status': 'success', 'access_token': access_token}


@router.get('/refresh')
def refresh_token(response: Response, request: Request,
                  Authorize: AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token,
                        ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True,
                        'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False,
                        'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'success'}
