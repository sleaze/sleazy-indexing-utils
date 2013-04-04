# -*- coding: utf-8 -*-

from .. import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

getEngine = lambda: create_engine('postgres://ppx@localhost/xhamster')

Session = sessionmaker(bind=getEngine())

_session = Session()
#getSession = lambda: sessionmaker(bind=getEngine())()
getSession = lambda: _session

#print '{0}'.format(engine.execute('select 1').scalar())

