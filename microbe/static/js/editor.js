/**
 * Markdown editor
 * inspired from https://github.com/lepture/editor/blob/master/src/intro.js
 * @author : TROUVERIE Joachim
 **/
 
/**
 * Editor class
 * @param textarea_id : Textarea id to create CodeMirror instance
 * @param upload_url : Url used to upload files with DnD
 * @param convert_url : Url used to convert Markdown into html
 **/
function Editor(textarea_id, upload_url, convert_url) {
    var self = this;
    // codemirror
    self.codemirror = CodeMirror.fromTextArea(
        document.getElementById(textarea_id), {
            "theme": "xq-light",
            "mode": "markdown",
	    "lineWrapping": "true",
        });
    
    // manage drag and drop
    self.upload_url = upload_url;
    self.codemirror.setOption('onDragEvent', function(data, event) {
        if ( event.type === 'drop' ) {
            event.stopPropagation();
            event.preventDefault();
            // test formdata
            if ( !!window.FormData ) {
                var formdata = new FormData();
                // number of files
                if ( event.dataTransfer.files.length === 1 ) {
                    // images
                    if ( event.dataTransfer.files[0].type.match(/image.*/) ) {
                        // add wait text on editor
                        var text = '![Please wait during upload...]()';
                        var cursor = self.codemirror.getCursor('start');
                        var line = self.codemirror.getLine(cursor.line);
                        var new_value = line.slice(0, cursor.ch) + text + line.slice(cursor.ch);
                        self.codemirror.setLine(cursor.line, new_value);
                        self.codemirror.focus();
                        // Ajax
                        formdata.append('file', event.dataTransfer.files[0]);
                        var httpRequest = new XMLHttpRequest();
                        httpRequest.onreadystatechange = function() {
                            if (httpRequest.readyState === 4) {
                                if (httpRequest.status === 200) {
                                    var data = JSON.parse(httpRequest.responseText);
                                    if (data.error) {                                        
                                        self.codemirror.setLine(cursor.line, new_value.replace(text, ''));
                                        alert(data.error);
                                    }
                                    else {
                                        self.codemirror.setLine(cursor.line, new_value.replace(text, '![' + data.label + ']('+ data.url +')'));
                                    }
                                    self.codemirror.focus();
                                }
                            }
                        };
                        httpRequest.open('POST', self.upload_url);
                        httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                        httpRequest.send(formdata);
                    }
                    // plain text
                    else if ( event.dataTransfer.files[0].type.match(/text.*/) ) {
                        // read file
                        if ( typeof FileReader != 'undefined' ) {
                            var reader = new FileReader();
                            // paste its content
                            reader.onload = function() {
                                var text = reader.result;
                                var cursor = self.codemirror.getCursor('start');
                                var line = self.codemirror.getLine(cursor.line);
                                var new_value = line.slice(0, cursor.ch) + text + line.slice(cursor.ch);
                                self.codemirror.setLine(cursor.line, new_value);
                                self.codemirror.focus();
                            }
                            reader.readAsText(event.dataTransfer.files[0]);
                        }
                        else alert('FileReader not supported');
                    }
                    else alert('File format not supported');
                }
                else alert('You can upload only one file');
            }
            else alert('Your browser does not seem to support HTML5 Drag and drop API');
            
            return true;
        }
    });
    
    self.convert_url = convert_url;

    /*
     * Define if current line is in given state
     */
    self._getState = function(state) {
        var pos = self.codemirror.getCursor('start');
        var stat = self.codemirror.getTokenAt(pos);
        if (!stat.type) return false;

        var types = stat.type.split(' ');

        for (ii = 0; ii < types.length; ii++) {
            var data = types[ii];
            if (data === 'strong' && state === 'bold') {
                return true;
            } 
            else if (data === 'em' && state === 'italic') {
                return true;
            }
        }

        return false;
    }
    
    /*
     * Replace selection adding prefix and suffix
     */
    self._replaceSelection = function(prefix, suffix) {
        var start = self.codemirror.getCursor('start');
        var stop = self.codemirror.getCursor('end');

        var text = self.codemirror.getSelection();
        self.codemirror.replaceSelection(prefix + text + suffix);

        start.ch += prefix.length;
        stop.ch += suffix.length;

        self.codemirror.setSelection(start, stop);
        self.codemirror.focus();
    }

    /*
     * Toggle state for selection
     */
    self._toggleSelection = function(prefix, suffix, state) {
        var state = self._getState(state);

        // already in state
        if (state) {
            // get cursor
            var cursor = self.codemirror.getCursor('start');
            // get cursor line
            var line = self.codemirror.getLine(cursor.line);
            // split to keep only value with cursor
            var prefix_index = line.slice(0, cursor.ch).lastIndexOf(prefix);
            var suffix_index = cursor.ch + line.slice(cursor.ch).indexOf(suffix);
            // replace line
            line = line.slice(0, prefix_index) + line.slice(prefix_index + prefix.length, suffix_index) + line.slice(suffix_index + suffix.length)
            self.codemirror.setLine(cursor.line, line);
            self.codemirror.focus();
        } 
        else {
            self._replaceSelection(prefix, suffix);
        }
    }

    /**
     * draw editor toolbar
     */
    var container = document.createElement('div');
    container.className = 'toolbar';

    // bold
    var bold = document.createElement('span');
    bold.className = 'fi-bold';
    bold.title = 'Bold';
    bold.onclick = function(in_event) {
        self._toggleSelection('**', '**', 'bold');
    }
    container.appendChild(bold);
    // italic
    var italic = document.createElement('span');
    italic.className = 'fi-italic';
    italic.title = 'Italic';
    italic.onclick = function(in_event) {
        self._toggleSelection('*', '*', 'italic');
    }
    container.appendChild(italic);
    // img
    var img = document.createElement('span');
    img.className = 'fi-photo';
    img.title = 'Picture';
    img.onclick = function(in_event) {
        self._replaceSelection('![', '](/<your_file_url>)');
    }
    container.appendChild(img);
    // link
    var link = document.createElement('span');
    link.className = 'fi-link';
    link.title = 'Link';
    link.onclick = function(in_event) {
        self._replaceSelection('[', '](http://)');
    }
    container.appendChild(link);
    // undo
    var undo = document.createElement('span');
    undo.onclick = function() {
        self.codemirror.undo();
    }
    undo.className = 'fi-refresh';
    undo.title = 'Undo';
    container.appendChild(undo);
    // preview
    var preview = document.createElement('span');
    preview.onclick = function(in_event) {
        // create div if not exists
        var div = document.getElementById('markdown_preview');
        var wrapper = self.codemirror.getWrapperElement();
        var btn = this; 
        if (div == null) {
            div = document.createElement('div');
            div.setAttribute('id', 'markdown_preview');
            div.style.display = 'none';
            wrapper.parentNode.insertBefore(div, wrapper.nextSibling);
        }
        // show div
        if (wrapper.style.display != 'none') {
            // send request to server with value
            btn.className = 'fi-asterisk';
            var text = self.codemirror.getValue();
            var httpRequest = new XMLHttpRequest();
            httpRequest.onreadystatechange = function() {
                if (httpRequest.readyState === 4) {
                    if (httpRequest.status === 200) {
                        var data = JSON.parse(httpRequest.responseText);
                        div.innerHTML = data.value;
                        div.style.display = 'block';
                        wrapper.style.display = 'none';
                        btn.className = 'fi-lock';
                        btn.title = 'Click to unlock';
                    }
                }
            };
            httpRequest.open('POST', self.convert_url);
            httpRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            httpRequest.send('content=' + text);
        } 
        else {
            div.style.display = 'none';
            wrapper.style.display = 'block';
            btn.className = 'fi-eye';
            btn.title = 'Preview';
        }
    }
    preview.className = 'fi-eye';
    preview.title = 'Preview';
    container.appendChild(preview);
    // append container
    var wrapper = self.codemirror.getWrapperElement();
    wrapper.parentNode.insertBefore(container, wrapper);
}

