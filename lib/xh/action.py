# -*- coding: utf-8 -*-

from . import getSession #engine, Session
from .models import User, Gallery, Video
from ..wget import wget

import logging
from pyquery import PyQuery as pq
from dateutil import parser as dateParser
from datetime import datetime


logger = logging.getLogger('xhamster')

def getOrCreateUser(name, session=None):
#    needToClose = False
    if session is None:
        session = getSession()
#        needToClose = True
    user = session.query(User).filter(User.name==name).first()
    if user is None:
        user = User(name=name)
        session.add(user)
        session.commit()
#        if needToClose:
#            session.close()

    print 'user=',user
    return user

def video(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

    session = getSession() #Session()

    def isDeletedLocally():
        return session.query(Video).filter(Video.id==identifier).filter(Video.deleted==True).first() is not None

    if isDeletedLocally():
        logger.info('Skipping video id={0} because it is already marked as deleted'.format(identifier))
#        session.close()
        return

    d = pq(wget(url))

    def isDeleted():
        return d('span.error').text() is not None and d('span.error').text().lower() == 'this video was deleted'

    if isDeleted():
        video = session.query(Video).filter(Video.id==identifier).first()
        if video is None:
            # Take note of deleted video.
            video = Video(id=identifier, userId=None, title=extra.replace('_', ' ').replace('.html', ''), deleted=True, createdTs=datetime.now(), modifiedTs=datetime.now())
            logger.info('Saving deleted video, id={0}'.format(identifier))
        else:
            # Mark deleted.
            video.deleted = True
            video.modifiedTs = datetime.now()
            logger.info('Marked video deleted, id={0}'.format(identifier))

        session.add(video)
        session.commit()
#        session.close()
        return

    video = session.query(Video).filter(Video.id==identifier).first()

    if video is not None:
        # Update the last modified ts.
        video.modifiedTs = datetime.now()
        session.add(video)
        logger.info('Already knew about video id={0} userId={1} title="{2}"'.format(identifier, video.userId, video.title))

    else:
        # Add the video to the db.
        def discoverInfo():
            discovered = {
                'id': identifier,
                'title': d('th.mTitle h1').text(),
                'duration': None,
                'createdTs': None,
                'modifiedTs': datetime.now(),
                'userId': None
            }

            #f = d('tr td b:nth-child(1)')#b.text:contains("^.*$")')
            for row in d('table.stats_table tr'):
                children = row.getchildren()
                if len(children) > 1:
                    colName = children[0].getchildren()[0].text.lower()
                    colValue = children[1]
                    #print colName, colValue

                    if colName == 'runtime:':
                        discovered['duration'] = colValue.text

                    elif colName == 'added on:':
                        discovered['createdTs'] = dateParser.parse(colValue.text)

                    elif colName == 'description:':
                        discovered['description'] = colValue.text

                    elif colName == 'channels:':
                        discovered['categories'] = map(lambda x: x.text, colValue.getchildren())

                    elif colName == 'added by:':
                        name = colValue.getchildren()[0].getchildren()[0].text
                        print 'name=',name
                        discovered['userId'] = getOrCreateUser(name, session).id

            print discovered
            return discovered

        discovered = discoverInfo()

        video = Video(**discovered)
        logger.info('Added new video, id={0} userId={1} title="{2}"'.format(identifier, discovered['userId'], discovered['title']))

    session.add(video)
    session.commit()
#    session.close()

def gallery(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

def photo(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

def profile(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

def userGalleryListing(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

def userVideoListing(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

