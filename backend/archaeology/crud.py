from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date


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


# ------------- Fragments CRUD -------------

def create_fragment(db: Session, fragment: schemas.TblfragmentCreate):
    db_fragment = models.Tblfragment(**fragment.dict())
    db.add(db_fragment)
    db.commit()
    db.refresh(db_fragment)
    return db_fragment


def get_fragments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tblfragment).offset(skip).limit(limit).all()


def get_fragment(db: Session, fragmentid: int):
    return db.query(models.Tblfragment).filter(models.Tblfragment.fragmentid == fragmentid).first()


def update_fragment(db: Session, fragmentid: int, fragment: schemas.TblfragmentUpdate):
    db_fr = db.query(models.Tblfragment).filter(models.Tblfragment.fragmentid == fragmentid).first()
    if not db_fr:
        return None
    for k, v in fragment.dict(exclude_unset=True).items():
        setattr(db_fr, k, v)
    db.commit()
    db.refresh(db_fr)
    return db_fr


def delete_fragment(db: Session, fragmentid: int):
    db_fr = db.query(models.Tblfragment).filter(models.Tblfragment.fragmentid == fragmentid).first()
    if not db_fr:
        return None
    db.delete(db_fr)
    db.commit()
    return db_fr


# -------------- POK CRUD ---------------

# 🟢 Създаване на нов запис
def create_pok(db: Session, pok: schemas.PokCreate):
    new_pok = models.Tblpok(
        locationid=pok.locationid,
        type=pok.type,
        quantity=pok.quantity,
        weight=pok.weight,
        sok_weight=pok.sok_weight,
        recordenteredon=pok.recordenteredon or date.today(),
    )
    db.add(new_pok)
    db.commit()
    db.refresh(new_pok)
    return new_pok


# 🟢 Взимане на всички записи
def get_poks(db: Session):
    return db.query(models.Tblpok).all()


# 🟢 Взимане на един запис по ID
def get_pok_by_id(db: Session, pokid: int):
    return db.query(models.Tblpok).filter(models.Tblpok.pokid == pokid).first()


# 🟡 Обновяване на съществуващ запис
def update_pok(db: Session, pokid: int, pok_data: schemas.PokUpdate):
    pok = db.query(models.Tblpok).filter(models.Tblpok.pokid == pokid).first()
    if not pok:
        return None

    for key, value in pok_data.dict(exclude_unset=True).items():
        setattr(pok, key, value)

    db.commit()
    db.refresh(pok)
    return pok


# 🔴 Изтриване
def delete_pok(db: Session, pokid: int):
    pok = db.query(models.Tblpok).filter(models.Tblpok.pokid == pokid).first()
    if not pok:
        return None

    db.delete(pok)
    db.commit()
    return True


# ---- ORNAMENTS ----

def get_all_ornaments(db: Session):
    return db.query(models.Tblornament).all()

def get_ornament(db: Session, ornamentid: int):
    return db.query(models.Tblornament).filter(models.Tblornament.ornamentid == ornamentid).first()

def create_ornament(db: Session, ornament: schemas.OrnamentCreate):
    db_ornament = models.Tblornament(**ornament.dict())
    db.add(db_ornament)
    db.commit()
    db.refresh(db_ornament)
    return db_ornament


def update_ornament(db: Session, ornamentid: int, ornament: schemas.OrnamentUpdate):
    db_ornament = db.query(models.Tblornament).filter(models.Tblornament.ornamentid == ornamentid).first()
    if not db_ornament:
        return None
    for key, value in ornament.dict(exclude_unset=True).items():
        setattr(db_ornament, key, value)
    db.commit()
    db.refresh(db_ornament)
    return db_ornament

def delete_ornament(db: Session, ornamentid: int):
    db_ornament = db.query(models.Tblornament).filter(models.Tblornament.ornamentid == ornamentid).first()
    if not db_ornament:
        return None
    db.delete(db_ornament)
    db.commit()
    return db_ornament
