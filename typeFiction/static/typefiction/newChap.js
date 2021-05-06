
$("#new-chapter-btn").click(function(){
    $("#new-chapter-form").toggleClass("d-none")
    const word = $('#new-chapter-btn').text();
    $('#new-chapter-btn').text(
        word == "Add New Chapter" ? "Close" : "Add New Chapter");
})
