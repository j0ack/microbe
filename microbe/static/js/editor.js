/***
* JavaScript for Markdown Editor
* https://github.com/lepture/editor/blob/master/src/intro.js
* author : Hsiaoming Yang
**/

/**
* Get state of editor
**/
function _getState(cm, pos) {
  pos = pos || cm.getCursor('start');
  var stat = cm.getTokenAt(pos);
  if (!stat.type) return {};

  var types = stat.type.split(' ');

  var ret = {}, data, text;
  for (var i = 0; i < types.length; i++) {
    data = types[i];
    if (data === 'strong') {
      ret.bold = true;
    } 
    else if (data === 'em') {
      ret.italic = true;
    }
  }
  return ret;
}

/**
* Replace text in editor
**/
function _replaceSelection(cm, start, end) {
  var startPoint = cm.getCursor('start');
  var endPoint = cm.getCursor('end');
  
  var text = cm.getSelection();
  cm.replaceSelection(start + text + end);

  startPoint.ch += start.length;
  endPoint.ch += start.length;
  
  cm.setSelection(startPoint, endPoint);
  cm.focus();
}


/**
* Set text to bold
**/
function toggleBold(editor) {
  var stat = _getState(editor);

  var text;
  var start = '**';
  var end = '**';

  var startPoint = editor.getCursor('start');
  var endPoint = editor.getCursor('end');
  if (stat.bold) {
    text = editor.getLine(startPoint.line);
    start = text.slice(0, startPoint.ch);
    end = text.slice(startPoint.ch);

    start = start.replace(/^(.*)?(\*|\_){2}(\S+.*)?$/, '$1$3');
    end = end.replace(/^(.*\S+)?(\*|\_){2}(\s+.*)?$/, '$1$3');
    startPoint.ch -= 2;
    endPoint.ch -= 2;
    editor.setLine(startPoint.line, start + end);
  } 
  
  else {
    text = editor.getSelection();
    editor.replaceSelection(start + text + end);

    startPoint.ch += 2;
    endPoint.ch += 2;
  }

  editor.setSelection(startPoint, endPoint);
  editor.focus();
}

/**
* Set text to italic
**/
function toggleItalic(editor) {
  var stat = _getState(editor);

  var text;
  var start = '*';
  var end = '*';

  var startPoint = editor.getCursor('start');
  var endPoint = editor.getCursor('end');
  if (stat.bold) {
    text = editor.getLine(startPoint.line);
    start = text.slice(0, startPoint.ch);
    end = text.slice(startPoint.ch);

    start = start.replace(/^(.*)?(\*|\_)(\S+.*)?$/, '$1$3');
    end = end.replace(/^(.*\S+)?(\*|\_)(\s+.*)?$/, '$1$3');
    startPoint.ch -= 1;
    endPoint.ch -= 1;
    editor.setLine(startPoint.line, start + end);
  } 

  else {
    text = editor.getSelection();
    editor.replaceSelection(start + text + end);

    startPoint.ch += 1;
    endPoint.ch += 1;
  } 

  editor.setSelection(startPoint, endPoint);
  editor.focus();
}

/**
* Action for drawing a link.
*/
function drawLink(editor) {
  var stat = _getState(editor);
  _replaceSelection(editor, '[', '](http://)');
}


/**
* Action for drawing an img.
*/
function drawImage(editor) {
  var stat = _getState(editor);
  _replaceSelection(editor, '![', '](/static/media/<your_file>)');
}

/**
 * Action to toggle preview
 **/
function togglePreview(editor) {
    if (typeof markdown_converter === "undefined")
        markdown_converter = Markdown.getSanitizingConverter().makeHtml;
    var wrapper = editor.getWrapperElement();
    var preview = document.getElementById('markdown_preview');
    var btn = document.getElementById('preview_btn');
    if (wrapper.style.display != 'none') {
        var text = markdown_converter(editor.getValue());
        preview.innerHTML = text;
        preview.style.display = 'block';
        wrapper.style.display = 'none';
        btn.className += ' active';
    }
    else {
        preview.style.display = 'none';
        wrapper.style.display = 'block';
        btn.className = btn.className.replace('active', '');
    }   
}    

/**
 * Draw toolbar for editor
 **/
function drawToolbar(editor) {
    var container = document.createElement('div');
    container.className = 'toolbar';
    // bold
    var bold = document.createElement('a');
    bold.onclick = function(evt) {
        toggleBold(editor);
    }
    var bold_img = document.createElement('i');
    bold_img.className = 'fi-bold';
    bold.appendChild(bold_img);
    container.appendChild(bold);
    // italic
    var italic = document.createElement('a');
    italic.onclick = function(evt) {
        toggleItalic(editor);
    }
    var italic_img = document.createElement('i');
    italic_img.className = 'fi-italic';
    italic.appendChild(italic_img);
    container.appendChild(italic);
    // img
    var img = document.createElement('a');
    img.onclick = function(evt) {
        drawImage(editor);
    }
    var img_img = document.createElement('i');
    img_img.className = 'fi-photo';
    img.appendChild(img_img);    
    container.appendChild(img);
    // link
    var link = document.createElement('a');
    link.onclick = function(evt) {
        drawLink(editor);
    }
    var link_img = document.createElement('i');
    link_img.className = 'fi-link';
    link.appendChild(link_img);    
    container.appendChild(link);
    // preview
    var preview = document.createElement('a');
    preview.onclick = function(evt) {
        togglePreview(editor);
    }
    preview.setAttribute('id', 'preview_btn');
    var preview_img = document.createElement('i');
    preview_img.className = 'fi-eye';
    preview.appendChild(preview_img);
    container.appendChild(preview);

    // append container
    var wrapper = editor.getWrapperElement();
    wrapper.parentNode.insertBefore(container, wrapper);
}

/**
 * Insert preview div
 **/
function drawPreview(editor) {
    var wrapper = editor.getWrapperElement();
    var preview = document.createElement('div');
    preview.setAttribute('id', 'markdown_preview');
    preview.style.display = 'none';
    wrapper.parentNode.insertBefore(preview, wrapper.nextSibling);
}
