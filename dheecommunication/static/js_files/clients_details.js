
function clientDetailsLoader() {
    var $client_name = $('#client_name').find(":selected").text();
    console.log($client_name)
    if ($client_name !== '---------') {
        var url = '/load_client_ajax/'
        var data_dict = { 'client_name': $client_name, 'csrfmiddlewaretoken': '{{ csrf_token }}' }
        $.ajax({
            type: 'GET',
            url: url,
            data: data_dict,
            success: function (data) {

                data_split = data.split(',')
                console.log(data_split)
                document.getElementById("record_name").innerHTML = data_split[0]
                document.getElementById("contact_name").innerHTML = data_split[1]
                document.getElementById("mobile_no").innerHTML = data_split[2]
                document.getElementById("area_name").innerHTML = data_split[3]
                document.getElementById("pending_payment").innerHTML = data_split[4]
            },
            error: function (error) {
                console.log('error');
                console.log(JSON.stringify(error));
            }
        });
    }
}

function load_client_by_id_ajax($client_id) {
    console.log($client_id)
    if ($client_id !== '---------') {
        var url = '/load_client_by_id_ajax/'
        var data_dict = { 'client_id': $client_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' }
        $.ajax({
            type: 'GET',
            url: url,
            data: data_dict,
            success: function (data) {

                data_split = data.split(',')
                // console.log(data_split)
                document.getElementById("record_name").innerHTML = data_split[0]
                document.getElementById("contact_name").innerHTML = data_split[1]
                document.getElementById("mobile_no").innerHTML = data_split[2]
                document.getElementById("area_name").innerHTML = data_split[3]
                document.getElementById("pending_payment").innerHTML = data_split[4]
            },
            error: function (error) {
                console.log('error');
                console.log(JSON.stringify(error));
            }
        });
    }
}


function load_client_transcation_by_id_ajax($client_id) {
    console.log($client_id)
    if ($client_id !== '---------') {
        var url = '/load_client_transcation_by_id_ajax/'
        var data_dict = { 'client_id': $client_id, 'csrfmiddlewaretoken': '{{ csrf_token }}' }
        $.ajax({
            type: 'GET',
            url: url,
            data: data_dict,
            success: function (data) {

                data = JSON.parse(data)
                // console.log(data)
                // console.log(typeof(data))

                // $('#selected-client-transcation-table').html($(data).find("#selected-client-transcation-table").html())
                selected_client_transcation_table(data)
				$('#selected-client-transcation-table').css("display","block");
            },
            error: function (error) {
                console.log('error');
                console.log(JSON.stringify(error));
            }
        });
    }
}

function selected_client_transcation_table(data)
{
    var header = $('<tr class="w-auto align-middle"><th scope="col">Type</th>'+
    '<th scope="col">Name in Record</th>'+
    '<th scope="col">Date</th>'+
    '<th scope="col">Transaction Type</th>'+
    '<th scope="col">Debit Amount</th>'+
    '<th scope="col">Credit Amount</th>'+
    '<th scope="col">Open Balance</th>'+
    '<th scope="col">Close Balance</th>'+
    '<th scope="col">Collected On</th></tr>')
    var tableelement = $('#client-transcations')

    tableelement.append(header)

    for(var i=0; i< data.length; i++){
        tableelement.append(createRow(data[i]));
} 
}

function createRow(client){

    // console.log(client.type)
    // console.log(client.client)
    // console.log(client.date)
    // console.log(client.debit_option)
    // console.log(client.debit_amount)
    // console.log(client.open_balance)
    // console.log(client.close_balance)
    // console.log(client.collected_on)

    if (client.type == 'Debit')
    {
        var trElement = '<tbody><tr class="w-auto align-middle">'+
        '<td class="text-center">'+ client.type +'</td>'+
        '<td class="text-center">'+ client.client + '</td>'+
        '<td class="text-center">'+client.date+'</td>'+
        '<td class="text-center">'+ client.debit_option +'</td>'+
        '<td class="text-center">'+ client.debit_amount +'</td>'+
        '<td class="text-center">'+ " " +'</td>'+
        '<td class="text-center">'+ client.open_balance +'</td>'+
        '<td class="text-center">'+ client.close_balance+'</td>'+
        '<td class="text-center">'+ client.collected_on+'</td>'+
        '</tr> </tbody>';
    }
    else
    {
        var trElement = '<tbody><tr class="w-auto align-middle">'+
        '<td class="text-center">'+ client.type +'</td>'+
        '<td class="text-center">'+ client.client + '</td>'+
        '<td class="text-center">'+client.date+'</td>'+
        '<td class="text-center">'+ client.credit_option +'</td>'+
        '<td class="text-center">'+ " " +'</td>'+
        '<td class="text-center">'+ client.credit_amount +'</td>'+
        '<td class="text-center">'+ client.open_balance +'</td>'+
        '<td class="text-center">'+ client.close_balance+'</td>'+
        '<td class="text-center">'+ client.collected_on+'</td>'+
        '</tr> </tbody>';
    }

    return trElement
}
