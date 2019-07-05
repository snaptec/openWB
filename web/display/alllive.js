do2Interval = setInterval(loadText, 5000);
function loadText(){
    $.ajax({
        url:"/openWB/web/tools/lademodus.php",
        type: "post", //request type,
        dataType: 'json',
        data: {call: "loadfile"},
        success:function(result){
            if(result.text == 0){
                $('.actstat .btn').addClass("btn-green");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
            }
            if(result.text == 1){
                $('.actstat1 .btn').addClass("btn-green");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 2){
                $('.actstat2 .btn').addClass("btn-green");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 3){
                $('.actstat2 .btn').addClass("btn-red");
	        $('.actstat2 .btn').removeClass("btn-green");
                $('.actstat3 .btn').addClass("btn-green");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-red");
                $('.actstat4 .btn').removeClass("btn-green");

            }
            if(result.text == 4){
                $('.actstat2 .btn').addClass("btn-red");
                $('.actstat3 .btn').addClass("btn-red");
                $('.actstat .btn').addClass("btn-red");
                $('.actstat1 .btn').addClass("btn-red");
                $('.actstat .btn').removeClass("btn-green");
                $('.actstat2 .btn').removeClass("btn-green");
                $('.actstat3 .btn').removeClass("btn-green");
                $('.actstat1 .btn').removeClass("btn-green");
                $('.actstat4 .btn').addClass("btn-green");
                $('.actstat4 .btn').removeClass("btn-red");

            }
        }
    });
}
loadText();


