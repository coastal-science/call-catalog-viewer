/**
 * Site analytics loader with first-party opt-out.
 *
 * Cookie: analytics_opt_out=1  → do not load Google Analytics on this site.
 * Privacy page can call CallCatalogueAnalytics.optOut() / optIn().
 */
(function (global) {
  var COOKIE_NAME = 'analytics_opt_out';
  var COOKIE_MAX_AGE_SEC = 60 * 60 * 24 * 365 * 2; // 2 years
  // Primary measurement ID used by the catalogue; include legacy ID so older
  // cached pages that still reference it are also disabled when opted out.
  var MEASUREMENT_ID = 'G-NXV17QEMVJ';
  var ALL_MEASUREMENT_IDS = ['G-NXV17QEMVJ', 'G-4ZT5PMCN8Z'];

  function readCookie(name) {
    var match = document.cookie.match(
      new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)')
    );
    return match ? decodeURIComponent(match[1]) : null;
  }

  function writeCookie(name, value, maxAgeSec) {
    var secure = location.protocol === 'https:' ? '; Secure' : '';
    document.cookie =
      name +
      '=' +
      encodeURIComponent(value) +
      '; path=/' +
      '; max-age=' +
      maxAgeSec +
      '; SameSite=Lax' +
      secure;
  }

  function clearCookie(name) {
    document.cookie =
      name +
      '=; path=/; max-age=0; SameSite=Lax' +
      (location.protocol === 'https:' ? '; Secure' : '');
  }

  function isOptedOut() {
    return readCookie(COOKIE_NAME) === '1';
  }

  function setGaDisableFlags(disabled) {
    ALL_MEASUREMENT_IDS.forEach(function (id) {
      global['ga-disable-' + id] = disabled;
    });
  }

  function loadGoogleAnalytics() {
    if (global.__callCatalogueAnalyticsLoaded) {
      return;
    }
    global.__callCatalogueAnalyticsLoaded = true;

    global.dataLayer = global.dataLayer || [];
    function gtag() {
      global.dataLayer.push(arguments);
    }
    global.gtag = gtag;

    gtag('js', new Date());
    gtag('config', MEASUREMENT_ID);

    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
    document.head.appendChild(script);
  }

  function optOut() {
    writeCookie(COOKIE_NAME, '1', COOKIE_MAX_AGE_SEC);
    setGaDisableFlags(true);
  }

  function optIn() {
    clearCookie(COOKIE_NAME);
    setGaDisableFlags(false);
    loadGoogleAnalytics();
  }

  global.CallCatalogueAnalytics = {
    isOptedOut: isOptedOut,
    optOut: optOut,
    optIn: optIn,
    measurementId: MEASUREMENT_ID
  };

  if (isOptedOut()) {
    setGaDisableFlags(true);
    return;
  }

  loadGoogleAnalytics();
})(window);
