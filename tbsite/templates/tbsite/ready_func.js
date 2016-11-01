<script type="text/javascript">

// not good to sleep.... BUT
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

$(document).ready(function(){

  $("#res").hide();

  $('#main_table').dataTable( {
        "scrollX": true,
        "bAutoWidth": false,
        dom: 'Blfrtip',
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10', '25', '50', 'all' ]
        ],
  } );

  $('#main_table tbody').on( 'click', 'td', function () {
    if ( $(this).hasClass("c_sel") ){
      cl = $(this).attr("class").split(" ")[0]
      /*alert(cl);*/
      if ( $("."+cl).hasClass('my_bblue') ) {
          $("."+cl).removeClass('my_bblue');
      }
      else {
          $("."+cl).addClass('my_bblue');
      }
    }
  } );

});

//For getting CSRF token
function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
             }
          }
      }
 return cookieValue;
}

$("#add_els").click(function(e) {

  if ( !$(this).hasClass("my_disabled") ){
    lid = window.location.href.split("/")[4];
    alert(lid);
    window.location.href = "/listadd/"+lid+"/";
    return false;
  }

});


$("#save_list").click(function(e) {

  if ( !$(this).hasClass("my_disabled") ){

    e.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.ajax({
            url : window.location.href, // the endpoint,commonly same url
            type : "POST", // http method
            data : { 
              csrfmiddlewaretoken : csrftoken,
              cmd: 1
            }, 

     // handle a successful response
     success : function(json) {
        console.log(json); // another sanity check
        if ( json.resMsg.length ) {
          $("#res").show();
          $("#res").html(json.resMsg);
        }
        else{
          window.location.href = "/listmgr/"+json.id.toString()+"/";
        }
     },

     // handle a non-successful response
     error : function(xhr,errmsg,err) {
       console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
     }
     });
  }
});

$("#del_els").click(function(e) {


  if ( !$(this).hasClass("my_disabled") ){

    var ids = "";

    $(".my_bblue").each(function (index, value) {
      cll = $(this).attr('class');
      if ( cll.indexOf("cs_")>=0 ){
        ist = cll.indexOf("cs_");
        ifn = cll.indexOf(" ",ist);
        anId = cll.substr(ist+3,ifn-ist-3);
        ids += anId + " ";
      }
    });

    alert(ids);

    e.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.ajax({
            url : window.location.href, // the endpoint,commonly same url
            type : "POST", // http method
            data : { 
              csrfmiddlewaretoken : csrftoken,
              idls: ids, 
              cmd: 2
            }, 

     // handle a successful response
     success : function(json) {
        console.log(json); // another sanity check
        if ( json.resMsg.length ) {
          $("#res").show();
          $("#res").html(json.resMsg);
        }
        else{
          window.location.href = "/listadd/"+json.id.toString()+"/";
        }
     },

     // handle a non-successful response
     error : function(xhr,errmsg,err) {
       console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
     }
     });
  }
});

// SAVE TESTS
$("#save_tests").click(function(e) {

  e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  // var subj = $("#inputWhat").val();
  $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { 
            csrfmiddlewaretoken : csrftoken,
            cmd: 1
          }, // data sent with the post request

   // handle a successful response
   success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
     $("#res").show();
     $("#res").html(json.resMsg);
   },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });
  
});

// START PROJECT
$("#start_proj").click(function(e) {

  e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  // var subj = $("#inputWhat").val();
  $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { 
            csrfmiddlewaretoken : csrftoken,
            cmd: 2,
            pid: pid,
            fid: fid
          }, // data sent with the post request

   // handle a successful response
   success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
     $("#res").show();
     $("#res").html("Протокол выполнения тестов:\n\n" + json.resMsg);
     pid = json.pid;
     fid = json.fid;
     if ( json.run==1 || json.run==2 ){
       $("#start_proj").html("REFRESH");
     } 
     if ( json.run==0 ){
      $("#start_proj").html("FINISHED");
      $("#start_proj").prop("disabled",true);
    }
   },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });
  
});

// SHOW REPORT
$("#show_reports").click(function() {

  window.open(window.location.href + "/rep/");
  return false;

});

// NEW 
$("#new_project").click(function(e) {

  e.preventDefault();

  window.open("/project/0/");
  return false;
  
});

// TESTS ======================================================================

// does actual save work (for checkins and checkouts as well)
function doSaveWork(e,aCmd){

  e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  editor.save();
  var tst_name = $("#InputName").val();
  var tst_code = $("#InputCode").val();
  var tst_user = $("#InputUser").val();
  var tst_docu = $("#InputDocu").val();
  var tst_body = $("#InputBody").val();
  var tst_opts = $("#InputOpts").val();
  var tags = "";
  $(".tg_btn:not(:hidden)").each(function() {
    tags += $(this).attr('did')+" ";
  });
  var libs = "";
  $(".lib_btn:not(:hidden)").each(function() {
    libs += $(this).attr('did')+" ";
  });
  var ress = "";
  $(".res_btn:not(:hidden)").each(function() {
    ress += $(this).attr('did')+" ";
  });
  var ifs = "";
  $(".if_btn:not(:hidden)").each(function() {
    ifs += $(this).attr('did')+" ";
  });
  $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { 
            csrfmiddlewaretoken : csrftoken,
            name: tst_name,
            code: tst_code,
            user: tst_user,
            docu: tst_docu,
            body: tst_body,
            opts: tst_opts,
            ts: tags,
            ls: libs,
            rs: ress,
            ifs: ifs,            
            cmd: aCmd
          }, // data sent with the post request

   // handle a successful response
   success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
      $("#res").show();
      $("#res").html(json.resMsg);
      if ( aCmd==5 || aCmd==4 ){ // checkin/checkout: redirect
        window.location.href = "/test/"+json.id.toString()+"/";
      }
      if ( json.nt && json.id>0 ) // newneed to redirect to actaul page with new test
        window.location.href = "/test/"+json.id.toString()+"/";
   },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });

}

// SAVE 
$("#save_test").click(function(e) {

  doSaveWork(e,1);

});

// CHECKIN 
$("#checkin_test").click(function(e) {

  doSaveWork(e,4);

});

// CHECKOUT
$("#checkout_test").click(function(e) {

  doSaveWork(e,5);

});

// DELETE
$("#del_test").click(function(e) {

  e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { 
            csrfmiddlewaretoken : csrftoken,
            cmd: 3
          }, // data sent with the post request

   // handle a successful response
  success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
      alert(json.resMsg + ", Вы будете перенаправлены на страницу со списком тестов");
      window.location.href = "/testlist/";
  },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });
  
});

// NEW 
$("#new_test").click(function(e) {

  e.preventDefault();

  window.open("/test/0/");
  return false;
  
});

// START TEST
$("#start_test").click(function(e) {

  e.preventDefault();
  var csrftoken = getCookie('csrftoken');

  //Collect data from fields
  // var subj = $("#inputWhat").val();
  $.ajax({
          url : window.location.href, // the endpoint,commonly same url
          type : "POST", // http method
          data : { 
            csrfmiddlewaretoken : csrftoken,
            pid: pid,
            fid: fid,
            cmd: 2
          }, // data sent with the post request

   // handle a successful response
   success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
      $("#res").show();
      $("#res").html("Протокол выполнения тестов:\n\n" + json.resMsg);
      pid = json.pid;
      fid = json.fid;
      $("#FID").val(fid); // save for report
     if ( json.run==1 || json.run==2 ){
       $("#start_test").html("REFRESH");
       $("#page_descr").html("Для обновления результатов теста нажмите <b>REFRESH</b>");
     } 
     if ( json.run==0 ){
      $("#page_descr").html("Выполнение тестов закончилось.");
      $("#start_test").html("FINISHED");
      $("#start_test").prop("disabled",true);
    }
   },

   // handle a non-successful response
   error : function(xhr,errmsg,err) {
     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
   });
  
});

// SHOW REPORT
$("#show_test_rep").click(function() {

  var fid = $("#FID").val();
  window.open(window.location.href + fid + "/rep/");
  return false;

});

// working with test tag-like attributes (libs, ress, ifaces)

function shideItem(hd, sh, ii){
  $("#"+hd+"_"+ii).hide();
  $("#"+sh+"_"+ii).show();
}

// click edit button
function editList ( ii ){  // тип = число, тип действия определяется текстом кнопки...

  if ( $("#"+ii).html()=="Edit" ){
    $(".badge").show();
    $(".dep_edit").show();
    $("#"+ii).html("Done");
    $(".tag_btn").prop("disabled", false);
  }
  else{
    $(".badge").hide();
    $(".dep_edit").hide();
    $("#"+ii).html("Edit");
    $(".tag_btn").prop("disabled", true);
  }

}

// CODEMIRROR STAFF
var curW;

function checkInp2(as) {  // для наших переменных: индекс 2!
    return curW.length==0 || as.indexOf(curW)==2;
}
function checkInp(as) {
    return curW.length==0 || as.indexOf(curW)==0;
}

function hSet( n ){
  CodeMirror.registerHelper("hint", "anyword", function(editor, options) {
    var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
    var end = cur.ch, start = end;

    curW = curLine.substring(curLine.lastIndexOf(" ",start)+1,end).trim();

    switch (n){
      case 1:
        var list = list1;
        break;
      case 2:
        var list = list2;
        break;
      default:
        var list = list3;
        break;
    }
    if (n==3)
      return {list: list.filter(checkInp), from: CodeMirror.Pos(cur.line, start-curW.length), to: CodeMirror.Pos(cur.line, end)};
    else
      return {list: list.filter(checkInp2), from: CodeMirror.Pos(cur.line, start-curW.length), to: CodeMirror.Pos(cur.line, end)};
  });
}

CodeMirror.defineSimpleMode("simplemode", {
  // The start state contains the rules that are intially used
  start: [
    // The regex matches the token, the token property contains the type
    {regex: /"(?:[^\\]|\\.)*?"/, token: "string"},
    {regex: /'(?:[^\\]|\\.)*?'/, token: "string"},
    // Rules are matched in the order in which they appear, so there is
    // no ambiguity between this one and the one above
    {regex: /(?:1var1|1else1)\b/, token: "error"},  /* сюда пытался запихнуть слова - не понял как */
    {regex: /^([A-Za-z\u0410-\u044f]+[ 0-9A-Za-z\u0410-\u044f]+)/, token: "keyword", sol: true},  /* не работает */
    {regex: /true|false|null|undefined/, token: "atom"},
    {regex: /\#.*/, token: "comment"},
    {regex: /[-+\/*=<>!]+/, token: "operator"},
    {regex: /\$\{([A-Z$]|[a-z$]|[ \.:]|\d|[\u0410-\u044f])*\}/, token: "number"},
    // You can embed other modes with the mode property. This rule
    // causes all code between << and >> to be highlighted with the XML
    // mode.
  ],
  // The meta property contains global information about the mode. It
  // can contain properties like lineComment, which are supported by
  // all modes, and also directives like dontIndentStates, which are
  // specific to simple modes.
  meta: {
    dontIndentStates: ["comment"],
    lineComment: "\#"
  }
});

var editor = CodeMirror.fromTextArea(document.getElementById("InputBody"), {
  lineNumbers: true,
  theme: "eclipse",
  mode: "simplemode",
  extraKeys: { 
    "Alt-W": function(cm) {
      $("#menu").hide();
      cm.setOption("fullScreen", !cm.getOption("fullScreen"));
    },
    "Alt-Q": function(cm) {
      $("#menu").show();
      if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
    },
    "Alt-A": function(cm){        
      hSet(1);
      CodeMirror.showHint(cm);
    },
    "Alt-S": function(cm){        
      hSet(2);
      CodeMirror.showHint(cm);
    },
    "Alt-Z": function(cm){      
      hSet(3);
      CodeMirror.showHint(cm);
    }
  }
});

</script>

