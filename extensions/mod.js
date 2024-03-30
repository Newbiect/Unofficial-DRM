(async () => {
    const b64 = {
        decode: s => Uint8Array.from(atob(s), c => c.charCodeAt(0)),
        encode: b => btoa(String.fromCharCode(...new Uint8Array(b)))
    };

    const fnproxy = (object, func) => new Proxy(object, { apply: func });

    const proxy = (object, key, func) => Object.defineProperty(object, key, {
        value: fnproxy(object[key], func)
    });

    // Proxy for requestMediaKeySystemAccess
    if (typeof Navigator !== 'undefined') {
        proxy(Navigator.prototype, 'requestMediaKeySystemAccess', async (_target, _this, _args) => {
            const [keySystem, supportedConfigurations] = _args;
            console.log(JSON.stringify({
                type: "RequestMediaKeySystemAccess",
                keySystem,
                supportedConfigurations
            }));
            return _target.apply(_this, _args);
        });
    }

    // Proxy for createMediaKeys
    if (typeof MediaKeySystemAccess !== 'undefined') {
        proxy(MediaKeySystemAccess.prototype, 'createMediaKeys', async (_target, _this, _args) => {
            console.log(JSON.stringify({
                type: "CreateMediaKeys"
            }));
            return _target.apply(_this, _args);
        });
    }

    // Proxy for setServerCertificate
    if (typeof MediaKeys !== 'undefined') {
        proxy(MediaKeys.prototype, 'setServerCertificate', async (_target, _this, _args) => {
            const [serverCertificate] = _args;
            console.log(JSON.stringify({
                type: "SetServerCertificate",
                serverCertificate
            }));
            return _target.apply(_this, _args);
        });
    }

    // Proxy for createSession
    if (typeof MediaKeys !== 'undefined') {
        proxy(MediaKeys.prototype, 'createSession', (_target, _this, _args) => {
            const [sessionType] = _args;
            console.log(JSON.stringify({
                type: "CreateSession",
                sessionType
            }));
            const session = _target.apply(_this, _args);
            return session;
        });
    }

    // Proxy for generateRequest
    if (typeof MediaKeySession !== 'undefined') {
        proxy(MediaKeySession.prototype, 'generateRequest', async (_target, _this, _args) => {
            const [initDataType, initData] = _args;
            const pssh = b64.encode(initData);
            console.groupCollapsed(
                `PSSH: ${pssh}`
            );
            console.trace();
            console.groupEnd();
            if (pssh)
                window.postMessage({ type: "38405bbb-36ef-454d-8b32-346f9564c978", log: pssh }, "*");
            return _target.apply(_this, _args);
        });
    }

    // Proxy for messageHandler
    function messageHandler(event) {
        const keySession = event.target;
        const { sessionId } = keySession;
        const { message, messageType } = event;
        const listeners = keySession.getEventListeners('message').filter(l => l !== messageHandler);
        if (messageType === 'license-request') {
            console.groupCollapsed(
                `%c[L33T] (EVENT)%c MediaKeySession::message%c\n` +
                `Session ID: %c%s%c\n` +
                `Message Type: %c%s%c\n` +
                `Message: %c%s%c\n` +
                `Listeners:`,

                `color: ${$.INFO}; font-weight: bold;`, `color: ${$.METHOD};`, `font-weight: normal;`,
                `color: ${$.VALUE}; font-weight: bold;`, sessionId || '(not available)', `color: inherit; font-weight: normal;`,
                `color: ${$.VALUE}; font-weight: bold;`, messageType, `color: inherit; font-weight: normal;`,
                `font-weight: bold;`, b64.encode(message), `font-weight: normal;`,
                listeners,
            );
            console.trace();
            console.groupEnd();
        } else {
            console.groupCollapsed(
                `%c[L33T] (EVENT)%c MediaKeySession::message%c\n` +
                `Session ID: %c%s%c\n` +
                `Message Type: %c%s%c\n` +
                `Message: %c%s%c\n` +
                `Listeners:`,

                `color: ${$.INFO}; font-weight: bold;`, `color: ${$.METHOD};`, `font-weight: normal;`,
                `color: ${$.VALUE}; font-weight: bold;`, sessionId || '(not available)', `color: inherit; font-weight: normal;`,
                `color: ${$.VALUE}; font-weight: bold;`, messageType, `color: inherit; font-weight: normal;`,
                `font-weight: bold;`, b64.encode(message), `font-weight: normal;`,
                listeners,
            );
            console.trace();
            console.groupEnd();
        }
    }

    // Attach messageHandler to message event of MediaKeySession
    if (typeof MediaKeySession !== 'undefined') {
        MediaKeySession.prototype.addEventListener('message', messageHandler);
    }
})();
