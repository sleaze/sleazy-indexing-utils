#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Interval, String, Text, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from .temporal import parseInterval


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, name, deleted=False, createdTs=None, modifiedTs=None):
        self.id = id
        self.name = name
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)

    def parseAge(self, specifier):
        """Parses a string like "55 days ago" and produces a timestamp."""
        return datetime.now() - parseInterval(specifier)


class Video(Base):
    __tablename__ = 'Video'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', backref=backref('videos', order_by='id'))
    title = Column(String)
    description = Column(Text)
    duration = Column(Interval)
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, id, userId, title, description=None, duration=None, deleted=False, createdTs=None, modifiedTs=None):
        self.id = id
        self.userId = userId
        self.title = title
        self.description = description
        self.duration = parseInterval(duration)
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)


class Gallery(Base):
    __tablename__ = 'Gallery'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', backref=backref('galleries', order_by='id'))
    title = Column(String)
    description = Column(Text)
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, id, userId, title, description=None, deleted=False, createdTs=None, modifiedTs=None):
        self.id = id
        self.userId = userId
        self.title = title
        self.description = description
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)

