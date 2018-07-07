var frame = require("ui/frame");
var observableModule = require("data/observable");

const httpModule = require("http");

var baseUrl = "http://10.0.0.21:5000/webhook"
// token keeps changing yo
var token = '59a589d6aa1bb31e9da886adffb6fbbff1fb6322f52f5a61'

factory = function (btn) {
  return function (e) {
    // ignore move actions. We only care about up and down atm
    if (e.action == 'move') {
      return
    }
    value = (e.action != 'up')*1
    console.log(btn, value);
    data = {}
    data['cid'] = 0
    data[btn] = value
    return fetch(baseUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    }).then(handleErrors)
  }
};

function HomeViewModel() {
  var viewModel = observableModule.fromObject({

    onButtonTouch_A: factory('A'),
    onButtonTouch_B: factory('B'),
    onButtonTouch_X: factory('X'),
    onButtonTouch_Y: factory('Y'),
    onButtonTouch_TL: factory('TL'),
    onButtonTouch_TR: factory('TR'),
    onButtonTouch_START: factory('START'),
    onButtonTouch_SELECT: factory('SELECT'),
    onButtonTouch_UP: factory('UP'),
    onButtonTouch_DOWN: factory('DOWN'),
    onButtonTouch_LEFT: factory('LEFT'),
    onButtonTouch_RIGHT: factory('RIGHT'),

    onOpenDrawerTap: function () {
        var sideDrawer = frame.topmost().getViewById("sideDrawer");
        sideDrawer.showDrawer();
        console.log('opened drawer')
    },
    onCloseDrawerTap: function () {
        var sideDrawer = frame.topmost().getViewById("sideDrawer");
        sideDrawer.closeDrawer();
    },
    onPageLoad: function () {
      console.log('Page loading brah')
      return httpModule.request({
        url: baseUrl + '?verify_token=' + token,
        method: "GET"
      }).then((response) => {
        // Argument (response) is HttpResponse
        console.log('Response status is', response.content.toJSON().status, response.statusCode)
      }, (e) => {
      }).then(handleErrors);
    },
      
  });

  return viewModel;
}

function handleErrors(response) {
  if (!response.ok) {
    console.log(JSON.stringify(response));
    throw Error(response.statusText);
  }
  return response;
}

module.exports = HomeViewModel;
