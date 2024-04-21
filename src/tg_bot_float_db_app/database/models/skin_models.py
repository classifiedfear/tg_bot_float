from __future__ import annotations

from typing import List

import sqlalchemy
from sqlalchemy import orm

from tg_bot_float_db_app.database.declar_base import Base


class RelationModel(Base):
    __tablename__ = 'relation_model'

    weapon_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('weapon.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    skin_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('skin.id', ondelete='cascade'), primary_key=True, nullable=False
    )
    quality_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey('quality.id', ondelete='cascade'), primary_key=True, nullable=False
    )

    weapon: orm.Mapped['WeaponModel'] = orm.relationship('WeaponModel', back_populates='w_s_q')
    skin: orm.Mapped['SkinModel'] = orm.relationship('SkinModel', back_populates='w_s_q')
    quality: orm.Mapped['QualityModel'] = orm.relationship('QualityModel', back_populates='w_s_q')


class WeaponModel(Base):
    __tablename__ = 'weapon'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, unique=True, nullable=False)

    w_s_q: orm.Mapped[List['RelationModel']] = orm.relationship(
        'RelationModel', back_populates='weapon', cascade='all, delete', passive_deletes=True
    )


class SkinModel(Base):
    __tablename__ = 'skin'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False, unique=True)

    stattrak_existence: orm.Mapped[bool] = orm.mapped_column(sqlalchemy.Boolean, nullable=False)

    w_s_q: orm.Mapped[List['RelationModel']] = orm.relationship(
        'RelationModel', back_populates='skin', cascade='all, delete', passive_deletes=True
    )


class QualityModel(Base):
    __tablename__ = 'quality'

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, unique=True, nullable=False)

    w_s_q: orm.Mapped[List['RelationModel']] = orm.relationship(
        'RelationModel', back_populates='quality', cascade='all, delete', passive_deletes=True
    )

