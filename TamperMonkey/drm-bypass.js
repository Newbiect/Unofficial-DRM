// ==UserScript==
// @name         DRM Bypass
// @author       Pari Malam
// @version      2.4
// @description  Simulates a fault(Fake) page cast to bypass Google's Digital Rights Management Block, allowing you to Record or Screenshot a website no matters its Security Policy/DRM.
// @match        https://www.netflix.com/*
// @match        https://www.hulu.com/*
// @match        https://www.crunchyroll.com/*
// @match        https://www.youtube.com/*
// @match        https://www.hbomax.com/*
// @match        https://www.showtime.com/*
// @match        https://www.vudu.com/*
// @icon         https://i.pinimg.com/originals/9e/d8/61/9ed86194c90b60ad5ce0e14fdb1b97d5.png
// @grant        window.focus
// ==/UserScript==

// Press ALT+C To Start Screen Cap
// Select Window & Click the one with your Movie/Show/Video
// Hide the notification at the bottom
// Use a recorder (OBS Recommended) or screenshot software with no BlackScreen

(function() {
    "use strict";

    if (!localStorage.getItem("firstTime")) localStorage.setItem("firstTime", "true");

    if (localStorage.getItem("firstTime") === "true") {
        alert("\nThis script will fake a capture to fool Chromium into thinking that we are casting.\nPress Alt+C after this alert, select your browser in the Window tab, and you should be able to screen record and screenshot Netflix.\nEnjoy :)");
        localStorage.setItem("firstTime", "false");
    }

    const videoElement = document.createElement("video");
    let capturing = false;

    document.onkeydown = function(event) {
        if (event.altKey && event.keyCode === 67 && capturing) {
            capturing = false;
            videoElement.getTracks().forEach(track => track.stop());
            return;
        }

        if (event.altKey && event.keyCode === 67) {
            startCapture(stream => {
                capturing = true;
                console.log(capturing);
                videoElement.srcObject = stream;
            });
            return;
        }
    };

    function startCapture(callback, errorCallback) {
        if (navigator.mediaDevices.getDisplayMedia) {
            navigator.mediaDevices.getDisplayMedia({ video: true }).then(callback).catch(errorCallback);
        } else if (navigator.getDisplayMedia) {
            navigator.getDisplayMedia({ video: true }).then(callback).catch(errorCallback);
        }
    }
})();
