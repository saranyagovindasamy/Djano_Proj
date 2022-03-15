function load_batch() {
    
	
    let course = $('#course').find(":selected").text()
    console.log(course)
	$.ajax({
		type: 'GET',
		url: '/load_batch_ajax/',
		data: {
			'course': course
		},
		success: function (response) {
			if (!response["valid"]) {
				// languages = eval(response)
				console.log(response.type)
				data = response.split(',')
				console.log(data)
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
			}
		},
		error: function(response) {
			console.log(response)
		}
	})
}

function load_trainees() {
	$('div#right-side').find('span').html('');
	// let batch_id = $('#batch option:selected').attr('id');
	let batch_id = $('#batch').val();
    // console.log($('#batch').find(":selected").text())
	// console.log($('#batch').val())
	console.log(batch_id)
	$.ajax({
		type: 'GET',
		url: '/load_trainees_ajax/',
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
                console.log(i)
                console.log(p)
                $(select).append($('<option></option>').val(p).html(p));
            });
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}

function load_selected_trainee_details() {
	$('div#right-side').find('span').html('');
	let selected_trainee = $('#trainee').find(":selected").text()
	let trainee_id = $('#trainee option:selected').attr('id');
	let batch_id = $('#batch').val();
	console.log(selected_trainee)
	console.log(trainee_id)
	$.ajax({
		type: 'GET',
		url: '/load_selected_trainee_details_ajax/',
		data: {
			'trainee': $('#trainee').find(":selected").text(),
			'batch': batch_id
		},
		success: function(data) {
    
			data_split = data.split(',')
			console.log(data_split)
			document.getElementById("record_name").innerHTML = selected_trainee
			document.getElementById("email").innerHTML = data_split[0]
			document.getElementById("mobile_no").innerHTML = data_split[1]
			document.getElementById("course_entrolled").innerHTML = data_split[2]
			document.getElementById("batch_name").innerHTML = data_split[3]
			document.getElementById("amount_paid").innerHTML = data_split[4]
			document.getElementById("balance_fee").innerHTML = data_split[5]
		},
		error: function(response) {
			console.log(response)
		}
	})
}