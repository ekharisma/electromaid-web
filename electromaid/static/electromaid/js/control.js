var device_id;
var device_status;
var device_active;
$(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    $('.create_modal').on('click', function () {
        $("#device_name").prop('disabled', false);
        document.getElementById('modal_label').innerHTML = "Create Device"
        document.getElementById('device_name').value = "";
        document.getElementById('device_daya').value = "0";
        $("#device_status").prop("checked", false);
        $("#device_active").prop("checked", false);
        $("#device_status").prop('disabled', true);
        $("#device_active").prop('disabled', true);
        $("#device_status").val("off");
        $("#device_aktif").val("false");
        $("#statusTxt").html("off");
        $("#activeTxt").html("false");
    });

    $('.update_modal').on('click', function () {
        $("#device_status").prop('disabled', false);
        $("#device_active").prop('disabled', false);
        document.getElementById('modal_label').innerHTML = "Change Device";
        var device_data = $(this).attr("data-id");
        console.log(device_data);
        var fields = device_data.slice(1, device_data.length - 1);
        fields = fields.split(",");

        device_id = fields[0];
        device_id = device_id.slice(1, device_id.length - 1);
        document.getElementById('device_name').value = device_id;
        $("#device_name").prop('disabled', true);

        device_status = fields[1];
        device_status = device_status.slice(1, device_status.length - 1);
        if (device_status == 'on') {
            console.log("Switch On ")
            $("#device_status").prop("checked", true);
        } else {
            console.log("Switch Off ")
            $("#device_status").prop("checked", false);
        }
        document.getElementById('statusTxt').innerHTML = device_status;
        document.getElementById('device_status').value = device_status;

        device_active = fields[2];
        device_active = device_active.slice(1, device_active.length - 1);
        document.getElementById('activeTxt').innerHTML = device_active;
        document.getElementById('device_active').value = device_active;
        if (device_active == 'True') {
            console.log(device_active)
            $("#device_active").prop("checked", true);
        } else {
            console.log("Switch Off ")
            $("#device_active").prop("checked", false);
            console.log(device_active)
        }

        var device_daya = fields[3];
        device_daya = device_daya.slice(1, device_daya.length - 1);
        document.getElementById('device_daya').value = device_daya;

    });

    $("#device_status").on('click', function () {
        if (document.getElementById('device_status').value == "off") {
            document.getElementById('device_status').value = "on";
            document.getElementById('statusTxt').innerHTML = "on";
        } else if (document.getElementById('device_status').value == "on") {
            document.getElementById('device_status').value = "off";
            document.getElementById('statusTxt').innerHTML = "off";
        }
    });

    $("#device_active").on('click', function () {
        if (document.getElementById('device_active').value == "False") {
            document.getElementById('device_active').value = "True";
            document.getElementById('activeTxt').innerHTML = "True";
        } else if (document.getElementById('device_active').value == "True") {
            document.getElementById('device_active').value = "False";
            document.getElementById('activeTxt').innerHTML = "False";
        }
    });

    $('form').submit(function (event) {
        const dev_id = document.getElementById('device_name').value;
        const dev_status = document.getElementById('device_status').value;
        const dev_active = document.getElementById('device_active').value;
        const dev_daya = document.getElementById('device_daya').value;

        var formData = {
            'csrfmiddlewaretoken': csrftoken,
            'id': dev_id,
            'daya': dev_daya,
            'status': 'off',
            'aktif': 'False'
        }
        $.ajax({
            type: 'POST',
            url: '',
            data: formData,

        }).done(function (data) {
            $("#createBtn").modal('hide');
            location.reload();
        });

        event.preventDefault();
    });

    var data_to_sent;
    $(".delete_modal").on("click", function () {
        var device_to_delete = $(this).attr("data-delete");
        data_to_sent = {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'delete',
            'id': device_to_delete
        };
    });
    $(".delete-device").on("click", function () { 
        $.ajax({
            type: "POST",
            url: '',
            data: data_to_sent
        }).done(function(data){
            console.log("Success");
            $("#delete_modal").modal('hide');
            location.reload();
        })
     })
});
