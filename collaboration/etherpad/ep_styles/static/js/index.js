var _, $, jQuery;

var $ = require('ep_etherpad-lite/static/js/rjquery').$;
var _ = require('ep_etherpad-lite/static/js/underscore');
var cssFiles = ['ep_styles/static/css/editor.css'];

// Bind the event handler to the toolbar buttons
var postAceInit = function(hook, context){
  var hs = $('#custom-style-selection');
  hs.on('change', function(){
    var value = $(this).val();
    //var intValue = parseInt(value,10);
    if(value && value.indexOf("style") === 0){
      context.ace.callWithAce(function(ace){
        ace.ace_doInsertStyles(value);
      },'insertStyle' , true);
      hs.val("default");
    }
  })
};

// Our colors attribute will result in a heaading:h1... :h6 class
function aceAttribsToClasses(hook, context){
  if(context.key == 'styles'){
    return ['styles:' + context.value ];
  }
}


// Here we convert the class colors:h1 into a tag
function aceCreateDomLine(name, context){
  var cls = context.cls;
  var domline = context.domline;
  var stylesType = /(?:^| )styles:([A-Za-z0-9]*)/.exec(cls);
  var style;
  if (stylesType) style = stylesType[1];

      
  if (style !== undefined && style.indexOf("style") === 0){
      console.log('STYLE: ' + style);  
      
    var modifier = {
      extraOpenTags: '<span class="' + style + '">',
      extraCloseTags: '</span>',
      cls: cls
    };
    console.log(cls);
    return [modifier];
  }
  return [];
};



// Find out which lines are selected and assign them the colors attribute.
// Passing a level >= 0 will set a colors on the selected lines, level < 0 
// will remove it
function doInsertStyles(style){
  var rep = this.rep,
    documentAttributeManager = this.documentAttributeManager;
  if (!(rep.selStart && rep.selEnd) || (style === undefined))
  {
    return;
  }
  
    if(style != "style0"){
          documentAttributeManager.setAttributesOnRange(rep.selStart, rep.selEnd, [
                ['styles', style]
          ]);
    }else{
        documentAttributeManager.setAttributesOnRange(rep.selStart, rep.selEnd, [
                    ['styles', '']
              ]);
    }
}


// Once ace is initialized, we set ace_doInsertColors and bind it to the context
function aceInitialized(hook, context){
  var editorInfo = context.editorInfo;
  editorInfo.ace_doInsertStyles = _(doInsertStyles).bind(context);
}

function aceEditorCSS(){
  return cssFiles;
};

// Export all hooks
exports.postAceInit = postAceInit;
exports.aceInitialized = aceInitialized;
exports.aceCreateDomLine = aceCreateDomLine;
exports.aceAttribsToClasses = aceAttribsToClasses;
exports.aceEditorCSS = aceEditorCSS;
