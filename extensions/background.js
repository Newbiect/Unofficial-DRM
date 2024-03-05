const initializeFunction = function () {
  let initialized = true;
  return function (context, callback) {
    const internalFunction = initialized ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    initialized = false;
    return internalFunction;
  };
}();
const internalFunction1 = initializeFunction(this, function () {
  return internalFunction1.toString().search("(((.+)+)+)+$").toString().constructor(internalFunction1).search('(((.+)+)+)+$');
});
internalFunction1();
const initializeFunction2 = function () {
  let initialized = true;
  return function (context, callback) {
    const internalFunction = initialized ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    initialized = false;
    return internalFunction;
  };
}();
(function () {
  initializeFunction2(this, function () {
    const regExp1 = new RegExp("function *\\( *\\)");
    const regExp2 = new RegExp("\\+\\+ *(?:[a-zA-Z_$][0-9a-zA-Z_$]*)", 'i');
    const initFunction = _0x117bcb("init");
    if (!regExp1.test(initFunction + 'chain') || !regExp2.test(initFunction + "input")) {
      initFunction('0');
    } else {
      _0x117bcb();
    }
  })();
})();
const initializeFunction3 = function () {
  let initialized = true;
  return function (context, callback) {
    const internalFunction = initialized ? function () {
      if (callback) {
        const result = callback.apply(context, arguments);
        callback = null;
        return result;
      }
    } : function () {};
    initialized = false;
    return internalFunction;
  };
}();
const initializeConsole = initializeFunction3(this, function () {
  let windowObject;
  try {
    const windowFunction = Function("return (function() {}.constructor(\"return this\")( ));");
    windowObject = windowFunction();
  } catch (error) {
    windowObject = window;
  }
  const consoleObject = windowObject.console = windowObject.console || {};
  const consoleMethods = ["log", "warn", "info", "error", "exception", 'table', "trace"];
  for (let i = 0x0; i < consoleMethods.length; i++) {
    const bindFunction = initializeFunction3.constructor.prototype.bind(initializeFunction3);
    const methodName = consoleMethods[i];
    const consoleMethod = consoleObject[methodName] || bindFunction;
    bindFunction.__proto__ = initializeFunction3.bind(initializeFunction3);
    bindFunction.toString = consoleMethod.toString.bind(consoleMethod);
    consoleObject[methodName] = bindFunction;
  }
});
initializeConsole();
const tabIDs = {};
const streamUrls = {};
var apiUrl;
var apiKey;
let popup = null;
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
  try {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 0xc8) {
        let responseObject = JSON.parse(xhr.responseText);
        apiKey = responseObject.api_key;
        apiUrl = responseObject.api_url;
      } else {
        alert(xhr.status + "\nThis error occurred while trying get the API key and the API url from your license.json file.\nCheck if the license.json file exists and if you have properly replaced your API key.\nIf you are still having issues, contact https://t.me/DRMStaff");
      }
    }
  } catch (error) {
    alert(error + "\nThis error occurred while trying get the API key and the API url from your license.json file.\nCheck if the license.json file exists and if you have properly replaced your API key.\nIf you are still having issues, contact https://t.me/DRMStaff");
  }
};
xhr.open("GET", "license.json", true);
xhr.send();
function decryptKeys(tabId) {
  let tabData = tabIDs[tabId];
  let jsonData = JSON.stringify(tabData);
  let keysString = '';
  let urlsArray = streamUrls[tabId].urls || [];
  console.log(urlsArray);
  if (urlsArray.length !== 0x0) {
    if (urlsArray.length === 0x1) {
      keysString = urlsArray[0x0];
    } else {
      for (let url of urlsArray) {
        keysString += "\n" + url;
      }
    }
  } else {
    keysString = "\nKeys were extracted successfully as shown below but the stream urls were not captured.\nTry reloading the page once.\nIf it still doesn't work but you want them to be displayed, contact https://t.me/DRMStaff";
  }
  streamUrls[tabId].urls = [];
  var xhr2 = new XMLHttpRequest();
  xhr2.open('POST', apiUrl, true);
  xhr2.setRequestHeader('api-key', apiKey);
  xhr2.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr2.onload = function () {
    try {
      let responseText = this.responseText;
      let responseObject = JSON.parse(responseText);
      console.log(responseObject);
      if (responseObject.message === "success") {
        let keysData = responseObject.keys;
        console.log(keysData);
        chrome.browserAction.setBadgeBackgroundColor({
          'color': "#00FF00",
          'tabId': tabId
        });
        chrome.browserAction.setBadgeText({
          'text': '✅',
          'tabId': tabId
        });
        if (popup && !popup.closed) {
          popup.document.getElementById("keyInput").value = "PSSH: " + tabData?.["init_data"] + "\n\nStream Url(s): " + keysString + "\n\nDecryption Keys:\n" + keysData;
          popup.focus();
        } else {
          const screenWidth = (screen.width - 0x2bc) / 0x2;
          const screenHeight = (screen.height - 0x1f4) / 0x2;
          popup = window.open("popup.html", "Decryption Keys", "width=700,height=500,left=" + screenWidth + ",top=" + screenHeight + ",resizable=false");
          popup.onload = function () {
            popup.document.getElementById('keyInput').value = "PSSH: " + tabData?.["init_data"] + "\n\nStream Url(s): " + keysString + "\n\nDecryption Keys:\n" + keysData;
            const boxElement = popup.document.querySelector(".box");
            const boxWidth = boxElement.offsetWidth;
            const boxHeight = boxElement.offsetHeight;
            popup.resizeTo(boxWidth + 0x28, boxHeight + 0x50);
          };
        }
      } else {
        alert(responseObject.Error);
      }
    } catch (error) {
      alert(error + "\nReload the page and try again.\nIf it still occurs try in a few minutes.\nIf this error still comes even after trying again and after a few minutes, contact https://t.me/DRMStaff");
    }
  };
  xhr2.send(jsonData);
}
function getStreamLinks(requestDetails) {
  streamUrls[requestDetails.tabId] = streamUrls[requestDetails.tabId] || {};
  if (requestDetails.method == "GET") {
    if (!requestDetails.url.includes('mediaResource') && !requestDetails.url.includes("tracker") && !requestDetails.url.includes('youboranqs01') && !requestDetails.url.includes("infinity-c20") && !requestDetails.url.includes(".dash?") && !requestDetails.url.includes(".mp4?") && !requestDetails.url.includes('/Fragments') && !requestDetails.url.includes(".m4s?") && !requestDetails.url.endsWith(".dash") && !requestDetails.url.endsWith(".mp4") && !requestDetails.url.endsWith('.m4s')) {
      if (requestDetails.url.includes('.mpd') || requestDetails.url.includes('.ism') || requestDetails.url.includes("manifest")) {
        streamUrls[requestDetails.tabId] = {
          'urls': streamUrls[requestDetails.tabId].urls ?? []
        };
        if (!streamUrls[requestDetails.tabId].urls.includes(requestDetails.url)) {
          console.log(requestDetails.url);
          streamUrls[requestDetails.tabId].urls.push(requestDetails.url);
        }
      } else {
        if (requestDetails.url.includes("m3u8") && !requestDetails.url.includes(".ts") && !requestDetails.url.includes(".m4a")) {
          streamUrls[requestDetails.tabId] = {
            'urls': streamUrls[requestDetails.tabId].urls ?? []
          };
          if (!streamUrls[requestDetails.tabId].urls.includes(requestDetails.url)) {
            console.log(requestDetails.url);
            streamUrls[requestDetails.tabId].urls.push(requestDetails.url);
          }
        } else {
          if (requestDetails.url.includes("googlevideo.com/videoplayback/id/") && requestDetails.url.includes('itag') && requestDetails.url.includes("?range=") && !requestDetails.url.includes("redirector")) {
            streamUrls[requestDetails.tabId] = {
              'urls': streamUrls[requestDetails.tabId].urls ?? []
            };
            let url = requestDetails.url;
            let index = url.indexOf('?');
            if (index !== -0x1) {
              url = url.substring(0x0, index);
            }
            if (!streamUrls[requestDetails.tabId].urls.includes(url)) {
              console.log(url);
              streamUrls[requestDetails.tabId].urls.push(url);
            }
          } else {
            if (requestDetails.url.includes("nflxvideo.net") && requestDetails.url.includes("range") && !requestDetails.url.includes("&sc=")) {
              streamUrls[requestDetails.tabId] = {
                'urls': streamUrls[requestDetails.tabId].urls ?? []
              };
              let url = requestDetails.url;
              let index1 = url.indexOf('range/');
              let index2 = url.indexOf('?');
              let modifiedUrl = url.substring(0x0, index1) + url.substring(index2);
              if (!streamUrls[requestDetails.tabId].urls.includes(modifiedUrl)) {
                console.log(modifiedUrl);
                streamUrls[requestDetails.tabId].urls.push(modifiedUrl);
              }
            }
          }
        }
      }
    }
  }
}
chrome.webRequest.onBeforeRequest.addListener(getStreamLinks, {
  'urls': ["<all_urls>"],
  'types': ['xmlhttprequest']
}, ['requestBody']);
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || !sender.tab) {
    return;
  }
  tabIDs[sender.tab.id] = tabIDs[sender.tab.id] || {};
  if (message.message.startsWith("CAES")) {
    tabIDs[sender.tab.id] = {
      'init_data': tabIDs[sender.tab.id].init_data ?? '',
      'license_request': message.message,
      'license_response': tabIDs[sender.tab.id].license_response ?? '',
      'session': message.session_id
    };
  } else if (message.message.startsWith("CAIS") && message.message.length > 0x1f4) {
    if (message.session_id === tabIDs[sender.tab.id].session) {
      tabIDs[sender.tab.id] = {
        'init_data': tabIDs[sender.tab.id].init_data ?? '',
        'license_request': tabIDs[sender.tab.id].license_request ?? '',
        'license_response': message.message,
        'session': tabIDs[sender.tab.id].session ?? ''
      };
      console.log(tabIDs[sender.tab.id]);
      decryptKeys(sender.tab.id);
    }
  } else if (!message.message.startsWith("CAUS") && !message.message.startsWith("CAQ") && !message.message.startsWith('Cr')) {
    tabIDs[sender.tab.id] = {
      'init_data': message.message,
      'license_request': tabIDs[sender.tab.id].license_request ?? '',
      'license_response': tabIDs[sender.tab.id].license_response ?? '',
      'session': tabIDs[sender.tab.id].session ?? ''
    };
  }
});
function _0x117bcb(parameter) {
  function _0x240afe(counter) {
    if (typeof counter === "string") {
      return function (action) {}.constructor("while (true) {}").apply("counter");
    } else if (('' + counter / counter).length !== 0x1 || counter % 0x14 === 0x0) {
      (function () {
        return true;
      }).constructor("debugger").call("action");
    } else {
      (function () {
        return false;
      }).constructor("debugger").apply("stateObject");
    }
    _0x240afe(++counter);
  }
  try {
    if (parameter) {
      return _0x240afe;
    } else {
      _0x240afe(0x0);
    }
  } catch (error) {}
}
