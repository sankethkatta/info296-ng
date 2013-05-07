/* Ajax Update function
 * takes a json payload and POSTs to /update
 */
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

/* Slides the cards to the left */
slideLeft = function() {
    if (!($(".rec-form:visible").is(":last-child"))) {
        $(".rec-form:visible").animate({"right": "100%"}, function() {
            $(this).hide();
            $(this).next().show();
            $(this).next().animate({"left": "0%"}, function() {
                $(this).css("left", "auto");
            });
        });
        var index = $(".pagination-index span");
        index.html(parseInt(index.html()) + 1);
    }
};

/* Slides the cards to the right */
slideRight = function() {
    if (!($(".rec-form:visible").is(":first-child"))) {
        $(".rec-form:visible").animate({"left": "100%"}, function() {
            $(this).hide();
            $(this).prev().show();
            $(this).prev().animate({"right": "0%"}, function() {
                $(this).css("right", "auto");
            });
        });
        var index = $(".pagination-index span");
        index.html(parseInt(index.html()) - 1);
    }
};

/* The state machine transition
 * there are 3 transitions possible
 * 1 --> 2, 2 --> 3, 3 --> 2
 */
var transition = function() {
    if (STATE === 1) {
        STATE = 2;
        /* TRANSITION FROM 1 --> 2 */

    } else if (STATE === 2) {
        STATE = 3;
        /* TRANSITION FROM 2 --> 3 */

    } else if (STATE === 3) {
        STATE = 2;
        /* TRANSITION FROM 3 --> 2 */
    }
}

/* Following runs on document ready */
$(document).ready(function() {

var STATE = 1;

    /* On purchase */
    $(document).on("submit", ".rec-form", function(e) {
        e.preventDefault();
        if (!($(this).find(".purchase-btn").hasClass("disabled"))) {
            var payload = {purchased_items: {}};
            payload.customer_lnr = $(this).find(".todo-search-field").val();
            payload.time_step_since_last_purchase = $(this).find(".time-step-input").val()

            $(this).find(".todo-done").each(function() {
                payload.purchased_items[$(this).data("group_id")] = {quantity: $(this).data("quantity")}
            });

            $(this).find(".purchase-btn").val("PURCHASED");
            $(this).find(".purchase-btn").addClass("disabled");
            $(this).find(".time-step-input").attr("disabled", "disabled");
            console.log(payload)
            update(JSON.stringify(payload));

            $("#loading").animate({"opacity": 100});
        }
    });

    /* On item click */
    $(document).on("click", ".add", function(e) {
       var input = $(this).parents(".quantity").find(".quantity_input") 
       int_input = parseInt(input.val());
       input.val(int_input + 1); 
       $(this).parents(".recommendation-item").addClass("todo-done");
    });

    $(document).on("click", ".sub", function(e) {
       var input = $(this).parents(".quantity").find(".quantity_input") 
       int_input = parseInt(input.val());
       if (int_input > 0) {
           input.val(int_input - 1); 
           if (int_input - 1 === 0) {
              $(this).parents(".recommendation-item").removeClass("todo-done");
           }
       } else if (int_input === 0){
          $(this).parents(".recommendation-item").removeClass("todo-done");
       }
    });

    /* Bind arrow clicks to slide functions */
    $(document).on("click", ".previous", function() {
        slideRight();
    });

    $(document).on("click", ".next", function() {
        slideLeft();
    })
});
