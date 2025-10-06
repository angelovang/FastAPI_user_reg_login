from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from . import crud, schemas

router = APIRouter(
    prefix="/archaeology",
    tags=["archaeology"]
)

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
