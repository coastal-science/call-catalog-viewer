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
    
    String.prototype.toTitleCase = function () {
        return this.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase(); });
    };
    
    function flattenObj(obj) {
        // https://medium.com/@vickdayaram/flatten-a-dictionary-a5fa4426bf9d
        let flat = {}
            for(let i in obj) {
                if(typeof obj[i] == 'object') {
                    let flatObj = flattenObj(obj[i])
                    for(let x in flatObj){
                        flat[i + "." + x] = flatObj[x]
                    }
                } else {
                    flat[i] = obj[i]
                }
            }
        return flat
    }

    Object.filter = (obj, predicate) => 
                Object.fromEntries(Object.entries(obj).filter(predicate));

    function find_object_key_match(search_str){
        
        if (this[search_str]) {
            // `str.match(search_str="")` is the same as matching regex `search_str="*"`, 
            // which will match with any value,
            // handle this case and exact keys without searching.
            return {search_str: this[search_str]}
        }
        
        results = Object.filter(this, ([key, value]) => key.match(search_str));
        
        if(!results || jQuery.isEmptyObject(results)){
            return {'': ''}
            // return {'': 'Nothing is selected'}
        }
        return results
    }

    function find_object_value_match(search_str){
        if(!search_str || jQuery.isEmptyObject(search_str) ){
            return null
        }

        // if (this[search_str]) {
        //     // `str.match(search_str="")` is the same as matching regex `search_str="*"`, 
        //     // which will match with any value,
        //     // handle this case and exact keys without searching.
        //     return {search_str: this[search_str]}
        // }
        
        // results = Object.filter(Object.values(this), ([value]) => value ? JSON.stringify(value).match("/"
        //     + search_str +"/") : null);

        results = Object.filter(Object.entries(this), ([key, value]) => {
        // results = Object.filter(Object.entries(this), ([k,v]) => {
            console.log({search_str, 'obj': JSON.stringify(value), key});
            // value[0] is the key from taxonomy dictionary
            // value[1] is the value
            // key is the sequential index
            debugger
            if (typeof(value[1]) == 'string' && value[1].toLowerCase() === search_str.toLowerCase() ){
                return true;
            }
            return false;
               
        });

        console.log({results})
        if(!results || jQuery.isEmptyObject(results)) {
            return {'': ''}
            // return {'': 'Nothing is selected'}
        }
        return results
    }
