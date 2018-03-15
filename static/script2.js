$(document).ready(function() {
    var text = $('#text');
    text.html("<b>Email Recieved: </b>");

    var expand = $('#close');
    expand.hide();

    var sec1 = $('#sec1-sql');
    var sec2 = $('#sec2-sql');
    var sec3 = $('#sec3-sql');


    var close = $('#close-sql');
    close.on('click', function() {
        sec2.hide();
        sec3.removeClass("col-md-5");
        sec3.addClass("col-md-10");
        sec3.css('transition-duration','1s');
        sec3.css('transition-timing-function','linear');
        $('.main1').css('border-left', '8px solid rgb(114, 114, 114)');
        expand.show();
    });

    expand.on('click', function() {
        sec2.show();
        sec3.removeClass("col-md-10");
        sec3.addClass("col-md-5");
        sec3.css('transition-duration','0s');
        $('.main1').css('border-left', '0px solid rgb(114, 114, 114)');
        expand.hide();
    });

    var str = "> SELECT * FROM Customers WHERE CustomerID=1;";
    $('#run-query').click(function() {
        console.log("Hey");
        $('#area').val(str);
    });

    var list = [];
    var i = 1;
    var j = 1;
    var k = 1;
    var s;

    $('#btn1').click(function (e) {
        if(i === 1) {
            var img_src = $('#btn1').parent().siblings()[0].id;
            list.push(img_src);
            console.log(list);
            i = 0;
            s = '?q=';
            for (var a in list) {
                s = s + list[a] + '+';
            }
            s = s.substr(0, s.length);
            $('#report').attr('href', "/report"+ s);
        }
    });

    $('#btn2').click(function (e) {
        if(j === 1) {
            var img_src = $('#btn2').parent().siblings()[0].id;
            list.push(img_src);
            console.log(list);
            j = 0;
            s = '?q=';
            for (var a in list) {
                s = s + list[a] + '+';
            }
            s = s.substr(0, s.length-1);
            $('#report').attr('href', "/report"+ s);
        }
    });

    $('#btn3').click(function (e) {
        if(k === 1) {
            var img_src = $('#btn3').parent().siblings()[0].id;
            list.push(img_src);
            console.log(list);
            k = 0;
            s = '?q=';
            for (var a in list) {
                s = s + list[a] + '+';
            }
            s = s.substr(0, s.length-1);
            $('#report').attr('href', "/report"+ s);
        }
    });

    var param;

    function help() {
        var str = window.location.href;
        var url = new URL(str);
        var q = url.searchParams.get("q");
        console.log(q);
        param = q.split(' ');
        console.log(param);
        return param;
    }


    $('#img-one').hide();
    $('#img-two').hide();
    $('#img-three').hide();

    function show() {
        var array = help();
        var len = array.length;
        console.log(array);
        var b;
        if(len === 1) {
            $('#img-one').show();
        } else if (len === 2) {
            $('#img-one').show();
            $('#img-two').show();
        } else if (len === 3) {
            $('#img-one').show();
            $('#img-two').show();
            $('#img-three').show();
        }
    }

    function loop() {
        var array = help();
        for(var i in array) {
            if(array[i] === 'img1') {
                $('#img-one').show();
            } else if (array[i] === 'img2') {
                $('#img-two').show();
            } else if (array[i] === 'img3') {
                $('#img-three').show();
            }
        }
    }

    loop();
});