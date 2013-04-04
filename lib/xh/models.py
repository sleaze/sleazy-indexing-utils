#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Interval, String, Text, Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from .temporal import parseInterval
from dateutil import parser as dateParser


Base = declarative_base()


class X(object):
    def parseAge(self, specifier):
        """Parses a string like "55 days ago" and produces a timestamp."""
        from datetime import datetime
        if specifier is None or not isinstance(specifier, str):
            return specifier

        if specifier.endswith(' ago'):
            interval = parseInterval(specifier)
            return datetime.now() - interval
        else:
            return dateParser.parse(specifier)


class User(Base, X):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, name, deleted=False, createdTs=None, modifiedTs=None, **kw):
        super(User, self).__init__(**kw)
        self.name = name
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)


class Video(Base, X):
    __tablename__ = 'Video'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', backref=backref('videos'))#, order_by=id))
    title = Column(String)
    description = Column(Text)
    duration = Column(Interval(second_precision=False))
    categories = Column(ARRAY(String))
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, id, userId, title, description=None, duration=None, categories=None, deleted=False, createdTs=None, modifiedTs=None):
        self.id = id
        self.userId = userId
        self.title = title
        self.description = description
        self.duration = parseInterval(duration)
        self.categories = categories
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)


class Gallery(Base, X):
    __tablename__ = 'Gallery'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', backref=backref('galleries'))#, order_by='id'))
    title = Column(String)
    description = Column(Text)
    categories = Column(ARRAY(String))
    deleted = Column(Boolean)
    createdTs = Column(Time)
    modifiedTs = Column(Time)

    def __init__(self, id, userId, title, description=None, categories=None, deleted=False, createdTs=None, modifiedTs=None):
        self.id = id
        self.userId = userId
        self.title = title
        self.description = description
        self.categories = categories
        self.deleted = deleted
        self.createdTs = self.parseAge(createdTs)
        self.modifiedTs = self.parseAge(modifiedTs)

