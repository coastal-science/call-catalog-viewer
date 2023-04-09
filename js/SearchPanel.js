var SearchPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var originalData = undefined;
    var tmpResult = undefined;
    var s_options = {};
    var num_dropdowns;
    var dirty = false;
    var s_index = 1;
    var element_id_to_title = {};

    const LIBRARY = 'catalogs';
    const LIBRARY_INDEX = 'index.yaml';

    function pack_option(v) {
        return '<option value="' + v + '">' + v + '</option>'
    }

    /**
     * Update the s_options values to contain the variable data passed through url
     * @param {object} filter_options object of key value pairs where the key is the thing to filter on and the values are the possible values
     */
    function updateFilterOptions(filter_options) {
        
        console.log("FILTER OPTIONS: " + JSON.stringify(filter_options));
        // construct the object and then add it to the s_options
        let count = 1;
        var keys = Object.keys(filter_options);
        keys.forEach((key) => {
            // if this is 'population' then things are simple, add everything we need as array of values
            // if it is not, then it is populatoin specific filters and we need to be more careful
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
                // handling the population specific filters
                var dropdown_keys = Object.keys(filter_options[key][1]);

                console.log(filter_options[key][0]);
                console.log("DROPPIES: " + dropdown_keys);
                dropdown_keys.forEach((drop_key) => {
                    var obj = {};

                    // set all of the values that we need
                    obj.s = "s" + count;
                    obj.b = "b" + count;
                    obj.display = 's' + count;

                    obj.title = drop_key;

                    element_id_to_title['s' + count] = obj.title;

                    // create an array of all of the values
                    const arr = [];
                    filter_options[key][1][drop_key].forEach((value) => {
                        arr.push(value);
                    });
                    obj.values = arr;

                    if (!(s_options[population_value]))
                        s_options[population_value] = [];
                    
                    s_options[population_value].push(obj);
                    count++;
                    console.log("KEY" + drop_key);
                })
            } 
        });
        num_dropdowns = count;
        console.log("OPTIONS: " + JSON.stringify(s_options[2]));
    }

    /**
     * create an HTML representation of the dropdown to append to the panel
     * @param {string} title the title of the dropdown to put next to it
     * @param {string} id the id to the dropdown in html
     */
    function pack_dropdown(title, id) {
        title = title.charAt(0).toUpperCase() + title.slice(1);

        if (title === 'Population') {
            return '<div class="col col-12 col-sm-12 col-md-12 col-lg-12 col-xl-10 col-xxl-10 align-items-center align-middle align-right d-flex flex-nowrap">' + 
                    '<span class="col-4 text-end">' + title  + ': &nbsp;</span>' +
                    '<select id="' + id + '" class="col-8" aria-label="size 3 select">' +
                    '</select><br>&nbsp;' +
                '</div>'
        }

        return '<div class="col col-12 col-sm-12 col-md-12 col-lg-12 col-xl-10 col-xxl-10 align-items-center align-middle align-right d-flex flex-nowrap">' + 
                    '<span class="col-4 text-end">' + title  + ': &nbsp;</span>' +
                    '<select id="' + id + '" class="col-8" multiple aria-label="size 3 select">' +
                    '</select><br>&nbsp;' +
                '</div>'
    }

    function fileExists(url) {
        exists = false;

        $.ajax({
            url: url,
            type:'HEAD',
            async: false,
            error: function() 
            {
                exists = false;
            },
            success: function()
            {
                exists = true;
            }
        });

        return exists;
    }

    async function init() {
        originalData = {};

        var queryString = location.search;
        urlParams = new URLSearchParams(queryString);

        // check whether the index.yaml exists. This stops just constant refreshing on an empty catalog
        url = LIBRARY + '/' + LIBRARY_INDEX;
        if (!fileExists(url))
            return;
        // if the values have not already been set in the GridPanel line 300-310 then wait 500 milliseconds for them to get set, and then refresh the page 
        if (!urlParams.has('f')) {
            await sleep(300);
            setTimeout(function() {
                queryString = location.search;
                urlParams = new URLSearchParams(queryString);
                location.reload();
            }, 500)
        }

        if (urlParams.has('f')) {
            const filter = urlParams.get('f');
            const obj = atob(filter);

            console.log("OBJ: " + obj);
            if (obj !== undefined) {
                try {
                    const ev = eval('(' + obj + ')');
                    let count = 1;
                    Object.keys(ev).forEach((item) => {
                        if (!['s1', 's2', 's3'].includes(item)) {
                            var list = [item];
                            list = list.concat(ev[item]);
                            originalData['s' + count] = list; // set data using s1, s2, s3.... notation for easier access later
                            element_id_to_title['s' + count] = item;
                            count++;
                        }
                    });
                } catch (e) {
                    console.log(e);
                }
            }
        } else {
            
        }

        updateFilterOptions(originalData);
        
        tmpResult = {}
        // tmpResult = $.extend(true, {}, originalData);
        Panel = $('.panel');
        Panel.find("#search_rows").empty(); // clear the search rows panel so that we can append the data

        buildPopulationDropdown();
        bindEvents();
        // buildPopulationSpecificDropdown(selected_value);
    };
    panel.init = init;

    /**
     * blocking sleep function used to wait for filters to come through
     * @param {int} ms number of milliseconds to sleep
     * @returns 
     */
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * create and set listeners for all of the dropdowns 
     */
    function bindEvents() {
        // for the number of values, in s_options, do this thing
        for (let i = 1; i <= num_dropdowns; i++) {
            var object = s_options[i-1];
            $('#s' + i).on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => { // sets the listener when dropdowns are changed
                var title = element_id_to_title['s' + i];

                if (tmpResult[title] === undefined)     
                    tmpResult[title] = []
                tmpResult[element_id_to_title['s' + i]] = $('#s' + i).selectpicker('val');

                
                if (element_id_to_title['s' + i] === 'population'){
                    tmpResult['population'] = $('#s' + i).val();
                    buildPopulationSpecificDropdown($('#s' + i).val());
                }
                // buildPopulationSpecificDropdown($('#s' + i).val());
            });
        }
        Panel.find('#search_now').off('click').click(function (e) { // function that is called when the filter button is clicked. 
            dirty = false;
            originalData = $.extend(true, {}, tmpResult);
            console.log("PASSING NEW: " + JSON.stringify(originalData));
            GridPanel.get_new(originalData);
        });

        Panel.find('#retrieve_data').off('click').click(function (e) {
            var tab = window.open("about:blank", "_blank");
            tab.document.body.innerHTML = "<pre>" + JSON.stringify(window.entireFilterData) + "</pre>";
        });
    }

    /**
     * This builds the population dropdown as a single selecteable dropdown
     * Changes to this dropdown will result in changes to the dropdowns displayed to reflect 
     */
    function buildPopulationDropdown(last_value) {
        Panel = $('.panel');
        // find the population dropdown from all of the options
        var population_data = s_options['population'];
        
        // create the dropdown
        Panel.find('#search_rows').append(pack_dropdown(population_data.title, population_data.s));
         
        // append all of the options
        population_data.values.forEach((value) => {
            Panel.find("#" + population_data.s).append(pack_option(value));
        });

        $('#' + population_data.s).val(last_value);
        $('#' + population_data.s).selectpicker('refresh');
    }

    function buildDropdown(dropdown_data) {
        console.log("DROPDOWN DATA: " + JSON.stringify(dropdown_data));
        Panel = $('.panel');

        Panel.find('#search_rows').append(pack_dropdown(dropdown_data.title, dropdown_data.s));

        dropdown_data.values.forEach((value) => {
            Panel.find('#' + dropdown_data.s).append(pack_option(value));
        })

        $('#' + dropdown_data.s).selectpicker('refresh');
    }

    function buildPopulationSpecificDropdown(selected_value) {
        Panel = $('.panel');
        Panel.find('#search_rows').empty();

        buildPopulationDropdown(selected_value);
        console.log(JSON.stringify(selected_value));

        if (s_options[selected_value] !== undefined) {
            s_options[selected_value].forEach((dropdown)=> {
                buildDropdown(dropdown);
            })
        }
            

        bindEvents();
    }
}(SearchPanel || (SearchPanel = {})));