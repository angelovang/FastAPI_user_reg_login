from sqlalchemy.orm import Session
from . import models, schemas


# CREATE
def create_layer(db: Session, layer: schemas.TbllayerCreate):
    db_layer = models.Tbllayer(**layer.dict())
    db.add(db_layer)
    db.commit()
    db.refresh(db_layer)
    return db_layer


# READ all
def get_layers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tbllayer).offset(skip).limit(limit).all()


# READ by ID
def get_layer(db: Session, layerid: int):
    return db.query(models.Tbllayer).filter(models.Tbllayer.layerid == layerid).first()


# UPDATE
def update_layer(db: Session, layerid: int, layer: schemas.TbllayerUpdate):
    db_layer = get_layer(db, layerid)
    if not db_layer:
        return None
    for field, value in layer.dict(exclude_unset=True).items():
        setattr(db_layer, field, value)
    db.commit()
    db.refresh(db_layer)
    return db_layer


# DELETE
def delete_layer(db: Session, layerid: int):
    db_layer = get_layer(db, layerid)
    if not db_layer:
        return None
    db.delete(db_layer)
    db.commit()
    return db_layer
