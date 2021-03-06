# -*- coding: utf-8 -*-

from . import getSession #engine, Session
from .models import User, Gallery, Video
from ..wget import wget

import logging
from pyquery import PyQuery as pq
from dateutil import parser as dateParser
from datetime import datetime
import re


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

    #print 'user=',user
    return user

def video(url, identifier, extra):
    """d"""
    logger.info('identifier={0}, extra={1}'.format(identifier, extra))

    session = getSession() #Session()

    def isDeletedLocally():
        return session.query(Video).filter(Video.id==identifier).filter(Video.deleted==True).first() is not None

    if isDeletedLocally():
        logger.info('Skipping videoId={0} because it is already marked as deleted'.format(identifier))
#        session.close()
        return

    d = pq(wget(url))

    def isDeleted():
        return d('div.error').text() is not None and d('div.error').text().lower() == 'this video was deleted'

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

    def discoverInfo():
        """Scrape video info fields from HTML."""
        try:
            discovered = {
                'id': identifier,
                'title': d('h2.gr').text(),
                'description': None,
                'duration': None,
                'createdTs': None,
                'modifiedTs': datetime.now(),
                'userId': None
            }

            maybeDescription = d('div#videoInfoBox .desc').text()
            if maybeDescription is not None:
                discovered['description'] = re.sub(r'^Description:? +', '', maybeDescription.strip(), flags=re.I)

            #f = d('tr td b:nth-child(1)')#b.text:contains("^.*$")')
            for row in d('div#videoInfoBox .item'):
                text = pq(row).text().strip()
                ltext = text.lower()

                if ltext.startswith('added by'):
                    text = re.sub(r'^Added by:?\s+', '', text, flags=re.I)
                    username = text[0:text.index(' ')]
                    discovered['userId'] = getOrCreateUser(username, session).id

                    # Also grab hinted createdTs.
                    createdTs = pq(row)('span.hint').attr['hint']
                    discovered['createdTs'] = dateParser.parse(createdTs)

                elif ltext.startswith('runtime'):
                    text = re.sub(r'^Runtime:?\s+', '', text.strip(), flags=re.I)
                    discovered['duration'] = text

            discovered['categories'] = [pq(row).text() for row in d('#channels a')]

            print discovered
            assert discovered['duration'] is not None, 'Failed to parse the duration, something is probably very broken'
            assert discovered['description'] is not None, 'Failed to parse the description, something is probably somewhat broken'
            return discovered

        except Exception, e:
            print 'caught',e
            import traceback
            traceback.print_exc()
            raise e

    if video is not None:
        # Update the last modified ts.
        #video.modifiedTs = datetime.now()
        logger.info('Already knew about video id={0} userId={1} title="{2}"'.format(identifier, video.userId, video.title))
        logger.info('Refreshing info for videoId={0}'.format(video.id))

        discovered = discoverInfo()

        for k, v in discovered.items():
            setattr(video, k, v)
        session.add(video)

    else:

        # Add the video to the db.
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

