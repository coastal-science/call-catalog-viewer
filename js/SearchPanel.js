var SearchPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var originalData = undefined;
    var liveDropdownChoices = {}; // Variable to store dropdown selections for dynamic updates. As the user clicks but has not yet filtered.
    var selected_options = {}; // Store the last selection options used for filtering. Save options for each population.
    var selected_population = undefined // Variable to store the current population selection
    var s_options = {};
    var num_dropdowns;
    var dirty = false;
    var s_index = 1;
    var element_id_to_title = {};

    const LIBRARY = 'catalogs';
    const LIBRARY_INDEX = 'index.yaml';

    panel.liveDropdownChoices = liveDropdownChoices;

    async function init() {
        originalData = {};

        var queryString = location.search;
        urlParams = new URLSearchParams(queryString);

        // check whether the index.yaml exists. This stops just constant refreshing on an empty catalog
        url = LIBRARY + '/' + LIBRARY_INDEX;
        if (!fileExists(url))
            return;
        // if the values have not already been set in url 'f' parameters, wait 300ms for them to get set, and then refresh the page 
        // console.log({"waiting for variable": urlParams});
        // while (!urlParams.has('f')) {// define the condition as you like
        //     // console.log({'waiting': urlParams})
        //     await new Promise(resolve => setTimeout(resolve, 300));
        //     urlParams = new URLSearchParams(location.search);
        // }
        // console.log("waiting done. the variable is defined.");


        // the 'f' parameters have been set, 
        ev = get_params_to_obj(urlParams, 'f');
        let count = 1;
        if (ev) {
            Object.keys(ev).forEach((item) => {
                if (!['s1', 's2', 's3'].includes(item)) {
                    var list = [item];
                    list = list.concat(ev[item]);
                    originalData['s' + count] = list; // set data using s1, s2, s3.... notation for easier access later
                    element_id_to_title['s' + count] = item; // update lookup table for accessible lookup
                    count++;
                }
            });
        }

        // the 'sel' parameters, containing the user selections, has been set, 
        user_selection = get_params_to_obj(urlParams, 'sel');

        // originalData is our filters that we want to translate into dropdowns
        updateFilterOptions(originalData);

        // find the panel and clear the search rows so that we can rebuild from fresh
        Panel = $('.panel');
        Panel.find("#search_rows").empty();

        buildPopulationDropdown();
        bindEvents();
        
        if (user_selection && !jQuery.isEmptyObject(user_selection)) {
            selected_population = user_selection['population'];

            population_selector_element = $('#s1');
            
            // Update and trigger a change. Setting the value and triggering a change will 
            // trigger the same steps as a user interaction selecting the choice.
            population_selector_element.val(selected_population).change();
            //  containing the cascading steps...
            //     ...
            //     buildPopulationSpecificDropdown(selected_population)...
            //     updateURL('sel', user_selection) ...
            //     GridPanel.get_new(...)...
            
            // extract all key for dropdowns id pattern 's#' and set their corresponding value/selected choice.
            new_filters = Object.fromEntries(
                Object.entries(user_selection).
                    filter(([k,v]) => 
                        k.search(/s\d/) == 0 // must match pattern the 's#' at the beginning of the key
                    )
                )                
            for (const [key, value] of Object.entries(new_filters)) {
                console.log({key, value});
                $('#' + key).selectpicker('val', value);  // .change() is triggered automatically by bootstrap-select
            }

            // Update the url in the address bar and browser history. 
            // updateURL('sel', user_selection);
            // Trigger user interaction via the the Filter button.
            filter_btn = $('#search_now'); // filter button
            filter_btn.click();
        }
        // buildPopulationSpecificDropdown(selected_value);
    };
    panel.init = init;
    

    /**
     * URL Search parameters may contain encoded object. This function
     * extracts and decodes (`atob`) the previously stringified and encoded (`btoa`) object in the url parameter. 
     * Use `atob` to decode to a stringified object. Convert to object using `eval('(' + obj + ')')`
     * @param {urlParams} `URLSearchParams(queryString)` object
     * @param {param_name} name of parameter in the url string containing the encoded object.
     * @returns the `param_name` as an javascript object
     */
    function get_params_to_obj(urlParams, param_name) {

        if (urlParams.has(param_name)) {
            let param_value = urlParams.get(param_name);
            if (!param_value || ['null', 'undefined', 'nan'].includes(param_value.toLowerCase())) {
                // null, undefined, false, NaN, 0, ""
                param_value = btoa(JSON.stringify({}))
            }
            const obj_str = atob(param_value);

            if (obj_str !== undefined) {
                try {
                    const obj_ev = eval('(' + obj_str + ')');
                    return obj_ev;
                } catch (e) {
                    console.log(e);
                }
            }
        }
    }
    panel.get_params_to_obj = get_params_to_obj;


    /**
     * Update the URL search parameter `param_name` with the object `new_data`
     * stringify and encode (`bota`) the object `new_data` before updating the URL Search parameter
     * Update the browser `history` accordingly.
     * @param {param_name} name of the url parameter
     * @param {new_data} object to encode and store
     * @modifies {history}
     */
    function updateURL(param_name, new_data) {
        const params = new URLSearchParams(window.location.search);
        var encoded = new_data
        if (typeof(new_data) != 'string')
            encoded = btoa(JSON.stringify(new_data));
        params.set(param_name, encoded);
        const state = {};
        for (const [key, value] of params.entries()) {
            state[key] = value; // recreate state for history and url
        }
        console.log({new_data, state});
        debugger
        const title = ''; //For Safari only
        history.pushState(state, title, `${window.location.pathname}?${params}`);
    }


    /** 
     * @param {string} v value for the option in dropdown
     * @param {Boolean} selected value to indicate `selected` attribute 
     * @returns an HTML representation of the option to add
     */
    function pack_option(v, selected) {
        selected = Boolean(selected) ? 'selected' : ''
        return '<option value="' + v + '" ' + selected + '>' + v + '</option>'
    }


    /**
     * Update the s_options values to contain the variable data passed through url
     * @param {object} filter_options object of key value pairs where the key is the thing to filter on and the values are the possible values
     */
    function updateFilterOptions(filter_options) {
        // construct the object and then add it to the s_options
        let count = 1;
        var keys = Object.keys(filter_options);
        keys.forEach((key) => {
            // if this is 'population' then things are simple, add everything we need as array of values
            // if it is not, then it is population specific filters and we need to be more careful
            var population_value = filter_options[key][0];

            if (population_value === 'population') {
                var obj = {};
                // set all of the values that we need
                obj.s = "s" + count;
                obj.b = "b" + count;
                obj.display = 's' + count;

                obj.title = filter_options[key][0];

                element_id_to_title['s' + count] = obj.title;

                // create array of all of the values
                const arr = [];
                filter_options[key].slice(1).forEach((val) => {
                    arr.push(val);
                });
                obj.values = arr;

                // add to the options
                s_options.population = obj;
                // s_options.push(obj);
                count++;
            } else {
                // this means that we are looking at population specific filters

                // get the keys for to population specific, each one representing a dropdown that we need to create
                var dropdown_keys = Object.keys(filter_options[key][1]);

                dropdown_keys.forEach((drop_key) => {
                    var obj = {};

                    // set the s, b, and display values for access later
                    obj.s = "s" + count;
                    obj.b = "b" + count;
                    obj.display = 's' + count;

                    // the title of the dropdown is just the key that we are currently looking at, then for values iterate through the values for this key
                    obj.title = drop_key;

                    element_id_to_title['s' + count] = obj.title;

                    const arr = [];
                    filter_options[key][1][drop_key].forEach((value) => {
                        arr.push(value);
                    });
                    obj.values = arr;

                    // add the object to the population specific section of the s_options
                    if (!(s_options[population_value]))
                        s_options[population_value] = [];

                    s_options[population_value].push(obj);
                    count++;
                })
            }
        });
        // used when binding on changes to dropdowns
        num_dropdowns = count;
    }

    /**
     * @param {string} title the title of the dropdown to put next to it
     * @param {string} id the id to the dropdown in html
     * @returns an HTML representation of the dropdown to append to the panel
     */
    function pack_dropdown(title, id) {
        title = title.charAt(0).toUpperCase() + title.slice(1);

        if (title === 'Population') {
            return '<div class="col col-12 col-sm-12 col-md-12 col-lg-12 col-xl-10 col-xxl-10 align-items-center align-middle align-right d-flex flex-nowrap">' +
                '<span class="col-4 text-end">' + title + ': &nbsp;</span>' +
                '<select id="' + id + '" class="col-8" aria-label="size 3 select">' +
                '</select><br>&nbsp;' +
                '</div>'
        }

        return '<div class="col col-12 col-sm-12 col-md-12 col-lg-12 col-xl-10 col-xxl-10 align-items-center align-middle align-right d-flex flex-nowrap">' +
            '<span class="col-4 text-end">' + title + ': &nbsp;</span>' +
            '<select id="' + id + '" class="col-8" multiple aria-label="size 3 select">' +
            '</select><br>&nbsp;' +
            '</div>'
    }

    /**
     * @param {string} url path to file
     * @returns true if file exists, false otherwise
     */
    function fileExists(url) {
        exists = false;

        $.ajax({
            url: url,
            type: 'HEAD',
            async: false,
            error: function () {
                exists = false;
            },
            success: function () {
                exists = true;
            }
        });

        return exists;
    }

    /**
     * create and set listeners for all of the dropdowns 
     */
    function bindEvents() {
        // for the number of values, in s_options, do this thing
        for (let i = 1; i <= num_dropdowns; i++) {
            var object = s_options[i - 1];
            $('#s' + i).on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => { // sets the listener when dropdowns are changed
                var title = element_id_to_title['s' + i];
                // liveDropdownChoices holds the currently applied filters that are passed back to GridPanel in get_new calls
                if (liveDropdownChoices[title] === undefined)
                    liveDropdownChoices[title] = []
                liveDropdownChoices[element_id_to_title['s' + i]] = $('#s' + i).selectpicker('val');
                liveDropdownChoices['s' + i] = $('#s' + i).selectpicker('val');

                if (element_id_to_title['s' + i] === 'population') {
                    selected_id = '#s' + i;
                    selected_population = $(selected_id).val();
                    
                    // TODO: DESIGN CHOICE.
                    // By default, all filters cleared when population changes. 
                    // A storage feature is implemented `selection_storage` where you
                    // can change `populations` and your last filter setting restored (per population).
                    // These are two design choices.
                    // To clear all filters when the population changes, remove the Trash can button 
                    // (and all related listeners and helper functions). Or call the helper function 
                    // and retain the functionality of both (button to clear filter manually) and
                    // automatically when changing populations.

                    // clearFilter(); 

                    liveDropdownChoices = {};
                    liveDropdownChoices['population'] = selected_population;
                    // Copy pre-saved selections
                    if (selected_options[selected_population] != undefined) {
                        for (const [key, value] of Object.entries(selected_options[selected_population])) {
                            liveDropdownChoices[key] = value;
                        }
                    }
                    buildPopulationSpecificDropdown(selected_population);
                    updateURL('sel', liveDropdownChoices);
                    updateURL('catalogue', selected_population)
                    GridPanel.get_new(liveDropdownChoices);
                }
            });
        }
        Panel.find('#search_now').off('click').click(function (e) { // function that is called when the filter button is clicked. 
            dirty = false;
            originalData = $.extend(true, {}, liveDropdownChoices);
            // Copy the current filter selections for saving state
            selected_options[liveDropdownChoices['population']] = structuredClone(liveDropdownChoices)
            updateURL('sel', liveDropdownChoices);
            GridPanel.get_new(liveDropdownChoices);
            toggle_button(this, 100);
        });

        Panel.find('#retrieve_data').off('click').click(function (e) {
            var tab = window.open("about:blank", "_blank");
            tab.document.body.innerHTML = "<pre>" + JSON.stringify(window.entireFilterData) + "</pre>";
        });
    }

    /**
     * Builds the population dropdown populates it with values
     * Tracks the selection in 'selected_value' so that it doesn't total reset when we rebuild 
     */
    function buildPopulationDropdown(last_value) {
        var population_data = s_options['population'];

        Panel.find('#search_rows').append(pack_dropdown(population_data.title, population_data.s));

        population_data.values.forEach((value) => {
            Panel.find("#" + population_data.s).append(pack_option(value));
        });

        $('#' + population_data.s).val(last_value);
        $('#' + population_data.s).selectpicker('refresh');
    }

    /**
     * build the dropdown and append it to the searching panel
     * Duplicate `dropdown_data` or `selected_values` will be marked as 'selected'
     * @param {Object} dropdown_data data representing the dropdown to create
     * @param {Object} selected_values array representing the values from `dropdown_data` have the attribute selected. 
     */
    function buildDropdown(dropdown_data, selected_values) {
        Panel.find('#search_rows').append(pack_dropdown(dropdown_data.title, dropdown_data.s));

        dropdown_data.values.forEach((value) => {
            select = undefined
            if (selected_values != undefined)
                select = selected_values.includes(value)

            Panel.find('#' + dropdown_data.s).append(pack_option(value, select));
        })

        $('#' + dropdown_data.s).selectpicker('refresh');
    }

    /**
     * @param {string} population population value to construct all of the required dropdowns for
     */
    function buildPopulationSpecificDropdown(population) {
        if (population === undefined) {
            console.error("buildPopulationSpecificDropdown attempting to build `population=undefined`");
            return
        }
        Panel.find('#search_rows').empty();
        buildPopulationDropdown(population);
        console.log(JSON.stringify(population));
        if (s_options[population] !== undefined) {
            s_options[population].forEach((dropdown) => {
                dropdown_selected_value = get_population_selection_from_storage(population, dropdown);
                buildDropdown(dropdown, dropdown_selected_values);
            })
        }


        bindEvents();
    };

    /**
     * @param {string} population Title of the population dropdown.
     * @param {string} dropdown Corresponding dropdown (single) entry from `s_options[population]`.
     * @returns Array of already user-selected options (values only) from `selection_storage[population]` if it exists, otherwise an empty array.
     */
    function get_population_selection_from_storage(population, dropdown) {
        dropdown_selected_values = [];
        if (selected_options[population]) {
            dropdown_selected_values = selected_options[population][dropdown.title];
            dropdown.s;
            dropdown.title;
            console.log({ dropdown, dropdown_selected_values });
            // $('#' + dropdown_data.s).attr("selected","selected");
        }
        return dropdown_selected_values;
    }
    
    /**
     * Clears the displayed filter options for the currently selected_population. 
     * Clears from the selection_storage, and triggers to `buildPopulationSpecificDropdown()`.
     */
    function clearFilter() {
        console.log({selected_population, selected_options})
        if (selected_population != undefined && selected_options != undefined) {
            delete selected_options[selected_population]
            liveDropdownChoices = {}
            liveDropdownChoices['population'] = selected_population
            buildPopulationSpecificDropdown(selected_population)
        }
    };
    panel.clearFilter = clearFilter;

}(SearchPanel || (SearchPanel = {})));