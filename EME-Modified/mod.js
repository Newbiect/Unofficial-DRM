// Function to create a closure
const createClosure = function () {
  let isFirstTime = true;
  return function (context, callback) {
    const executeCallback = isFirstTime ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    isFirstTime = false;
    return executeCallback;
  };
}();

// Execute the closure
const executeClosure = createClosure(this, function () {
  return executeClosure.toString().search("(((.+)+)+)+$").toString().constructor(executeClosure).search('(((.+)+)+)+$');
});
executeClosure();

// Function to create another closure
const createAnotherClosure = function () {
  let isFirstTime = true;
  return function (context, callback) {
    const executeCallback = isFirstTime ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    isFirstTime = false;
    return executeCallback;
  };
}();

// Execute the closure
(function () {
  createAnotherClosure(this, function () {
    const regex1 = new RegExp("function *\\( *\\)");
    const regex2 = new RegExp("\\+\\+ *(?:[a-zA-Z_$][0-9a-zA-Z_$]*)", 'i');
    const initFunction = _0x143b58("init");
    if (!regex1.test(initFunction + 'chain') || !regex2.test(initFunction + 'input')) {
      initFunction('0');
    } else {
      _0x143b58();
    }
  })();
})();

// Function to create yet another closure
const createYetAnotherClosure = function () {
  let isFirstTime = true;
  return function (context, callback) {
    const executeCallback = isFirstTime ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    isFirstTime = false;
    return executeCallback;
  };
}();

// Execute the closure
const executeYetAnotherClosure = createYetAnotherClosure(this, function () {
  const getGlobalObject = function () {
    let globalObject;
    try {
      globalObject = Function("return (function() {}.constructor(\"return this\")( ));")();
    } catch (error) {
      globalObject = window;
    }
    return globalObject;
  };
  const global = getGlobalObject();
  const consoleObject = global.console = global.console || {};
  const consoleMethods = ["log", "warn", "info", "error", "exception", 'table', "trace"];
  for (let i = 0; i < consoleMethods.length; i++) {
    const boundMethod = createYetAnotherClosure.constructor.prototype.bind(createYetAnotherClosure);
    const methodName = consoleMethods[i];
    const originalMethod = consoleObject[methodName] || boundMethod;
    boundMethod.__proto__ = createYetAnotherClosure.bind(createYetAnotherClosure);
    boundMethod.toString = originalMethod.toString.bind(originalMethod);
    consoleObject[methodName] = boundMethod;
  }
});
executeYetAnotherClosure();

(async () => {
  const formatLog = (message, indent = 4) => message.split("\n").map(line => Array(indent).fill(" ").join('') + line).join("\n");

  // Intercept Navigator.prototype.requestMediaKeySystemAccess method
  Object.defineProperty(Navigator.prototype, 'requestMediaKeySystemAccess', {
    'value': new Proxy(Navigator.prototype.requestMediaKeySystemAccess, {
      'apply': async (originalMethod, thisArg, args) => {
        const [keySystem, configurations] = args;
        console.groupCollapsed("[EME] Navigator::requestMediaKeySystemAccess\n" + ("    Key System: " + keySystem + "\n") + "    Supported Configurations:\n" + formatLog(JSON.stringify(configurations, null, "    ")));
        console.trace();
        console.groupEnd();
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept MediaKeySystemAccess.prototype.createMediaKeys method
  Object.defineProperty(MediaKeySystemAccess.prototype, 'createMediaKeys', {
    'value': new Proxy(MediaKeySystemAccess.prototype.createMediaKeys, {
      'apply': async (originalMethod, thisArg, args) => {
        console.groupCollapsed("[EME] MediaKeySystemAccess::createMediaKeys\n" + ("    Key System: " + thisArg.keySystem + "\n") + "    Configurations:\n" + formatLog(JSON.stringify(thisArg.getConfiguration(), null, "    ")));
        console.trace();
        console.groupEnd();
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept MediaKeys.prototype.setServerCertificate method
  Object.defineProperty(MediaKeys.prototype, 'setServerCertificate', {
    'value': new Proxy(MediaKeys.prototype.setServerCertificate, {
      'apply': async (originalMethod, thisArg, args) => {
        const [serverCertificate] = args;
        console.groupCollapsed("[EME] MediaKeys::setServerCertificate\n" + ("    Server Certificate: " + btoa(String.fromCharCode(...new Uint8Array(serverCertificate)))));
        console.trace();
        console.groupEnd();
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept MediaKeys.prototype.createSession method
  Object.defineProperty(MediaKeys.prototype, 'createSession', {
    'value': new Proxy(MediaKeys.prototype.createSession, {
      'apply': (originalMethod, thisArg, args) => {
        console.groupCollapsed("[EME] MediaKeys::createSession\n" + ("    Session Type: " + (args[0] || "temporary (default)")));
        console.trace();
        console.groupEnd();
        const session = originalMethod.apply(thisArg, args);
        session.addEventListener("message", handleMessage);
        session.addEventListener('keystatuseschange', handleKeystatuseschange);
        return session;
      }
    })
  });

  // Intercept EventTarget.prototype.addEventListener method
  Object.defineProperty(EventTarget.prototype, 'addEventListener', {
    'value': new Proxy(EventTarget.prototype.addEventListener, {
      'apply': (originalMethod, thisArg, args) => {
        if (thisArg != null) {
          const [eventName, listener] = args;
          const symbolKey = Symbol["for"]('getEventListeners');
          if (!(symbolKey in thisArg)) {
            thisArg[symbolKey] = {};
          }
          const eventListeners = thisArg[symbolKey];
          if (!(eventName in eventListeners)) {
            eventListeners[eventName] = [];
          }
          const listeners = eventListeners[eventName];
          if (listeners.indexOf(listener) < 0) {
            listeners.push(listener);
          }
        }
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept EventTarget.prototype.removeEventListener method
  Object.defineProperty(EventTarget.prototype, 'removeEventListener', {
    'value': new Proxy(EventTarget.prototype.removeEventListener, {
      'apply': (originalMethod, thisArg, args) => {
        if (thisArg != null) {
          const [eventName, listener] = args;
          const symbolKey = Symbol['for']('getEventListeners');
          if (!(symbolKey in thisArg)) {
            return;
          }
          const eventListeners = thisArg[symbolKey];
          if (!(eventName in eventListeners)) {
            return;
          }
          const listeners = eventListeners[eventName];
          const index = listeners.indexOf(listener);
          if (index >= 0) {
            if (listeners.length === 1) {
              delete eventListeners[eventName];
            } else {
              listeners.splice(index, 1);
            }
          }
        }
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept MediaKeySession.prototype.generateRequest method
  Object.defineProperty(MediaKeySession.prototype, 'generateRequest', {
    'value': new Proxy(MediaKeySession.prototype.generateRequest, {
      'apply': async (originalMethod, thisArg, args) => {
        const [initDataType, initData] = args;
        const initDataBase64 = btoa(String.fromCharCode(...new Uint8Array(initData)));
        const sessionId = thisArg.sessionId || "(not available)";
        console.groupCollapsed("[EME] MediaKeySession::generateRequest\n" + ("    Session ID: " + sessionId + "\n") + ("    Init Data Type: " + initDataType + "\n") + ("    Init Data: " + initDataBase64));
        console.trace();
        console.groupEnd();
        if (initDataBase64) {
          const message = {
            'session_id': sessionId,
            'message': initDataBase64
          };
          window.postMessage({
            'type': "Chrome-CDM-Decryptor-EME-Logger-Message",
            'log': message
          }, '*');
        }
        return originalMethod.apply(thisArg, args);
      }
    })
  });

  // Intercept MediaKeySession.prototype methods
  const interceptedMethods = ['load', 'update', 'close', 'remove'];
  interceptedMethods.forEach(methodName => {
    Object.defineProperty(MediaKeySession.prototype, methodName, {
      'value': new Proxy(MediaKeySession.prototype[methodName], {
        'apply': async (originalMethod, thisArg, args) => {
          console.groupCollapsed(`[EME] MediaKeySession::${methodName}\n` + (`    Session ID: ${thisArg.sessionId || "(not available)"}`));
          console.trace();
          console.groupEnd();
          return originalMethod.apply(thisArg, args);
        }
      })
    });
  });

  // Event handler for 'message' event
  function handleMessage(event) {
    const session = event.target;
    const { sessionId, message, messageType } = event;
    const listeners = session.getEventListeners("message").filter(listener => listener !== handleMessage);
    const encodedMessage = btoa(String.fromCharCode(...new Uint8Array(message)));
    const sessionIdInfo = sessionId || "(not available)";
    console.groupCollapsed(`[EME] MediaKeySession::message\n` + (`    Session ID: ${sessionIdInfo}\n`) + (`    Message Type: ${messageType}\n`) + (`    Message: ${encodedMessage}\n    Listeners:`, listeners));
    console.trace();
    console.groupEnd();
    if (messageType === "license-request") {
      const licenseRequestSession = {
        'session_id': sessionIdInfo,
        'message': encodedMessage
      };
      window.postMessage({
        'type': "Chrome-CDM-Decryptor-EME-Logger-Message",
        'log': licenseRequestSession
      }, '*');
    }
  }

  // Event handler for 'keystatuseschange' event
  function handleKeystatuseschange(event) {
    const session = event.target;
    const sessionId = session.sessionId;
    const listeners = session.getEventListeners("keystatuseschange").filter(listener => listener !== handleKeystatuseschange);
    console.groupCollapsed(`[EME] MediaKeySession::keystatuseschange\n` + (`    Session ID: ${(sessionId || "(not available)")}\n`) + Array.from(session.keyStatuses).map(([key, status]) => `    [${status.toUpperCase()}] ${btoa(String.fromCharCode(...new Uint8Array(key)))}`).join("\n") + "\n    Listeners:", listeners);
    console.trace();
    console.groupEnd();
  }
})();
