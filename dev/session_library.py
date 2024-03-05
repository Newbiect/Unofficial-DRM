import threading

class SessionLibrary:
    sSingletonLock = threading.Lock()
    sSingleton = None

    def __init__(self):
        self.mSessionsLock = threading.Lock()
        self.mNextSessionId = 0
        self.mSessions = {}

    @staticmethod
    def get():
        with SessionLibrary.sSingletonLock:
            if SessionLibrary.sSingleton is None:
                print("Instantiating Session Library Singleton.")
                SessionLibrary.sSingleton = SessionLibrary()
        return SessionLibrary.sSingleton

    def createSession(self):
        with self.mSessionsLock:
            sessionIdRaw = str(self.mNextSessionId).encode()
            self.mNextSessionId += 1
            sessionId = list(sessionIdRaw)
            self.mSessions[sessionId] = Session(sessionId)
            if sessionId in self.mSessions:
                return self.mSessions[sessionId]
            else:
                return None

    def findSession(self, sessionId):
        with self.mSessionsLock:
            if sessionId in self.mSessions:
                return self.mSessions[sessionId]
            else:
                return None

    def destroySession(self, session):
        with self.mSessionsLock:
            if session.sessionId() in self.mSessions:
                del self.mSessions[session.sessionId()]

class Session:
    def __init__(self, sessionId):
        self.sessionId = sessionId