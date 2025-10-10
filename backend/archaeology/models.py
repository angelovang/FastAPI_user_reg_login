from sqlalchemy import Column, Integer, String, Text, LargeBinary, Date, CheckConstraint, ForeignKey
from sqlalchemy.orm import validates
from backend.database import Base


# ----------- Layers -------------
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


# ------------ Includes --------------
class Tbllayerinclude(Base):
    __tablename__ = "tbllayerincludes"

    includeid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    locationid = Column(Integer, ForeignKey("tbllayers.layerid"))

    includetype = Column(
        String,
        CheckConstraint("includetype IN ('антропогенен', 'естествен')"),
        nullable=True
    )

    includetext = Column(Text, nullable=True)

    includesize = Column(
        String,
        CheckConstraint("includesize IN ('малки', 'средни', 'големи')"),
        nullable=True
    )

    includeconc = Column(
        String,
        CheckConstraint("includeconc IN ('ниска', 'средна', 'висока')"),
        nullable=True
    )

    recordenteredon = Column(Date, nullable=False)

    # --- VALIDATOR ---
    @validates("includetext")
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    def __repr__(self):
        return f"<Tbllayerinclude id={self.includeid} type={self.includetype}>"

    def serialize(self):
        return {
            'includeid': self.includeid,
            'locationid': self.locationid,
            'includetype': self.includetype,
            'includetext': self.includetext,
            'includesize': self.includesize,
            'includeconc': self.includeconc,
            'recordenteredon': self.recordenteredon
        }

