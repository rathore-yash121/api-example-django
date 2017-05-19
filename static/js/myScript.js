$(document).ready(function(){
   // if send wishes button is clicked
    $("#dashboardPage").on('click touchstart', 'button#sendWishesBtn', function(){
        console.log("ss");
        $("#sendMail").css('display', 'block');
        $("#birthdayList").css('display', 'none');
        $(this).css('display', 'none');
        var patients = [];
        var patientsEmailList = [];
        $(".checkName").each(function(){
            if($(this).is( ":checked" )){
              // store the patient's name list
                patients.push($(this).parent().text().trim());
              // store the patient's email list
                patientsEmailList.push($(this).parent().attr('id').trim());
            }
        });
        console.log(patients.join(';'));
        $("#recipients").val(patients.join(';'));
        $("#recipientsEmail").val(patientsEmailList.join(';'));

    });
   // if discard button is clicked
    $("#dashboardPage").on('click touchstart', 'button#discardBtn', function(){
        $("#sendMail").css('display', 'none');
        $("#birthdayList").css('display', 'block');
        $("#sendWishesBtn").css('display', 'block');
    });


});
