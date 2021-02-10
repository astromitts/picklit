function doSynchedPost(targetUrl, postData) {
	var resultData;
	$.ajax({
		method: 'POST',
		url: targetUrl,
		dataType: 'json',
		data: postData,
		async: false,
		//beforeSend: function(){
		//	$('div#loader').removeClass('default-hidden');
		//},
		success: function successFunction(data) {
			resultData = data;
			//setTimeout(function () {
			//	$('div#loader').addClass('default-hidden');
		    //}, 500);
		},
		error: function errorFunction(data) {
			//setTimeout(function () {
			//	$('div#loader').addClass('default-hidden');
		    //}, 500);
		}
	});
	return resultData;
}


function doASynchedPost(targetUrl, postData, callBack) {
	$.ajax({
		method: 'POST',
		url: targetUrl,
		dataType: 'json',
		data: postData,
		beforeSend: function(){
			showLoader();
		},
		success: function successFunction(data) {
			callBack(data);
		},
		error: function errorFunction(data) {
			alert('An unkown error happened.');
			hideLoader();
		}
	});
}


function doASynchedGet(targetUrl, callBack) {
	$.ajax({
		method: 'GET',
		url: targetUrl,
		dataType: 'json',
		beforeSend: function(){
			showLoader();
		},
		success: function successFunction(data) {
			callBack(data);
			hideLoader();
		},
		error: function errorFunction(data) {
			
			hideLoader();
		}
	});
}


function doSynchedGet(targetUrl) {
	showLoader();
	$.ajax({
		method: 'GET',
		url: targetUrl,
		dataType: 'json',
		async: false,
		success: function successFunction(data) {
			resultData = data;
		}
	});
	return resultData;
}


function showLoader() {
	$('div#loader').removeClass('default-hidden');
}


function hideLoader() {
	$('div#loader').addClass('default-hidden');
}


function hide(element) {
	if (!element.hasClass('default-hidden')) {
		element.addClass('default-hidden');
	}
}


function show(element) {
	if (element.hasClass('default-hidden')) {
		element.removeClass('default-hidden');
	}
}


function toggleVisibility(element) {
	if (element.hasClass('default-hidden')) {
		element.removeClass('default-hidden');
	} else {
		element.addClass('default-hidden');
	}
}


function toggleText(element) {
	var expandedText = element.attr('data-expanded-text');
	var collapsedText = element.attr('data-collapsed-text');
	if ( expandedText != undefined ) {
		if ( element.html() != expandedText ) {
			element.html(expandedText);
		} else {
			element.html(collapsedText);
		}
	}
}


function bindToggleButtons() {
	$('.js-expand-collapse-toggle').click(function doToggle(){
		toggleText($(this));
		var showTarget = $($(this).attr('data-show-target'));
		if ( showTarget.length > 1 ) {
			showTarget.each(function toggleElement() {
				toggleVisibility($(this));
			});
		} else {
			toggleVisibility(showTarget);
		}
		var hideTarget = $(this).attr('data-hide-target');
		if ( hideTarget != undefined ) {
			hide(hideTarget);
		}
	});
}


function showMessage(message, type) {
/*
	<div id="js-alert" class="alert alert-dismissible fade show" role="alert">
	 	<strong><span id="message-body"></span></strong>
	 	<button type="button" class="close" data-dismiss="alert" aria-label="Close">
	 	<span aria-hidden="true">&times;</span>
	</div>

*/
	var messageDiv = document.createElement('div');
	messageDiv.setAttribute('id', 'js-alert')
	messageDiv.setAttribute('class', 'alert alert-dismissible fade show alert-' + type);
	messageDiv.innerHTML = '<strong>' + message + '</strong>';
	messageDiv.innerHTML = messageDiv.innerHTML + '<button class="close float-right" data-dismiss="alert" aria-label="Close">X</button>';

	var messagesCol = document.getElementById('js-messages-col');
	messagesCol.append(messageDiv);
	window.scrollTo(0, 0);
}


function errorMessage(message) {
	showMessage(message, 'danger');
}


function warningMessage(message) {
	showMessage(message, 'warning');

}


function successMessage(message) {
	showMessage(message, 'success');

}


function primaryMessage(message) {
	showMessage(message, 'primary');

}


function bindAjaxFormSubmit(form_id) {
	$('form#' + form_id).submit(function(event){
		event.preventDefault()
		var submitUrl = $(this).attr('action');
		var reloadUrl = $('input#id_submit_done_url').val();
		doASynchedPost(
	        submitUrl,
	        $(this).serialize(),
	        function handleFormSubmitOutcome(submitData) {
	        	if (submitData.status == 'success') {
	        		if (reloadUrl) {
	        			window.location.href = reloadUrl;
	        		}
	        	} else {
	        		errorMessage(submitData.message);
	        	}
	        },
	    );
	});
}

function bindShowModal(element) {
	element.click(function showModal(){
		var modalId = $(this).attr('data-modal-id');
		$('#' + modalId).modal('show');
	});
}

function getSvgFromCache(elementID) {
	var sourceSvg = document.getElementById('svg-cache-' + elementID);
	var elementCopy = sourceSvg.cloneNode(true);
	return elementCopy;
}
