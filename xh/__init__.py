# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://ppx@localhost/xhamster')

Session = sessionmaker(bind=engine)

print '{0}'.format(engine.execute('select 1').scalar())

