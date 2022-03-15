function load_selected_category_users() {
	
	let user_category = $('#user_category').find(":selected").text();
	$.ajax({
		type: 'GET',
		url: '/load_selected_category_users_ajax/',
		data: {
			'user_category': user_category
		},
		success: function(response) {
            usernames = eval(response)
            var select = document.getElementById("userprofile_tocreate");
            $('#userprofile_tocreate').attr('disabled', false);
            $(select).empty();
            $(select).append($('<option hidden>---------</option>'));
            $.each(usernames, function(i, p) {
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

function suggest_username(){
    let first_name,last_name, user_name;
    let selected_user = $('#userprofile_tocreate').find(":selected").text().split(' ');
    console.log(selected_user)
    let length = selected_user.length
    if (length == 1){
        first_name =  selected_user[0].toLowerCase()
        user_name = first_name
        console.log(user_name)
    }
    if (length == 2)
    {
        first_name = selected_user[0].toLowerCase()
        last_name = selected_user[1].toLowerCase()
    
        user_name = first_name+last_name;
        console.log(user_name)
    }


    $.ajax({
		type: 'GET',
		url: '/suggest_username_ajax/',
		data: {
			'user_name': user_name
		},
		success: function(response) {
            result = eval(response)
            if (result != 409){
                console.log(result)
                document.getElementById("username").value = user_name
                document.getElementById("user_id_field").value = result
            }
            if (result == 409)
            {
                console.log(usernames)
                document.getElementById("username").value = user_name + 1
            }
     
		},
		error: function(response) {
			console.log(response)
		}
	})
    

}