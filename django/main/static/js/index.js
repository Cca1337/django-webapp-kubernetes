let csrftoken = getCookie('csrftoken');
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
    headers: { "X-CSRFToken": csrftoken },
  }).then((_res) => {
    window.location.href = "/notes";
  });
}

function deletePic(picId) {
  fetch("/delete-picture", {
    method: "POST",
    body: JSON.stringify({ picId: picId }),
    headers: { "X-CSRFToken": csrftoken },
  }).then((_res) => {
    window.location.href = "/obrazky_update";
  });
}



// The following function are copying from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



$(document).ready(function(){
  setTimeout(function(){$('.messages.').fadeOut();}, 5000);
  $(window).click(function(){$('.messages').fadeOut();});
});


setTimeout(function() {
    $('.messages').fadeOut('fast');
}, 5000); // <-- time in milliseconds


$(document).ready(function() {
  setTimeout(function() {
    $("#proceed").show();
  }, 21000);
});

