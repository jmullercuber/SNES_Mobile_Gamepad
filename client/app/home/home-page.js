var frameModule = require("ui/frame");
var dialogsModule = require("ui/dialogs");
var HomeViewModel = require("./home-view-model");
var homeViewModel = new HomeViewModel();

exports.pageLoaded = function (args) {
  var page = args.object;
  page.bindingContext = homeViewModel;
  page.actionBarHidden = true;
  homeViewModel.onPageLoad()
};
