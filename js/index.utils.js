    // Used to toggle the menu on small screens when clicking on the menu button
    function myFunction() {
        var x = document.getElementById("navDemo");
        if (x.className.indexOf("w3-show") == -1) {
            x.className += " w3-show";
        } else {
            x.className = x.className.replace(" w3-show", "");
        }
    }

    function showAllOnly() {
        var show_all = document.getElementById("show-all");
        var show_only = document.getElementById("show-only");

        if (show_all.checked == true) {
            show_only.disabled = true
        } else {
            show_only.disabled = false
        }
    }

    //Get the button
    let buttonToTop = document.getElementById("btn-back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (
            document.body.scrollTop > 20 ||
            document.documentElement.scrollTop > 20
        ) {
            buttonToTop.style.display = "block";
        } else {
            buttonToTop.style.display = "none";
        }
    }

    // When the user clicks on the button, scroll to the top of the document
    buttonToTop.addEventListener("click", scrollBackToTop);
    function scrollBackToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }

    // buttonToTop.addEventListener("click", scrollBackToResults);
    function scrollBackToResults() {
        $('html, body').animate({
            scrollTop: $("#resultgrid").offset().top
        }, 0);
    }

    // buttonToTop.addEventListener("click", scrollBackToSearch);
    function scrollBackToSearch() {
        $('html, body').animate({
            scrollTop: $("#search_now").offset().top
        }, 0);
    }

    $(async function () {
        await GridPanel.init();
        SearchPanel.init();
    })
    
    //Get the button
    let clear_filter = document.getElementById("clear_filter");

    // When the user clicks on the button, clear the selected filters options
    clear_filter.addEventListener("click", clearFilter);
    function clearFilter(event) {
        event.preventDefault(); // To prevent following the link (optional)
        SearchPanel.clearFilter();
        toggle_button(this, 100);
    }

    /* Bootstrap buttons are being used for user input without a <form>. This is a tightly coupled design choice.
     * Bootstrap buttons are focused (css) when clicked. The css restores when you click on another item. This 
     * does not give the appearance of submitting and resubmitting input.
     * The Bootstrap-safe and accessibly-safe way is to .blur() the button after a click event. 
     *
     * @param button The HTML button object on which `.blur()` will be called after timeout_delay milliseconds,
     * @param timeout_delay milliseconds timeout delay for fluctuating the button.
     */
    function toggle_button(button, timeout_delay) {
        setTimeout(function() {
            button.blur() // The bootstrap-safe way to disable the highlighted css
        }.bind(button), timeout_delay);
    }
