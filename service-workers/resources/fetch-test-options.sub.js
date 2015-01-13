var BASE_ORIGIN = 'http://{{domains[www]}}:{{ports[http][0]}}';
var OTHER_ORIGIN = 'http://{{host}}:{{ports[http][0]}}';
var TEST_OPTIONS = '';
// TEST_OPTIONS is '', '-other-https', '-base-https', or
// '-base-https-other-https'.

if (location.href.indexOf('base-https') >= 0) {
  BASE_ORIGIN = 'https://{{domains[www]}}:8443';
  TEST_OPTIONS += '-base-https';
}

if (location.href.indexOf('other-https') >= 0) {
  OTHER_ORIGIN = 'https://{{host}}:8443';
  TEST_OPTIONS += '-other-https';
}
