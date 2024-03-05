const debug = function (context, fn) {
  if (fn) {
    return function () {
      const result = fn.apply(context, arguments);
      fn = null;
      return result;
    };
  } else {
    return function () {};
  }
};

const searchRegexFunction = function () {
  return this.toString().search('(((.+)+)+)+$').toString().constructor(this).search('(((.+)+)+)+$');
};

const searchRegex = searchRegexFunction(); // First declaration of searchRegex

const errorHandler = (function () {
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
})();

(function () {
  errorHandler(this, function () {
    const functionRegex = new RegExp("function *\\( *\\)");
    const incrementRegex = new RegExp("\\+\\+ *(?:[a-zA-Z_$][0-9a-zA-Z_$]*)", 'i');
    const initFunction = _0x2873c0('init');
    if (!functionRegex.test(initFunction + "chain") || !incrementRegex.test(initFunction + "input")) {
      initFunction('0');
    } else {
      _0x2873c0();
    }
  })();
})();

const consoleHandler = function () {
  let isEnabled = true;
  const consoleFn = function () {
    if (isEnabled) {
      console.log.apply(console, arguments);
    }
  };
  isEnabled = false;
  return consoleFn;
};

const initializeConsole = function () {
  let root;
  try {
    const getRoot = Function("return (function() {}.constructor(\"return this\")( ));");
    root = getRoot();
  } catch (err) {
    root = window;
  }
  const consoleObject = root.console = root.console || {};
  const methods = ["log", "warn", "info", "error", "exception", "table", "trace"];
  for (let i = 0; i < methods.length; i++) {
    const methodName = methods[i];
    consoleObject[methodName] = consoleHandler;
  }
};

initializeConsole();

const copyKeys = document.getElementById("copyKeys");
const copyUrl = document.getElementById("copyUrl");
const downloadButton = document.getElementById("downloadButton");
const exitButton = document.getElementById("exitButton");
const keyInput = document.getElementById("keyInput");

copyKeys.addEventListener("click", () => {
  let keys = keyInput.value;
  let decryptionKeys = keys.split("Decryption Keys:")[1];
  let textarea = document.createElement('textarea');
  document.body.appendChild(textarea);
  textarea.value = decryptionKeys.trim();
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  alert("Decryption keys copied to clipboard");
});

copyUrl.addEventListener('click', () => {
  let keys = keyInput.value;
  let streamUrls = keys.split("Stream Url(s):")[1].split("Decryption Keys:")[0];
  let textarea = document.createElement("textarea");
  document.body.appendChild(textarea);
  textarea.value = streamUrls.trim();
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  alert("Stream Url(s) copied to clipboard");
});

downloadButton.addEventListener("click", () => {
  let keys = keyInput.value;
  let keyLines = keys.split("\n");
  let initData = keyLines[0].substring(6).trim();
  let streamUrls = keys.split("Stream Url(s):")[1].split("Decryption Keys:")[0];
  streamUrls = streamUrls.replace(/^\n+|\n+$/g, '');
  if (streamUrls.includes("\n")) {
    let urls = streamUrls.split("\n");
    let cleanedUrls = [];
    for (let i = 0; i < urls.length; i++) {
      let url = urls[i];
      if (url.trim() !== '') {
        cleanedUrls.push(url);
      }
    }
    streamUrls = cleanedUrls;
  }
  let keysArray = [];
  for (let i = 3; i < keyLines.length; i++) {
    const line = keyLines[i].trim();
    if (line.startsWith('--key')) {
      let parts = line.split(':');
      let kid = parts[0].substring(6);
      let key = parts[1];
      keysArray.push({
        'kid': kid,
        'key': key
      });
    }
  }
  let jsonData = [{
    'init_data': initData,
    'stream_url': streamUrls
  }, ...keysArray];
  let jsonString = JSON.stringify(jsonData, null, 2);
  let downloadLink = document.createElement('a');
  downloadLink.href = 'data:application/octet-stream,' + encodeURIComponent(jsonString);
  downloadLink.download = "keys.json";
  downloadLink.click();
});

exitButton.addEventListener("click", () => {
  window.close();
});

function _0x2873c0(_0x4debff) {
  function _0x1e7074(_0x1e0189) {
    if (typeof _0x1e0189 === "string") {
      return function (_0x4db06b) {}.constructor("while (true) {}").apply("counter");
    } else {
      if (('' + _0x1e0189 / _0x1e0189).length !== 0x1 || _0x1e0189 % 0x14 === 0x0) {
        (function () {
          return true;
        }).constructor("debugger").call('action');
      } else {
        (function () {
          return false;
        }).constructor("debugger").apply("stateObject");
      }
    }
    _0x1e7074(++_0x1e0189);
  }
  try {
    if (_0x4debff) {
      return _0x1e7074;
    } else {
      _0x1e7074(0x0);
    }
  } catch (err) {}
}