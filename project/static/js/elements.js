function _addAttrs(object, attrs) {
	Object.keys(attrs).forEach(function(key) {
		object.setAttribute(key, attrs[key]);
	});
}

function _form(attrs) {
	var form = document.createElement('form');
	_addAttrs(form, attrs);
	return form;
}

function _fieldset(attrs) {
	var fieldset = document.createElement('fieldset');
	_addAttrs(fieldset, attrs);
	return fieldset;
}


function _div(attrs) {
	var div = document.createElement('div');
	_addAttrs(div, attrs);
	return div;
}

function _button(content, attrs) {
	var btn = document.createElement('button');
	_addAttrs(btn, attrs);
	btn.innerHTML = content;
	return btn;
}

function _span(attrs) {
	var span = document.createElement('span');
	_addAttrs(span, attrs);
	return span;
}

function _header(level, attrs) {
	var h = document.createElement('h' + level);
	_addAttrs(h, attrs);
	return h;
}

function _form(attrs) {
	var form = document.createElement('form');
	_addAttrs(form, attrs);
	return form;
}

function _textarea(attrs, content) {
	var textarea = document.createElement('textarea');
	_addAttrs(textarea, attrs);
	if (content != undefined) {
		textarea.innerHTML = content;
	}
	return textarea;
}

function _titleInput(name, id, value) {
	var titleInput = document.createElement('input');
	titleInput.setAttribute('type', 'text');
	titleInput.setAttribute('class', 'form-control');
	titleInput.setAttribute('required', 'required');
	titleInput.setAttribute('name', name);
	titleInput.setAttribute('id', id);
	if ( value != undefined ) {
		titleInput.setAttribute('value', value);
	}
	return titleInput;
}

function _titleInputPrefilled(name, id, value) {
	var titleInput = document.createElement('input');
	titleInput.setAttribute('type', 'text');
	titleInput.setAttribute('class', 'form-control');
	titleInput.setAttribute('required', 'required');
	titleInput.setAttribute('name', name);
	titleInput.setAttribute('id', id);
	titleInput.setAttribute('value', value);
	return titleInput;
}

function _submitInput(value, displayClass) {
	var submitInput = document.createElement('input');
	submitInput.setAttribute('type', 'submit');
	submitInput.setAttribute('class', 'btn btn-sm btn-' + displayClass);
	submitInput.setAttribute('value', value);
	return submitInput;
}