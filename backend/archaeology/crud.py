from sqlalchemy.orm import Session
from . import models, schemas


# ------------ Layers CRUD --------------
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


# -------------------- INCLUDES CRUD --------------------
def create_layer_include(db: Session, include: schemas.TbllayerincludeCreate):
    db_include = models.Tbllayerinclude(**include.dict())
    db.add(db_include)
    db.commit()
    db.refresh(db_include)
    return db_include


def get_layer_includes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tbllayerinclude).offset(skip).limit(limit).all()


def get_layer_include(db: Session, includeid: int):
    return db.query(models.Tbllayerinclude).filter(models.Tbllayerinclude.includeid == includeid).first()


def update_layer_include(db: Session, includeid: int, include: schemas.TbllayerincludeUpdate):
    db_include = get_layer_include(db, includeid)
    if not db_include:
        return None
    for key, value in include.dict(exclude_unset=True).items():
        setattr(db_include, key, value)
    db.commit()
    db.refresh(db_include)
    return db_include


def delete_layer_include(db: Session, includeid: int):
    db_include = get_layer_include(db, includeid)
    if not db_include:
        return None
    db.delete(db_include)
    db.commit()
    return db_include
