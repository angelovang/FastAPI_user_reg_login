from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal


# ----------- Layers ----------------

class TbllayerBase(BaseModel):
    # Enums чрез Literal
    layertype: Optional[Literal['механичен', 'контекст']] = None
    color1: Optional[Literal['бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен']] = None
    color2: Optional[Literal['бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен']] = None

    layername: Optional[str] = None
    site: Optional[str] = None
    sector: Optional[str] = None
    square: Optional[str] = None
    context: Optional[str] = None
    layer: Optional[str] = None
    stratum: Optional[str] = None
    parentid: Optional[int] = None
    level: Optional[str] = None
    structure: Optional[str] = None
    includes: Optional[str] = None
    handfragments: Optional[int] = None
    wheelfragment: Optional[int] = None
    recordenteredby: Optional[str] = None
    recordenteredon: Optional[date] = None
    recordcreatedby: Optional[str] = None
    recordcreatedon: Optional[date] = None
    description: Optional[str] = None
    akb_num: Optional[int] = None


class TbllayerCreate(TbllayerBase):
    pass


class TbllayerUpdate(TbllayerBase):
    pass


class Tbllayer(TbllayerBase):
    layerid: int

    class Config:
        orm_mode = True


# ----------- Includes ---------------

class TbllayerincludeBase(BaseModel):
    locationid: Optional[int] = None
    includetype: Optional[Literal["антропогенен", "естествен"]] = None
    includetext: Optional[str] = None
    includesize: Optional[Literal["малки", "средни", "големи"]] = None
    includeconc: Optional[Literal["ниска", "средна", "висока"]] = None
    recordenteredon: Optional[date] = None


class TbllayerincludeCreate(TbllayerincludeBase):
    pass


class TbllayerincludeUpdate(TbllayerincludeBase):
    pass


class Tbllayerinclude(TbllayerincludeBase):
    includeid: int

    class Config:
        orm_mode = True


# ------------- Fragments --------------

class TblfragmentBase(BaseModel):
    locationid: Optional[int] = None
    fragmenttype: Optional[Literal['1', '2']] = None
    technology: Optional[Literal['1', '2', '2А', '2Б']] = None
    baking: Optional[Literal['Р', 'Н']] = None
    fract: Optional[Literal['1', '2', '3']] = None
    primarycolor: Optional[Literal[
        'бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен'
    ]] = None
    secondarycolor: Optional[Literal[
        'бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен'
    ]] = None
    covering: Optional[Literal['да','не','Ф1','Ф2','Б','Г']] = None
    includesconc: Optional[Literal['+','-']] = None
    includessize: Optional[Literal['М','С','Г']] = None
    surface: Optional[Literal['А','Б','В','В1','В2','Г']] = None

    count: int = 0

    onepot: Optional[Literal['да','не']] = None

    # piecetype е силен enum (много стойности), за да не правим ужасно дълъг Literal тук,
    # можем да приемем str, но по-добре да оставим str и валидираме от UI.
    piecetype: str
    wallthickness: Optional[Literal['М','С','Г']] = None
    handlesize: Optional[Literal['М','С','Г']] = None
    handletype: Optional[str] = None
    dishsize: Optional[Literal['М','С','Г']] = None

    bottomtype: Optional[Literal['А','Б','В','А1','А2','Б1','Б2','В1','В2']] = None
    outline: Optional[Literal['1','2','3']] = None

    category: Optional[str] = None
    form: Optional[str] = None
    type: Optional[int] = None
    subtype: Optional[str] = None
    variant: Optional[int] = None

    note: Optional[str] = None
    inventory: Optional[str] = None

    recordenteredby: Optional[str] = None
    recordenteredon: Optional[date] = None


class TblfragmentCreate(TblfragmentBase):
    pass


class TblfragmentUpdate(TblfragmentBase):
    pass


class Tblfragment(TblfragmentBase):
    fragmentid: int

    class Config:
        orm_mode = True
