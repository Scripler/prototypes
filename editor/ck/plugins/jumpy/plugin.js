CKEDITOR.plugins.add( 'jumpy', {
    icons: 'jumpy',
    init: function( editor ) {
        editor.addCommand( 'jumpy', {
            exec: function( editor ) {
			    var selection = editor.getSelection();
                var range = selection.getRanges()[0];
                var pNode = range.startContainer.getAscendant('p', true);
                var newRange = new CKEDITOR.dom.range(range.document);
                newRange.moveToPosition(pNode, CKEDITOR.POSITION_BEFORE_END);
                newRange.select();
            }
        });
        editor.ui.addButton( 'Jumpy', {
            label: 'Jumpy',
            command: 'jumpy',
            toolbar: 'insert'
        });
    }
});