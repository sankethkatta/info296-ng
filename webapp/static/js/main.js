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
        slideLeft();
        $("#loading").animate({"opacity": 0});
   });
};

/* Slides the cards to the left */
slideLeft = function() {
    
    
    if (!($("#shopping-content:visible").is(":last-child"))) {
      
        $("#shopping-content:visible").animate({"right": "100%"}, function() {
            
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
  
    if (!($("#shopping-content:visible").is(":first-child"))) {
        $("#shopping-content:visible").animate({"left": "100%"}, function() {
            
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

var twoToThreeTransition = function() {
    STATE = 3;

}

var threeToTwoTransition = function() {
    STATE = 2;

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
            threeToTwoTransition();
        }
    })

    $(document).on("submit", ".time-step-form", function(e) {
        if (STATE === 2) {
            twoToThreeTransition();
        }
    })
    
    
    
    
    
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
