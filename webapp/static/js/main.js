var update = function(payload) {
    $.ajax({
        url: "/update",
        method: "POST",
        contentType: "application/json",
        data: payload,
    }).done(function(new_list) {
        $("#lists").append(new_list);
    });
};


$(document).ready(function() {
    $(document).on("submit", "form", function(e) {
        e.preventDefault();
        payload = {purchased_list: []};
        payload.customer_lnr = $(this).find(".todo-search-field").val()
        $(this).find(".todo-done").each(function() {
            payload.purchased_list.push($(this).data("name"))
        });
        update(JSON.stringify(payload));
    });

    $(document).on("click", ".recommendation-item", function(e) {
        if ($(this).hasClass("todo-done")) {
            $(this).removeClass("todo-done");
        } else {
            $(this).addClass("todo-done");
        }
    });
});