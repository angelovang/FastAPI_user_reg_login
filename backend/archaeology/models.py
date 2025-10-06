from sqlalchemy import Column, Integer, String, Text, LargeBinary, Date, CheckConstraint
from sqlalchemy.orm import validates
from backend.database import Base


class Tbllayer(Base):
    __tablename__ = 'tbllayers'

    layerid = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Enums (реализирани чрез CheckConstraint)
    layertype = Column(
        String,
        CheckConstraint("layertype IN ('механичен', 'контекст')"),
        nullable=True
    )

    layername = Column(Text)

    site = Column(Text)
    sector = Column(Text)
    square = Column(Text)
    context = Column(Text)
    layer = Column(Text)
    stratum = Column(Text)
    parentid = Column(Integer)

    level = Column(Text)
    structure = Column(Text)
    includes = Column(Text)

    color1 = Column(
        String,
        CheckConstraint("color1 IN ('бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен')"),
        nullable=True
    )
    color2 = Column(
        String,
        CheckConstraint("color2 IN ('бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен')"),
        nullable=True
    )

    photos = Column(LargeBinary, nullable=True)
    drawings = Column(LargeBinary, nullable=True)

    handfragments = Column(Integer, nullable=True)
    wheelfragment = Column(Integer, nullable=True)

    recordenteredby = Column(Text)
    recordenteredon = Column(Date, nullable=False)
    recordcreatedby = Column(Text)
    recordcreatedon = Column(Date, nullable=False)

    description = Column(Text)
    akb_num = Column(Integer)

    # ---- VALIDATORS ----
    @validates(
        'layername', 'site', 'sector', 'square', 'context',
        'layer', 'stratum', 'level', 'structure', 'includes',
        'photos', 'drawings', 'handfragments', 'wheelfragment',
        'recordenteredby', 'recordcreatedby', 'description', 'akb_num'
    )
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value.strip() == '':
            return None
        return value

    def __repr__(self):
        return f"<Tbllayer id={self.layerid} name={self.layername}>"
