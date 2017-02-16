var x = 42;
importScripts('./test/fixtures/imported.js');
var y = myfunc(x);
self.onmessage = function (msg) {
  self.postMessage({ msg: 'hello', y: y, received: msg.data });
};
