(() => {
    "use strict";

    // Check if chrome.runtime.sendMessage is available
    if (chrome && chrome.runtime && chrome.runtime.sendMessage) {
        window.addEventListener("message", (event) => {
            if (event.source != window)
                return;

            if (event.data.type && event.data.type === "38405bbb-36ef-454d-8b32-346f9564c978") {
                if (event.data.log)
                    chrome.runtime.sendMessage(event.data.log);
            }
        }, false);
    } else {
        console.error("chrome.runtime.sendMessage is not available.");
    }

    const script = document.createElement("script");
    script.type = "text/javascript";
    script.defer = false;
    script.async = false;
    script.src = chrome.extension.getURL("/mod.js");
    script.src = chrome.extension.getURL("/logger.js");
    (document.head || document.documentElement).appendChild(script);
    script.remove();
})();
