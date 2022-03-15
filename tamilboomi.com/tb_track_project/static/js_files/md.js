function load_courses() {
    console.log($('#language').find(":selected").text())
	$.ajax({
		type: 'GET',
		url: '/load_courses_md_ajax/',
		data: {
			'language': $('#language').find(":selected").text()
		},
		success: function(response) {
            coursenames = eval(response)
            var select = document.getElementById("courses");
            $('#courses').attr('disabled', false);
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

function load_trainer() {
    
    let language = $('#language').find(":selected").text();
    let course = $('#courses').find(":selected").text()
    console.log(language, course)
	$.ajax({
		type: 'GET',
		url: '/load_trainer_md_ajax/',
		data: {
			'language': language,
            'course': course
		},
		success: function(response) {
            trainernames = eval(response)
            var select = document.getElementById("trainer");
            $('#trainer').attr('disabled', false);
            $(select).empty();
            $(select).append($('<option hidden>---------</option>'));
            $.each(trainernames, function(id, name) {
                console.log(id)
                console.log(name)
                $('<option/>').val(name).html(name).appendTo('#trainer');
                // $(select).append($('<option></option>').val(p).html(p));
            });
			
		},
		error: function(response) {
			console.log(response)
		}
	})
}
