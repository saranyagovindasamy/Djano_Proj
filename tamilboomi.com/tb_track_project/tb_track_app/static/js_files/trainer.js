function load_lan() {
	$.ajax({
		type: 'GET',
		url: '/load_language_ajax/',
		data: {
			'course_name': $('#courseName').val()
		},
		success: function(response) {
			if (!response["valid"]) {
				coursenames = eval(response)
				var select = document.getElementById("langName");
				$('#langName').attr('disabled', false);
				$(select).empty();
				$(select).append($('<option hidden>select</option>'));
				$.each(coursenames, function(i, p) {
					$(select).append($('<option></option>').val(p).html(p));
				});
			}
		},
		error: function(response) {
			console.log(response)
		}
	})
}


function load_languages() {
	// console.log($('#course').val())
	$.ajax({
		type: 'GET',
		url: '/load_languages_ajax/',
		data: {
			'course': $('#course').val()
		},
		success: function (response) {
			if (!response["valid"]) {
				// languages = eval(response)
				// console.log(response.type)
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


function load_trainer() {
	$.ajax({
		type: 'GET',
		url: '/load_trainer_ajax/',
		data: {
			'course': $('#course').val()
		},
		success: function (response) {
			if (!response["valid"]) {
				languagenames = eval(response)
				var select = document.getElementById("language");
				$('#language').attr('disabled', false);
				trainernames = eval(response)
				var select = document.getElementById("trainerName");
				$('#trainerName').attr('disabled', false);
				$(select).empty();
				$(select).append($('<option hidden>select</option>'));
				$.each(trainernames, function (i, p) {
					$(select).append($('<option></option>').val(p).html(p));
				});
			}
		},
		error: function (response) {
			console.log(response)
		}
	})
}



function load_selected_batch_trainers() {
	$('div#right-side').find('span').html('');
	let batch_id = $('#batch option:selected').attr('id');
    // console.log($('#batch').find(":selected").text())
	// console.log(batch_id)
	$.ajax({
		type: 'GET',
		url: '/load_selected_batch_trainers_ajax/',
		data: {
			'batch': batch_id
		},
		success: function(response) {
            coursenames = eval(response)
            var select = document.getElementById("trainee");
            $('#trainee').attr('disabled', false);
            $(select).empty();
            $(select).append($('<option hidden>---------</option>'));
            $.each(coursenames, function(i, p) {
                // console.log(i)
                // console.log(p)
                $(select).append($('<option></option>').val(p).html(p));
            });
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}

function load_selected_trainer_details() {
	$('div#right-side').find('span').html('');
	let selected_trainer = $('#trainer').find(":selected").text()
	let trainer_id = $('#trainer option:selected').attr('id');
	var select_course = document.getElementById("course");
	$(select_course).empty();
	var select_batch = document.getElementById("batch");
	$(select_batch).empty();
	$.ajax({
		type: 'GET',
		url: '/load_selected_trainer_details_ajax/',
		data: {
			'trainer': $('#trainer').find(":selected").text()
		},
		success: function(data) {
			data_split = data.split(',')
			// console.log(data_split)
			document.getElementById("record_name").innerHTML = selected_trainer
			document.getElementById("email").innerHTML = data_split[0]
			document.getElementById("mobile_no").innerHTML = data_split[1]
		},
		error: function(response) {
			console.log(response)
		}
	})
}

function load_selected_trainer_course() {
	let selected_trainer = $('#trainer').find(":selected").text()
	let trainer_id = $('#trainer option:selected').attr('id');
	var select_batch = document.getElementById("batch");

	document.getElementById("course_name").innerHTML = ""
	document.getElementById("batch_name").innerHTML = ""
	document.getElementById("amount_paid").innerHTML = ""
	document.getElementById("balance_fee").innerHTML = ""

	$(select_batch).empty();
	$.ajax({
		type: 'GET',
		url: '/load_selected_trainer_course_ajax/',
		data: {
			'trainer': selected_trainer
		},
		success: function(response) {
			if (!response["valid"]) {
				// languages = eval(response)
				// console.log(response)
				data = response.split(',')
			
				var select = document.getElementById("course");
				 $(select).empty();
				var option = '<option>-------</option>';
				$('<option/>').val(option).html(option).appendTo('#course');
				for (var i = 0; i < data.length; i++) {
					select_str = data[i].split('#')
					select_id = select_str[0].replace(/'|[_\W]/, '')
					select_val = select_str[1].replace(/[_\W]+/g, '')
					// console.log(select_val)
					// console.log(select_id)
       
					$('<option/>').val(select_val).html(select_id).appendTo('#course');
				}
			}
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}


function load_trainer_batch()
{
	var select_batch = document.getElementById("batch");
	$(select_batch).empty();

	let selected_course = $('#course').find(":selected").text()
	let course_id = $('#course option:selected').attr('id');

	// console.log(selected_course)
	// console.log(course_id)
	$.ajax({
		type: 'GET',
		url: '/load_trainer_batch_ajax/',
		data: {
			'course': course_id,
		},
		success: function(response) {
       				// languages = eval(response)
				data = response.split(',')
				// console.log(data)
				var select = document.getElementById("batch");
				 $(select).empty();
				var option = '<option>-------</option>';
				$('<option/>').val(option).html(option).appendTo('#batch');
				for (var i = 0; i < data.length; i++) {
					select_str = data[i].split('#')
					select_id = select_str[0].replace(/'|[_\W]/, '')
					select_val = select_str[1].replace(/[_\W]+/g, '')
       
					$('<option/>').val(select_val).html(select_id).appendTo('#batch');
				}
				$('#trainee-data').css("display","none");
			
		},
		error: function(response) {
			console.log(response)
		}
	})

}
function load_selected_course_batch() {
	var select_batch = document.getElementById("batch");
	$(select_batch).empty();
	document.getElementById("batch_name").innerHTML = ""
	document.getElementById("amount_paid").innerHTML = ""
	document.getElementById("balance_fee").innerHTML = ""
	let selected_trainer = $('#trainer').find(":selected").text()
	let trainer_id = $('#trainer option:selected').attr('id');
	let selected_course = $('#course').find(":selected").text()
	let course_id = $('#course').val()
	document.getElementById("course_name").innerHTML = selected_course.replace(/'|[_\W]/, '')
	console.log(selected_trainer)
	console.log(trainer_id)
	console.log(selected_course.replace(/'|[_\W]/, ''))
	console.log(course_id)
	$.ajax({
		type: 'GET',
		url: '/load_selected_course_batch_ajax/',
		data: {
			'course': course_id,
			'trainer': trainer_id,
		},
		success: function(response) {
       				// languages = eval(response)
				data = response.split(',')
				// console.log(data)
				var select = document.getElementById("batch");
				 $(select).empty();
				var option = '<option>-------</option>';
				$('<option/>').val(option).html(option).appendTo('#batch');
				for (var i = 0; i < data.length; i++) {
					select_str = data[i].split('#')
					select_id = select_str[0].replace(/'|[_\W]/, '')
					select_val = select_str[1].replace(/[_\W]+/g, '')
       
					$('<option/>').val(select_val).html(select_id).appendTo('#batch');
				}
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}


function load_selected_batch_traineer_fees() {
	document.getElementById("amount_paid").innerHTML = ""
	document.getElementById("balance_fee").innerHTML = ""
	let selected_trainer = $('#trainer').find(":selected").text()
	let trainer_id = $('#trainer option:selected').attr('id');
	let selected_course = $('#course').find(":selected").text()
	let selected_batch = $('#batch').find(":selected").text()
	let course_id = $('#course').val()
	let batch_id = $('#batch').val()
	document.getElementById("batch_name").innerHTML = selected_batch.replace(/'|[_\W]/, '')
	document.getElementById("remarks").value = 'payment for ' +selected_batch.replace(/'|[_\W]/, '')
	// console.log(selected_trainer)
	// console.log(trainer_id)
	// console.log(selected_course.replace(/'|[_\W]/, ''))
	// console.log(course_id)
	$.ajax({
		type: 'GET',
		url: '/load_selected_batch_traineer_fee_ajax/',
		data: {
			'course': course_id,
			'trainer': trainer_id,
			'batch':batch_id
		},
		success: function(response) {
       				// languages = eval(response)
				trainer_data = response.split(',')
				// console.log(trainer_data)
				document.getElementById("batch_pay").innerHTML = trainer_data[0]
				document.getElementById("amount_paid").innerHTML = trainer_data[1]
				document.getElementById("balance_fee").innerHTML = trainer_data[2]
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}

function load_selected_batch_trainees()
{

	let selected_course = $('#course').find(":selected").text()
	let selected_batch = $('#batch').find(":selected").text()
	let course_id = $('#course option:selected').attr('id');
	let batch_id = $('#batch').val();
	// console.log(course_id)
	// console.log(batch_id)
	$.ajax({
		type: 'GET',
		url: '/load_selected_batch_trainees_ajax/',
		data: {
			'course': course_id,
			'batch':batch_id
		},
		success: function(data) {
       				// languages = eval(response)
				$('.trainee-data').html($(data).find(".trainee-data").html())
				$('#trainee-data').css("display","block");
		},
		error: function(response) {
			console.log(response)
		}
	})

}