from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from . import crud, schemas

router = APIRouter(
    prefix="/archaeology",
    tags=["archaeology"]
)

# ---------- Layers -------------
# -----------------------
# CREATE
# -----------------------
@router.post("/layers/", response_model=schemas.Tbllayer)
def create_layer(layer: schemas.TbllayerCreate, db: Session = Depends(get_db)):
    return crud.create_layer(db, layer)

# -----------------------
# READ ALL
# -----------------------
@router.get("/layers/", response_model=List[schemas.Tbllayer])
def read_layers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_layers(db, skip=skip, limit=limit)

# -----------------------
# READ BY ID
# -----------------------
@router.get("/layers/{layerid}", response_model=schemas.Tbllayer)
def read_layer(layerid: int, db: Session = Depends(get_db)):
    db_layer = crud.get_layer(db, layerid)
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer

# -----------------------
# UPDATE
# -----------------------
@router.put("/layers/{layerid}", response_model=schemas.Tbllayer)
def update_layer(layerid: int, layer: schemas.TbllayerUpdate, db: Session = Depends(get_db)):
    db_layer = crud.update_layer(db, layerid, layer)
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer

# -----------------------
# DELETE
# -----------------------
@router.delete("/layers/{layerid}", response_model=schemas.Tbllayer)
def delete_layer(layerid: int, db: Session = Depends(get_db)):
    db_layer = crud.delete_layer(db, layerid)
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer


# ----------- Includes ----------------
# -----------------------
# TBL LAYER INCLUDES
# -----------------------
@router.post("/layer_includes/", response_model=schemas.Tbllayerinclude)
def create_include(include: schemas.TbllayerincludeCreate, db: Session = Depends(get_db)):
    return crud.create_layer_include(db, include)


@router.get("/layer_includes/", response_model=List[schemas.Tbllayerinclude])
def read_includes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_layer_includes(db, skip=skip, limit=limit)


@router.get("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def read_include(includeid: int, db: Session = Depends(get_db)):
    db_include = crud.get_layer_include(db, includeid)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include


@router.put("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def update_include(includeid: int, include: schemas.TbllayerincludeUpdate, db: Session = Depends(get_db)):
    db_include = crud.update_layer_include(db, includeid, include)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include


@router.delete("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def delete_include(includeid: int, db: Session = Depends(get_db)):
    db_include = crud.delete_layer_include(db, includeid)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include
