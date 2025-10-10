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