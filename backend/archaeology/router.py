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

#---------- CREATE ---------

@router.post("/layers/", response_model=schemas.Tbllayer)
def create_layer(layer: schemas.TbllayerCreate, db: Session = Depends(get_db)):
    return crud.create_layer(db, layer)

#---------- READ ALL --------

@router.get("/layers/", response_model=List[schemas.Tbllayer])
def read_layers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_layers(db, skip=skip, limit=limit)

#--------- READ BY ID -------

@router.get("/layers/{layerid}", response_model=schemas.Tbllayer)
def read_layer(layerid: int, db: Session = Depends(get_db)):
    db_layer = crud.get_layer(db, layerid)
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer

#--------- UPDATE ----------

@router.put("/layers/{layerid}", response_model=schemas.Tbllayer)
def update_layer(layerid: int, layer: schemas.TbllayerUpdate, db: Session = Depends(get_db)):
    db_layer = crud.update_layer(db, layerid, layer, )
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer


#-------- DELETE -----------

@router.delete("/layers/{layerid}", response_model=schemas.Tbllayer)
def delete_layer(layerid: int, db: Session = Depends(get_db)):
    db_layer = crud.delete_layer(db, layerid)
    if not db_layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return db_layer


# ----------- Includes ----------------

#----------- CREATE -----------

@router.post("/layer_includes/", response_model=schemas.Tbllayerinclude)
def create_include(include: schemas.TbllayerincludeCreate, db: Session = Depends(get_db)):
    return crud.create_layer_include(db, include)

#----------- READ ALL -------------

@router.get("/layer_includes/", response_model=List[schemas.Tbllayerinclude])
def read_includes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_layer_includes(db, skip=skip, limit=limit)

# ---------- READ BY ID --------

@router.get("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def read_include(includeid: int, db: Session = Depends(get_db)):
    db_include = crud.get_layer_include(db, includeid)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include

#----------- UPDATE ----------

@router.put("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def update_include(includeid: int, include: schemas.TbllayerincludeUpdate, db: Session = Depends(get_db)):
    db_include = crud.update_layer_include(db, includeid, include)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include

#------------ DELETE ---------

@router.delete("/layer_includes/{includeid}", response_model=schemas.Tbllayerinclude)
def delete_include(includeid: int, db: Session = Depends(get_db)):
    db_include = crud.delete_layer_include(db, includeid)
    if not db_include:
        raise HTTPException(status_code=404, detail="Include not found")
    return db_include


# ------------- Fragments -----------------

# CREATE
@router.post("/fragments/", response_model=schemas.Tblfragment)
def create_fragment(fragment: schemas.TblfragmentCreate, db: Session = Depends(get_db)):
    return crud.create_fragment(db, fragment)


# READ ALL
@router.get("/fragments/", response_model=List[schemas.Tblfragment])
def read_fragments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_fragments(db, skip=skip, limit=limit)


# READ BY ID
@router.get("/fragments/{fragmentid}", response_model=schemas.Tblfragment)
def read_fragment(fragmentid: int, db: Session = Depends(get_db)):
    db_fr = crud.get_fragment(db, fragmentid)
    if not db_fr:
        raise HTTPException(status_code=404, detail="Fragment not found")
    return db_fr


# UPDATE
@router.put("/fragments/{fragmentid}", response_model=schemas.Tblfragment)
def update_fragment(fragmentid: int, fragment: schemas.TblfragmentUpdate, db: Session = Depends(get_db)):
    db_fr = crud.update_fragment(db, fragmentid, fragment)
    if not db_fr:
        raise HTTPException(status_code=404, detail="Fragment not found")
    return db_fr


# DELETE
@router.delete("/fragments/{fragmentid}", response_model=schemas.Tblfragment)
def delete_fragment(fragmentid: int, db: Session = Depends(get_db)):
    db_fr = crud.delete_fragment(db, fragmentid)
    if not db_fr:
        raise HTTPException(status_code=404, detail="Fragment not found")
    return db_fr


# --------------- POK -----------------

# ----------- READ ALL ------------
@router.get("/pok", response_model=list[schemas.PokOut])
def get_poks(db: Session = Depends(get_db)):
    return crud.get_poks(db)


# ----------- READ BY ID ----------
@router.get("/pok/{pokid}", response_model=schemas.PokOut)
def get_pok(pokid: int, db: Session = Depends(get_db)):
    pok = crud.get_pok_by_id(db, pokid)
    if not pok:
        raise HTTPException(status_code=404, detail="POK not found")
    return pok


# ----------- CREATE -----------
@router.post("/pok", response_model=schemas.PokOut)
def create_pok(pok: schemas.PokCreate, db: Session = Depends(get_db)):
    return crud.create_pok(db, pok)


# ---------- UPDATE -------------
@router.put("/pok/{pokid}", response_model=schemas.PokOut)
def update_pok(pokid: int, pok_data: schemas.PokUpdate, db: Session = Depends(get_db)):
    pok = crud.update_pok(db, pokid, pok_data)
    if not pok:
        raise HTTPException(status_code=404, detail="POK not found")
    return pok


# ---------- DELETE -------------
@router.delete("/pok/{pokid}")
def delete_pok(pokid: int, db: Session = Depends(get_db)):
    success = crud.delete_pok(db, pokid)
    if not success:
        raise HTTPException(status_code=404, detail="POK not found")
    return {"detail": "POK deleted successfully"}


# --------------- Ornaments ---------------

# ---------- READ ALL --------------
@router.get("/ornaments/", response_model=list[schemas.OrnamentOut])
def read_ornaments(db: Session = Depends(get_db)):
    return crud.get_all_ornaments(db)

# ---------- CREATE -------------
@router.post("/ornaments/", response_model=schemas.OrnamentOut)
def create_ornament(ornament: schemas.OrnamentCreate, db: Session = Depends(get_db)):
    return crud.create_ornament(db, ornament)

# ---------- READ BY ID ------------
@router.get("/ornaments/{ornamentid}", response_model=schemas.OrnamentOut)
def read_ornament(ornamentid: int, db: Session = Depends(get_db)):
    db_ornament = crud.get_ornament(db, ornamentid)
    if not db_ornament:
        raise HTTPException(status_code=404, detail="Ornament not found")
    return db_ornament

# ---------- UPDATE ------------
@router.put("/ornaments/{ornamentid}", response_model=schemas.OrnamentOut)
def update_ornament(ornamentid: int, ornament: schemas.OrnamentUpdate, db: Session = Depends(get_db)):
    db_ornament = crud.update_ornament(db, ornamentid, ornament)
    if not db_ornament:
        raise HTTPException(status_code=404, detail="Ornament not found")
    return db_ornament

# --------- DELETE -----------
@router.delete("/ornaments/{ornamentid}")
def delete_ornament(ornamentid: int, db: Session = Depends(get_db)):
    db_ornament = crud.delete_ornament(db, ornamentid)
    if not db_ornament:
        raise HTTPException(status_code=404, detail="Ornament not found")
    return {"detail": "Deleted successfully"}
