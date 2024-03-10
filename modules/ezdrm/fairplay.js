// Apple FairPlay DRM for HLS
// Apple FairPlay requires 3 values.
// 1. The .m3u8 URL
// 2. The license_url
// The base license_url is
// https://fps.ezdrm.com/api/licenses/<<ASSET-ID>>
// 3. The FPS cert URL
// This is the .cer file provided by Apple. This URL should be either on your Website or CDN. 

<script src="https://cdn.radiantmediatechs.com/rmp/6.4.12/js/rmp.min.js"></script>
<div id="rmpPlayer"></div>
<script>
  var src = {
    fps: '<<HTTPS LOCATION OF YOUR M3U8 FILE>>'
  };
  // we define our functions and variables to be passed to the player
  // this is specific to FairPlay streaming with EZDRM
  // extractContentId
  var extractContentId = function (initData) {
    var arrayToString = function (array) {
    var uint16array = new Uint16Array(array.buffer);
      return String.fromCharCode.apply(null, uint16array);
    };
    var uri = arrayToString(initData);
    var uriParts = uri.split('://', 1);
    var protocol = uriParts[0].slice(‐3);
    uriParts = uri.split(';', 2);
    var contentId = uriParts.length > 1 ? uriParts[1] : '';
    return protocol.toLowerCase() == 'skd' ? contentId : '';
  };
  // licenseRequestMessage
  var licenseRequestMessage = function (message) {
    return new Blob([message], { type: 'application/octet‐binary' });
  };
  // licenseRequestLoaded
  var licenseRequestLoaded = function (event) {
    var request = event.target;
    if (request.status == 200) {
      var blob = request.response;
      var reader = new FileReader();
            reader.addEventListener('loadend', function () {
        var array = new Uint8Array(reader.result);
        request.session.update(array);
      });
      reader.readAsArrayBuffer(blob);
    }
  };
  // processSpcPath
  var processSpcPath = 'https://fps.ezdrm.com/api/licenses/<<ASSET‐ID>>' + '?p1=' + Date.now();
  // licenseRequestHeaders
  var licenseRequestHeaders = [
    {
      name: 'Content‐type',
      value: 'application/octet‐stream'
    }
  ];
  var settings = {
    licenseKey: 'your‐Radiant‐license‐key',
    src: src,
    width: 640,
    height: 360,
    contentMetadata: {
      poster: [
        'https://your‐poster‐url.jpg'
      ]
    },
    // we pass here our FPS setting through fpsDrm object
    fpsDrm: {
      certificatePath: '<<HTTPS LOCATION OF YOUR CERTIFICATE>>',
      processSpcPath: processSpcPath,
      licenseResponseType: 'blob',
      licenseRequestHeaders: licenseRequestHeaders,
      certificateRequestHeaders: [],
      extractContentId: extractContentId,
      licenseRequestMessage: licenseRequestMessage,
      licenseRequestLoaded: licenseRequestLoaded
    }
  };
  var elementID = 'rmpPlayer';
  var rmp = new RadiantMP(elementID);
  rmp.init(settings);
</script>
