function toggleAlert(name, time) {
	$(name).show().delay(time).fadeOut();
}

function ajaxError() {
	$('.alert-info').fadeOut().delay(1000);
	toggleAlert('.alert-danger', 3000)
}

function handleDocCreate(name, type) {
	if (!name || name.length === 0) {
		toggleAlert('.alert-warning', 3000);
	}
	else {
		$('.alert-info').show();
		$.get(type, {
			'name': name,
		})
		.done(function(data) {
			console.log(data);
			if (data['data']) {
				$('.alert-info').fadeOut().delay(1000);
				$("#doc_link").attr('href', data['data']);
				toggleAlert('.alert-success', 5000);
			}
			else
				ajaxError();
		})
		.fail(ajaxError);
	}
}

window.addEventListener('load', function(event) {
	var app = new Vue({
		el: '#app',
		data: {
			name: "",

			addDoc: function() {
				handleDocCreate(this.name, '/create_doc/');
				this.name = "";
			},

			addSheet: function() {
				handleDocCreate(this.name, '/create_sheet/');
				this.name = "";
			}
		}
	})
});