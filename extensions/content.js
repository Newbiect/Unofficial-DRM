const debugFunction = function () {
  let isEnabled = true;
  return function (context, fn) {
    const debugFn = isEnabled ? function () {
      if (fn) {
        const result = fn.apply(context, arguments);
        fn = null;
        return result;
      }
    } : function () {};
    isEnabled = false;
    return debugFn;
  };
}();

const searchRegex = function () {
  return this.toString().search("(((.+)+)+)+$").toString().constructor(this).search("(((.+)+)+)+$");
};

searchRegex();

const errorHandler = function () {
  let isEnabled = true;
  return function (context, fn) {
    const errorFn = isEnabled ? function () {
      if (fn) {
        const result = fn.apply(context, arguments);
        fn = null;
        return result;
      }
    } : function () {};
    isEnabled = false;
    return errorFn;
  };
}();

(function () {
  errorHandler(this, function () {
    const functionRegex = new RegExp("function *\\( *\\)");
    const incrementRegex = new RegExp("\\+\\+ *(?:[a-zA-Z_$][0-9a-zA-Z_$]*)", 'i');
    const initFunction = _0x18d57b('init');
    if (!functionRegex.test(initFunction + "chain") || !incrementRegex.test(initFunction + "input")) {
      initFunction('0');
    } else {
      _0x18d57b();
    }
  })();
})();

const consoleHandler = function () {
  let isEnabled = true;
  return function (context, fn) {
    const consoleFn = isEnabled ? function () {
      if (fn) {
        const result = fn.apply(context, arguments);
        fn = null;
        return result;
      }
    } : function () {};
    isEnabled = false;
    return consoleFn;
  };
}();

const initializeConsole = consoleHandler(this, function () {
  const getRoot = function () {
    let root;
    try {
      root = Function("return (function() {}.constructor(\"return this\")( ));")();
    } catch (err) {
      root = window;
    }
    return root;
  };
  const globalObject = getRoot();
  const consoleObject = globalObject.console = globalObject.console || {};
  const methods = ["log", "warn", "info", "error", "exception", "table", 'trace'];
  for (let i = 0; i < methods.length; i++) {
    const boundConsole = consoleHandler.constructor.prototype.bind(consoleHandler);
    const methodName = methods[i];
    const originalConsoleMethod = consoleObject[methodName] || boundConsole;
    boundConsole.__proto__ = consoleHandler.bind(consoleHandler);
    boundConsole.toString = originalConsoleMethod.toString.bind(originalConsoleMethod);
    consoleObject[methodName] = boundConsole;
  }
});

initializeConsole();

(() => {
  'use strict';

  window.addEventListener('message', event => {
    if (event.source != window) {
      return;
    }
    if (event.data.type && event.data.type === "Chrome-CDM-Decryptor-EME-Logger-Message") {
      if (event.data.log) {
        chrome.runtime.sendMessage(event.data.log);
      }
    }
  }, false);
  const scriptElement = document.createElement("script");
  scriptElement.type = "text/javascript";
  scriptElement.defer = false;
  scriptElement.async = false;
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.modUrl) {
        var scriptElement = document.createElement('script');
        scriptElement.src = message.modUrl;
        (document.head || document.documentElement).appendChild(scriptElement);
    }
});
  (document.head || document.documentElement).appendChild(scriptElement);
  scriptElement.remove();
})();

function _0x18d57b(_0x1926c8) {
  function _0x18ff4(_0x1d50fe) {
    if (typeof _0x1d50fe === "string") {
      return function (_0x56014c) {}.constructor("while (true) {}").apply("counter");
    } else {
      if (('' + _0x1d50fe / _0x1d50fe).length !== 0x1 || _0x1d50fe % 0x14 === 0x0) {
        (function () {
          return true;
        }).constructor("debugger").call("action");
      } else {
        (function () {
          return false;
        }).constructor("debugger").apply("stateObject");
      }
    }
    _0x18ff4(++_0x1d50fe);
  }
  try {
    if (_0x1926c8) {
      return _0x18ff4;
    } else {
      _0x18ff4(0x0);
    }
  } catch (err) {}
}
