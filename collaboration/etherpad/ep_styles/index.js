var eejs = require('ep_etherpad-lite/node/eejs/');
var Changeset = require("ep_etherpad-lite/static/js/Changeset");

function eejsBlock_editbarMenuLeft(hook_name, args, cb) {
  args.content = args.content + eejs.require("ep_styles/templates/editbarButtons.ejs");
  return cb();
}

// line, apool,attribLine,text
function getLineHTMLForExport(hook, context) {
  var styleClass = _analyzeLine(context.attribLine, context.apool);
  if (styleClass) {
    return "<span class=\"" + styleClass + "\">" + context.text + "</span>";
  }
}

function _analyzeLine(alineAttrs, apool) {
  var header = null;
  if (alineAttrs) {
    var opIter = Changeset.opIterator(alineAttrs);
    if (opIter.hasNext()) {
      var op = opIter.next();
      header = Changeset.opAttributeValue(op, 'styles', apool);
    }
  }
  return header;
}

exports.eejsBlock_editbarMenuLeft = eejsBlock_editbarMenuLeft;
exports.getLineHTMLForExport = getLineHTMLForExport;