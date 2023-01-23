from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

import schemas
import models
from database import get_db
from oauth2 import require_user

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.CoinResponse)
def create_coin(coin: schemas.CoinsBase, db: Session = Depends(get_db),
                owner_id: str = Depends(require_user)):
    coin.user_id = owner_id
    new_coin = models.Coins(**coin.dict())
    try:
        db.add(new_coin)
        db.commit()
        db.refresh(new_coin)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Not valid data")
    return new_coin


@router.get('/', response_model=schemas.ListCoins)
def get_coins(db: Session = Depends(get_db),
              user_id: str = Depends(require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.is_superuser:
        coins = db.query(models.Coins).all()
    else:
        coins = db.query(models.Coins).filter(
            models.Coins.user_id == user.id).all()
    return {'status': 'success', 'results': len(coins), 'coins': coins}


@router.put('/{id}', response_model=schemas.CoinResponse)
def update_coin(id: str, coin: schemas.CoinsBase,
                db: Session = Depends(get_db),
                user_id: str = Depends(require_user)):
    coin_query = db.query(models.Coins).filter(models.Coins.id == id)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    updated_coin = coin_query.first()
    if not updated_coin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No coin with this id: {id}')
    if user.is_superuser or updated_coin.user_id == user.id:
        try:
            coin_query.update(coin.dict(exclude_unset=True))
        except IntegrityError:
            raise HTTPException(status_code=404, detail="Not valid data")
        db.commit()
        return updated_coin
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.delete('/{id}')
def delete_coin(id: str, db: Session = Depends(get_db),
                user_id: str = Depends(require_user)):
    coin_query = db.query(models.Coins).filter(models.Coins.id == id)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    deleted_coin = coin_query.first()
    if not deleted_coin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No coin with this id: {id}')
    if user.is_superuser or deleted_coin.user_id == user.id:
        coin_query.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
