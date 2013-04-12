var update = function(payload) {
    $.ajax({
        url: "/update",
        method: "POST",
        contentType: "application/json",
        data: payload,
    }).done(function(new_list) {
        $("#lists").append(new_list);
        slideLeft();
        $("#loading").animate({"opacity": 0});
   });
};

slideLeft = function() {
    if (!($(".rec-form:visible").is(":last-child"))) {
        $(".rec-form:visible").animate({"right": "100%"}, function() {
            $(this).hide();
            $(this).next().show();
            $(this).next().animate({"left": "0%"});
        });
        var index = $("#pagination-index span");
        index.html(parseInt(index.html()) + 1);
    }
};

slideRight = function() {
    if (!($(".rec-form:visible").is(":first-child"))) {
        $(".rec-form:visible").animate({"left": "100%"}, function() {
            $(this).hide();
            $(this).prev().show();
            $(this).prev().animate({"right": "0%"});
        });
        var index = $("#pagination-index span");
        index.html(parseInt(index.html()) - 1);
    }
};


$(document).ready(function() {
    $(document).on("submit", ".rec-form", function(e) {
        e.preventDefault();
        if (!($(this).find(".purchase-btn").hasClass("disabled"))) {
            var payload = {purchased_list: []};
            payload.customer_lnr = $(this).find(".todo-search-field").val()
            $(this).find(".todo-done").each(function() {
                payload.purchased_list.push($(this).data("name"))
            });
            $(this).find(".purchase-btn").val("PURCHASED");
            $(this).find(".purchase-btn").addClass("disabled");
            update(JSON.stringify(payload));

            $("#loading").animate({"opacity": 100});
        }
    });

    $(document).on("click", ".recommendation-item", function(e) {
        if ($(this).hasClass("todo-done")) {
            $(this).removeClass("todo-done");
        } else {
            $(this).addClass("todo-done");
        }
    });

    $(document).on("click", ".previous", function() {
        slideRight();
    });

    $(document).on("click", ".next", function() {
        slideLeft();
    })
});