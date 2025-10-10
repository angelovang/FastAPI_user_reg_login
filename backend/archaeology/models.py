
from sqlalchemy import Column, Integer, String, Text, LargeBinary, Date, CheckConstraint, ForeignKey
from sqlalchemy.orm import validates
from backend.database import Base
from sqlalchemy.sql import text



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


# ------------ Fragments --------------

class Tblfragment(Base):
    __tablename__ = 'tblfragments'

    fragmentid = Column(Integer, primary_key=True, autoincrement=True, index=True)

    locationid = Column(Integer, ForeignKey('tbllayers.layerid'), nullable=True)

    # Enums реализирани чрез CheckConstraint (SQLite няма native ENUM)
    fragmenttype = Column(String(10), CheckConstraint("fragmenttype IN ('1','2')"), nullable=True)
    technology = Column(String(10), CheckConstraint("technology IN ('1','2','2А','2Б')"), nullable=True)
    baking = Column(String(3), CheckConstraint("baking IN ('Р','Н')"), nullable=True)
    fract = Column(String(3), CheckConstraint("fract IN ('1','2','3')"), nullable=True)
    primarycolor = Column(String(20), CheckConstraint(
        "primarycolor IN ('бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен')"
    ), nullable=True)
    secondarycolor = Column(String(20), CheckConstraint(
        "secondarycolor IN ('бял','жълт','охра','червен','сив','тъмносив','кафяв','светлокафяв','тъмнокафяв','черен')"
    ), nullable=True)
    covering = Column(String(5), CheckConstraint(
        "covering IN ('да','не','Ф1','Ф2','Б','Г')"
    ), nullable=True)
    includesconc = Column(String(2), CheckConstraint("includesconc IN ('+','-')"), nullable=True)
    includessize = Column(String(2), CheckConstraint("includessize IN ('М','С','Г')"), nullable=True)
    surface = Column(String(3), CheckConstraint("surface IN ('А','Б','В','В1','В2','Г')"), nullable=True)

    count = Column(Integer, nullable=False, default=0)

    onepot = Column(String(3), CheckConstraint("onepot IN ('да','не')"), nullable=True)

    piecetype = Column(String(50), nullable=False)  # множество възможни стойности (списък в schema)
    wallthickness = Column(String(2), CheckConstraint("wallthickness IN ('М','С','Г')"), nullable=True)
    handlesize = Column(String(2), CheckConstraint("handlesize IN ('М','С','Г')"), nullable=True)
    handletype = Column(String(50), nullable=True)

    dishsize = Column(String(2), CheckConstraint("dishsize IN ('М','С','Г')"), nullable=True)

    bottomtype = Column(String(3), CheckConstraint(
        "bottomtype IN ('А','Б','В','А1','А2','Б1','Б2','В1','В2')"
    ), nullable=True)
    outline = Column(String(3), CheckConstraint("outline IN ('1','2','3')"), nullable=True)

    category = Column(String(5), nullable=True)
    form = Column(String(5), nullable=True)
    type = Column(Integer, nullable=True)
    subtype = Column(String(3), nullable=True)
    variant = Column(Integer, nullable=True)

    note = Column(Text, nullable=True)
    inventory = Column(Text, nullable=True)

    recordenteredby = Column(Text, nullable=True)
    recordenteredon = Column(Date, nullable=False)

    # ---- validators: преобразуват празен string -> NULL ----
    @validates(
        'fragmenttype', 'technology', 'baking', 'fract', 'primarycolor', 'secondarycolor',
        'covering', 'includesconc', 'includessize', 'surface', 'onepot',
        'piecetype', 'wallthickness', 'handlesize', 'handletype',
        'dishsize', 'bottomtype', 'outline', 'category', 'form',
        'subtype', 'note', 'inventory', 'recordenteredby'
    )
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value.strip() == '':
            return None
        return value

    def __repr__(self):
        return f"<Tblfragment id={self.fragmentid} location={self.locationid}>"

    def serialize(self):
        return {
            "fragmentid": self.fragmentid,
            "locationid": self.locationid,
            "fragmenttype": self.fragmenttype,
            "technology": self.technology,
            "baking": self.baking,
            "fract": self.fract,
            "primarycolor": self.primarycolor,
            "secondarycolor": self.secondarycolor,
            "covering": self.covering,
            "includesconc": self.includesconc,
            "includessize": self.includessize,
            "surface": self.surface,
            "count": self.count,
            "onepot": self.onepot,
            "piecetype": self.piecetype,
            "wallthickness": self.wallthickness,
            "handlesize": self.handlesize,
            "handletype": self.handletype,
            "dishsize": self.dishsize,
            "bottomtype": self.bottomtype,
            "outline": self.outline,
            "category": self.category,
            "form": self.form,
            "type": self.type,
            "subtype": self.subtype,
            "variant": self.variant,
            "note": self.note,
            "inventory": self.inventory,
            "recordenteredby": self.recordenteredby,
            "recordenteredon": self.recordenteredon,
        }
