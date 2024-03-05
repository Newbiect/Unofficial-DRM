import logging
from threading import Lock
from collections import defaultdict

class SESSION:
    def __init__(self, session_id):
        self.session_id = session_id

class SessionLibrary:
    sSingletonLock = Lock()
    sSingleton = None

    def __init__(self):
        self.mNextSessionId = 0
        self.mSessionsLock = Lock()
        self.mSessions = defaultdict(Session)

    @classmethod
    def get(cls):
        with cls.sSingletonLock:
            if cls.sSingleton is None:
                logging.debug("Instantiating Session Library Singleton.")
                cls.sSingleton = cls()
        return cls.sSingleton

    def createSession(self):
        with self.mSessionsLock:
            sessionIdString = str(self.mNextSessionId)
            self.mNextSessionId += 1
            sessionId = [ord(c) for c in sessionIdString]
            self.mSessions[tuple(sessionId)] = Session(sessionId)
            return self.mSessions[tuple(sessionId)]

    def findSession(self, sessionId):
        with self.mSessionsLock:
            if tuple(sessionId) not in self.mSessions:
                return None
            return self.mSessions[tuple(sessionId)]

    def destroySession(self, session):
        with self.mSessionsLock:
            del self.mSessions[tuple(session.session_id)]
