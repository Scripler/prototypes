var _ = require('ep_etherpad-lite/static/js/underscore');

var collectContentPre = function(hook, context){
  var tname = context.tname;
  var state = context.state;
  var lineAttributes = state.lineAttributes

  if(tname.indexOf("style") === 0){
    lineAttributes['styles'] = tname;
  }
};

var collectContentPost = function(hook, context){
  var tname = context.tname;
  var state = context.state;
  var lineAttributes = state.lineAttributes

  if(tname.indexOf("style") === 0){
    delete lineAttributes['styles'];
  }
};

exports.collectContentPre = collectContentPre;
exports.collectContentPost = collectContentPost;
