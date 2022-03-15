function load_enroll_batch() {

	let course = $('#course').find(":selected").text()
	console.log(course)
	$.ajax({
		type: 'GET',
		url: '/load_enroll_batch_ajax/',
		data: {
			'course': course
		},
		success: function (response) {
			if (!response["valid"]) {
				// languages = eval(response)
				data = response.split(',')
			
				var select = document.getElementById("up_batch");
				$(select).empty();

				if (data == "['empty']") {
					
					$('#notify-div').show();
					$('#upcoming-div').hide();
				}
				else {

					$('#upcoming-div').show();
					$('#notify-div').hide();
					var option = '<option>-------</option>';
					$('<option/>').val(option).html(option).appendTo('#up_batch');
					for (var i = 0; i < data.length; i++) {
						select_str = data[i].split('#')
						select_id = select_str[0].replace(/'|[_\W]/, '')
						select_val = select_str[1].replace(/[_\W]+/g, '')

						$('<option/>').val(select_val).html(select_id).appendTo('#up_batch');
					}
				}
			}
			load_enroll_languages(course);
		},
		error: function (response) {
			console.log(response)
		}
	})
}

function load_enroll_languages(course) {

	$.ajax({
		type: 'GET',
		url: '/load_languages_ajax/',
		data: {
			'course': course
		},
		success: function (response) {
			if (!response["valid"]) {
				// languages = eval(response)
				data = response.split(',')
				// console.log(data)
				var select = document.getElementById("language");
				$(select).empty();
				var option = '<option>-------</option>';
				$('<option/>').val(option).html(option).appendTo('#language');
				for (var i = 0; i < data.length; i++) {
					select_str = data[i].split('-')
					select_id = select_str[0].replace(/[_\W]+/g, '')
					select_val = select_str[1].replace(/[_\W]+/g, '')

					$('<option/>').val(select_val).html(select_id).appendTo('#language');
				}
			}
		},
		error: function (response) {
			console.log(response)
		}
	})
}
