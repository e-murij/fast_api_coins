from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

import schemas
import models
from database import get_db

router = APIRouter()


# CRUD типов монет
@router.get('/type')
def get_types(db: Session = Depends(get_db)):
    types = db.query(models.Type).all()
    return {'type': types}


@router.post('/type', status_code=status.HTTP_201_CREATED,
             response_model=schemas.Type)
def create_type(type: schemas.TypeBase, db: Session = Depends(get_db)):
    new_type = models.Type(**type.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.put('/type/{id}', response_model=schemas.Type)
def update_type(id: str, type: schemas.TypeBase,
                db: Session = Depends(get_db)):
    type_query = db.query(models.Type).filter(models.Type.id == id)
    updated_type = type_query.first()
    if not updated_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No type with this id: {id}')
    type_query.update(type.dict(exclude_unset=True))
    db.commit()
    return updated_type


@router.delete('/type/{id}')
def delete_type(id: str, db: Session = Depends(get_db)):
    type_query = db.query(models.Type).filter(models.Type.id == id)
    updated_type = type_query.first()
    if not updated_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No type with this id: {id}')
    type_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# CRUD валют
@router.get('/currency')
def get_currency(db: Session = Depends(get_db)):
    currency = db.query(models.Currency).all()
    return {'currency': currency}


@router.post('/currency', status_code=status.HTTP_201_CREATED,
             response_model=schemas.Currency)
def create_currency(currency: schemas.CurrencyBase,
                    db: Session = Depends(get_db)):
    new_currency = models.Currency(**currency.dict())
    db.add(new_currency)
    db.commit()
    db.refresh(new_currency)
    return new_currency


@router.put('/currency/{id}', response_model=schemas.Currency)
def update_currency(id: str, currency: schemas.CurrencyBase,
                    db: Session = Depends(get_db)):
    currency_query = db.query(models.Currency).filter(models.Currency.id == id)
    updated_currency = currency_query.first()
    if not updated_currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No currency with this id: {id}')
    currency_query.update(currency.dict(exclude_unset=True))
    db.commit()
    return updated_currency


@router.delete('/currency/{id}')
def delete_currency(id: str, db: Session = Depends(get_db)):
    currency_query = db.query(models.Currency).filter(models.Currency.id == id)
    updated_currency = currency_query.first()
    if not updated_currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No currency with this id: {id}')
    currency_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# CRUD монетный двор
@router.get('/md')
def get_md(db: Session = Depends(get_db)):
    md = db.query(models.Md).all()
    return {'md': md}


@router.post('/md', status_code=status.HTTP_201_CREATED,
             response_model=schemas.Md)
def create_md(md: schemas.MdBase, db: Session = Depends(get_db)):
    new_md = models.Md(**md.dict())
    db.add(new_md)
    db.commit()
    db.refresh(new_md)
    return new_md


@router.put('/md/{id}', response_model=schemas.Md)
def update_md(id: str, md: schemas.CurrencyBase,
              db: Session = Depends(get_db)):
    md_query = db.query(models.Md).filter(models.Md.id == id)
    updated_md = md_query.first()
    if not updated_md:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No md with this id: {id}')
    md_query.update(md.dict(exclude_unset=True))
    db.commit()
    return updated_md


@router.delete('/md/{id}')
def delete_md(id: str, db: Session = Depends(get_db)):
    md_query = db.query(models.Md).filter(models.Md.id == id)
    updated_md = md_query.first()
    if not updated_md:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No md with this id: {id}')
    md_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# CRUD выпускающее государство
@router.get('/state')
def get_state(db: Session = Depends(get_db)):
    state = db.query(models.State).all()
    return {'state': state}


@router.post('/state', status_code=status.HTTP_201_CREATED,
             response_model=schemas.State)
def create_state(state: schemas.StateBase, db: Session = Depends(get_db)):
    new_state = models.State(**state.dict())
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state


@router.put('/state/{id}', response_model=schemas.State)
def update_state(id: str, state: schemas.StateBase,
                 db: Session = Depends(get_db)):
    state_query = db.query(models.State).filter(models.State.id == id)
    updated_state = state_query.first()
    if not updated_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No state with this id: {id}')
    state_query.update(state.dict(exclude_unset=True))
    db.commit()
    return updated_state


@router.delete('/state/{id}')
def delete_state(id: str, db: Session = Depends(get_db)):
    state_query = db.query(models.State).filter(models.State.id == id)
    updated_state = state_query.first()
    if not updated_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No state with this id: {id}')
    state_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
