$(document).ready(function () {
    /*创建socket连接*/
    var socket = new WebSocket("ws://" + window.location.host + "/chatroom/");
    socket.onopen = function () {
        console.log('WebSocket open');//成功连接上Websocket
     };
    socket.onmessage = function (e) {
        var userid = $('#userid').val();
        // console.log('message: ' + e.data);//打印出服务端返回过来的数据
        var obj = JSON.parse(e.data);
        if(obj.type == "new_msg"){
            if (obj.userid == userid){ 
                var line = '<div align="right" class="bubbleItem"><h5>'+obj.username
                line += '<br/><span class="bubble rightBubble">'+obj.msg
                line += '<span class="bottomLevel"></span><span class="topLevel"></span></span></h5></div>' 
            } else { 
                var line = '<div class="bubbleItem"><h5>'+obj.username
                line += '<br/><span class="bubble leftBubble">'+obj.msg
                line += '<span class="bottomLevel"></span><span class="topLevel"></span></span></h5></div>' 
            }
            $('#result').append(line);
            var div = document.getElementById('result');
            div.scrollTop = div.scrollHeight;
        }else if(obj.type == 'song_list'){
            var songArr = obj.list;
            $('#MusicArea .table table').html("");
            for(var i=0;i<songArr.length;i++){
                $('#MusicArea .table table').append($("<tr class='"+i+"'><td>"+songArr[i][0]+"</td><td>"+songArr[i][1]+"</td></tr>"));
            }
            $('#MusicArea .panel-body .table table tr').click(function(){
                $('#MusicArea .panel-body .table').css("height","400px");
                $('#MusicArea .panel-body .audio').html("<audio autoplay='autoplay' controls></audio>")
                var i=$(this).attr("class");
                var audio = $("audio")[0];
                audio.src = 'http://ws.stream.qqmusic.qq.com/C100'+songArr[i][2]+'.m4a?fromtag=0&guid=126548448';
                audio.play();
                audio.onended = playEndedHandler; 
                audio.play();
                function playEndedHandler(){ 
                    i++;
                    if(i>=songArr.length){
                        i = 0;
                    }
                    console.log(songArr[i][0]+songArr[i][1]);
                    audio.src = 'http://ws.stream.qqmusic.qq.com/C100'+songArr[i][2]+'.m4a?fromtag=0&guid=126548448';
                    audio.play(); 
                } 
            })
        }
    };
    // Call onopen directly if socket is already open
    if (socket.readyState === WebSocket.OPEN) 
        socket.onopen();
    window.s = socket;
});
$('#send').click(function () {
    var msg = $('#msg').val()
    if (msg == '' || msg.split("\n").join("") == '') {
        $("#send").popover('show');
        setTimeout(function(){ $("#send").popover('hide'); }, 1500);
    } else {
        window.s.send(msg.split("\n").join("<br/>"));
        //通过websocket发送数据
    }
    $('#msg').val('')
});
document.onkeydown=function(e){
    if(e.keyCode == 13 && e.ctrlKey){
        document.getElementById('msg').value += '\n';
    } else if(e.keyCode == 13){
        e.preventDefault();
        $('#send').click()
    }
}
$('#FuncArea .panel-body li:eq(1)').click(function(){
    $('#MusicArea').css('display','block');
});
$('#MusicArea .panel-heading a').click(function(){
    $('#MusicArea').css('display','none');
})
$('#search_song').click(function () {
    var search_name = $('#MusicArea input').val()
    window.s.send("#SS "+search_name); 
});
$('#FuncArea .panel-heading span').click(function(){
    var width = Number($('#MsgArea').css('width').substr(0,6)) +
                Number($('#FuncArea').css('width').substr(0,6));
    $('#MsgArea').css('width', width);
    $('#FuncArea').hide();
})
$('#showFunction').click(function(){
    $('#FuncArea').show();
    var width = $('#MsgArea').css('width').substr(0,4) * 0.75;
    console.log(width)
    $('#MsgArea').css('width', width);
})
