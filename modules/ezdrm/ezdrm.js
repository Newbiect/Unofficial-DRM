<script src="https://cdn.radiantmediatechs.com/rmp/6.4.12/js/rmp.min.js"></script>
<div id="rmpPlayer"></div>
<script>
  // DASH streaming URL
  var src = {
    dash: 'https://your‐dash‐url.mpd'
  };
  // EZDRM license server for PlayReady
  var playReadyLaURL = 'https://playready.ezdrm.com/cency/preauth.aspx?pX=XXXXXX';  
  // EZDRM license server for Widevine
  var widevineLaURL = 'https://widevine‐dash.ezdrm.com/proxy?pX=XXXXXX';  
  // create Radiant Media Player instance
  var elementID = 'rmpPlayer';
  var rmp = new RadiantMP(elementID);
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
    // here we pass our EZDRM DRM data
    shakaDrm: {
      servers: {
        "com.widevine.alpha": widevineLaURL,
        "com.microsoft.playready": playReadyLaURL
      }
    }
  };
  rmp.init(settings);
</script>
