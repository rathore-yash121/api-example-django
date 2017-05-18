$(document).ready(function(){
    $("#dashboardPage").on('click touchstart', 'button#sendWishesBtn', function(){
        console.log("ss");
        $("#sendMail").css('display', 'block');
        $("#birthdayList").css('display', 'none');
        $(this).css('display', 'none');
        var patients = [];
        var patientsEmailList = [];
        $(".checkName").each(function(){
            if($(this).is( ":checked" )){
                patients.push($(this).parent().text().trim());
                patientsEmailList.push($(this).parent().attr('id').trim());
            }
        });
        console.log(patients.join(';'));
        $("#recipients").val(patients.join(';'));
        $("#recipientsEmail").val(patientsEmailList.join(';'));

    });

    $("#dashboardPage").on('click touchstart', 'button#discardBtn', function(){
        $("#sendMail").css('display', 'none');
        $("#birthdayList").css('display', 'block');
        $("#sendWishesBtn").css('display', 'block');
    });


});
