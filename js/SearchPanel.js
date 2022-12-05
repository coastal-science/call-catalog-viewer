var SearchPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var originalData = undefined;
    var tmpResult = undefined;
    var s_options = [
        // {
        //     "s": "s1",
        //     "b": "b1",
        //     "option": [
        //         { "v": "SRKW", "text": "Southern Resident" },
        //         { "v": "NRKW", "text": "Northern Resident" },
        //         { "v": "T", "text": "Transient" },
        //     ]
        // },
        // {
        //     "s": "s2",
        //     "b": "b2",
        //     "option": [
        //         { "v": "J", "text": "J" }
        //     ]
        // },
        // {
        //     "s": "s3",
        //     "b": "b3",
        //     "option": [
        //         { "v": "J", "text": "J" },
        //         { "v": "K", "text": "K" },
        //         { "v": "L", "text": "L" },
        //     ]
        // }
    ];
    var dirty = false;
    var s_index = 1;
    var element_id_to_title = {};

    const LIBRARY = 'catalogs';
    const LIBRARY_INDEX = 'index.yaml';

    function pack_option(v, a) {
        return '<option value="' + v + '">' + a + '</option>'
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
            var obj = {};
            // for compatibility
            obj.s = "s" + count;
            obj.b = "b" + count;
            obj.display = key;

            const arr = []
            filter_options[key].forEach((val) => {
                var temp = {}
                temp.v = val;  
                temp.text = val;
                arr.push(temp);  
            });
            obj.option = arr;
            s_options.push(obj);
            count++;
        });
    }

    /**
     * create html representation of the dropdown to append to the panel
     * @param {string} value the id of the panel to add s1, s2, s3.... 
     * @returns html representation of dropdown to append to the panel
     */
    function pack_dropdown(value) {
        return '<div class="col col-12 col-sm-12 col-md-12 col-lg-12 col-xl-10 col-xxl-10 align-items-center align-middle align-right d-flex flex-nowrap">' + 
                    '<span class="col-4 text-end">' + element_id_to_title[value]  + ': &nbsp;</span>' +
                    '<select id="' + value + '" class="col-8" multiple aria-label="size 3 select">' +
                    '</select><br>&nbsp;' +
                '</div>'
    }

    function init() {
        originalData = {
            // s1: ["SRKW", "NRKW"],
            // s2: ["J"],
            // s3: ["J", "K", "L"],
        };

        var queryString = location.search;
        urlParams = new URLSearchParams(queryString);

        // if the values have not already been set in the GridPanel line 300-310 then wait 500 milliseconds for them to get set, and then refresh the page 
        if (!urlParams.has('f')) {
            setTimeout(function() {
                queryString = location.search;
                urlParams = new URLSearchParams(queryString);
                location.reload();
            }, 500)
        }

        if (urlParams.has('f')) {
            const filter = urlParams.get('f');
            const obj = atob(filter);
            if (obj !== undefined) {
                try {
                    const ev = eval('(' + obj + ')');
                    let count = 1;
                    Object.keys(ev).forEach((item) => {
                        if (!['s1', 's2', 's3'].includes(item)) {
                            // originalData['s' + count] = ev[item];
                            var list = [item];
                            list = list.concat(ev[item]);
                            originalData['s' + count] = list;
                            // console.log("THIS IS EACH: " + JSON.stringify(originalData['s' + count]));
                            // originalData['s' + count] = [item].append(ev[item])
                            // originalData[item] = ev[item];
                            element_id_to_title['s' + count] = item;
                            count++;
                        }
                    });
                } catch (e) {
                    console.log(e);
                }
            }
        }
        updateFilterOptions(originalData);
        
        console.log("ORIG " + JSON.stringify(originalData)); // This is passed as a key value using the filterable name as key and options as value. Can convert this back s notation with value as first element in array
        tmpResult = $.extend(true, {}, originalData); // need for better handling of the tmpResult to update filtering capabilities
        console.log("TEMP RESULT: " + JSON.stringify(tmpResult));
        Panel = $('.panel');

        Panel.find("#search_rows").empty(); // clear the search rows panel so that we can append the data
        s_options.forEach((value) => { // won't allow with more than 3 options
            Panel.find('#' + value.s).empty();
            var default_option = [];
            Panel.find("#search_rows").append(pack_dropdown(value.display)); // the dropdown to the panel
            value.option.slice(1).forEach((op_val) => { // slice the string to not include the category {s1: ['pod', 'value1', 'value2']}
                Panel.find('#' + value.s).append(pack_option(op_val.v, op_val.text)); // add all of the options to the dropdown just added
                if (originalData[value.display].indexOf(op_val.v) >= 0) {
                    default_option.push(op_val.v);
                }
            });
            $('#' + value.s).selectpicker();
            $('#' + value.s).selectpicker('val', default_option);
        });
        bindEvents();
    };
    panel.init = init;

    function bindEvents() {
        // for the number of values, in s_options, do this thing
        for (let i = 1; i <= s_options.length; i++) {
            var object = s_options[i];
            $('#s' + i).on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => { // sets the listener when dropdowns are changed
                const list = [tmpResult['s' + i][0]]
                tmpResult['s' + i] = list.concat($('#s' + i).selectpicker('val'));
            });
        }
        Panel.find('#search_now').off('click').click(function (e) { // function that is called when the filter button is clicked. 
            dirty = false;
            console.log("ORIGINAL PRE BINDIGN: " + JSON.stringify(originalData));
            originalData = $.extend(true, {}, tmpResult);
            console.log("BINDING: " + JSON.stringify(originalData));
            GridPanel.get_new(originalData);
        });
    }
}(SearchPanel || (SearchPanel = {})));