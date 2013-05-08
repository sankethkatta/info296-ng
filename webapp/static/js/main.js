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
        $("#shopping-content").append(new_list);
        $(".rec-list-wrapper").last().addClass("offset2");
        $("#loading").animate({"opacity": 0});
   });
};

/* The state machine transition
 * there are 3 transitions possible
 * 1 --> 2, 2 --> 3, 3 --> 2
 */
var oneToTwoTransition = function() {
    STATE = 2;
    $("#initial-help").animate({"right": "100%"}, function() {
        var help = this;
        
        $(this).next().animate({"left": "0%"}, function() {
            $(help).hide();
            $("#shopping-content").append(time_step_template);
            $("#shopping-content").append(step_2_help_template);
            $(".purchase-btn").addClass("disabled");
        });
    });
}

var twoToThreeTransition = function(dom, e) {
    e.preventDefault();
    STATE = 3;
    var thisDom = dom;
    
    $(".pagination-index span").html(parseInt($(".pagination-index span").html()) + 1);
    $(".step2-help-wrapper").remove();
    $(".purchase-btn").removeClass("disabled");
    $(".time-step-btn").last().prop('disabled', true);
    $(".time-step-btn").last().addClass("disabled");
    $("#loading").animate({"opacity": 100});
    
    var payload = {purchased_items: {}};
    payload.time_step_since_last_purchase = parseInt($(thisDom).find(".time-step-input").val());
    
    $(".rec-list-wrapper").last().find(".todo-done").each(function() {
        payload.purchased_items[$(this).data("group_id")] = parseInt($(this).find(".quantity_input").val());
    });
    console.log(payload)
    update(JSON.stringify(payload));
}

var threeToTwoTransition = function(dom) {
    STATE = 2;
    var thisDom = dom;

    $(".rec-list-wrapper").last().prev().prev().animate({"right": "100%"}, function() {
        $(this).hide();
        $(".time-step-wrapper").last().animate({"right": "100%"}, function() {
            $(this).hide();
            $(".purchase-btn").addClass("disabled");
            $(".rec-list-wrapper").last().removeClass("offset2");
            $("#shopping-content").append(time_step_template);
            $("#shopping-content").append(step_2_help_template);
        });
    });

}

/* Following runs on document ready */
$(document).ready(function() {

    STATE = 1;
    time_step_template = $("#time_step_template").html(); 
    step_2_help_template = $("#step_2_help_template").html();
    /* Triggers transitions */
    $(document).on("click", ".purchase-btn", function(e) {
        if (STATE === 1) {
            oneToTwoTransition();
        } else if (STATE === 3) {
            threeToTwoTransition(this);
        }
    })

    $(document).on("submit", ".time-step-form", function(e) {
        if (STATE === 2) {
            twoToThreeTransition(this, e);
        }
    })

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

    $(document).on("click", ".timeadd", function(e) {
       var input = $(this).parents(".sub-wrapper").find(".time-step-input") 
       int_input = parseInt(input.val());
       input.val(int_input + 1); 
    });

    $(document).on("click", ".timesub", function(e) {
       var input = $(this).parents(".sub-wrapper").find(".time-step-input") 
       int_input = parseInt(input.val());
       if (int_input > 1) {
           input.val(int_input - 1); 
       }
    });
    /* Bind arrow clicks to slide functions */
    $(document).on("click", ".btn-previous", function() {
        slideRight();
    });

    $(document).on("click", ".btn-next", function() {
        slideLeft();
    })
});
