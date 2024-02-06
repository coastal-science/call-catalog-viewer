var GridPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var resultData = undefined; // this is all of the data read from catalogs initially
    var data_index = 0;
    var currentDisplayData = undefined; // this is the data that has the filters applied to it and we want to use
    window.entireFilterData = undefined;
    var searching_para = undefined;
    var all_fields = [];
    var sortable_fields = [];
    var metadata_show = undefined;
    var sort_by = undefined;
    var sort_asc = undefined;
    var id_to_seq = undefined;
    var next_drawn = undefined;

    var current_page = undefined;
    var page_size = 24;
    var total_result = undefined;
    var total_page = undefined;
    var data_initialized = false;

    var encoded = undefined;

    var poped = undefined;
    var pop_opening = undefined;
    var lity_data = undefined;
    var audio_element = undefined;
    var selecting = undefined;
    const LIBRARY = 'catalogs';
    const LIBRARY_INDEX = 'index.yaml';
    var catalog_library = {};
    const media_folder_path = ''; /* srkw-call-catalogue-files/media removed to get files locally */
    const play_icon = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-play" width="32" height="32" viewBox="0 0 24 24"><path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-3 17v-10l9 5.146-9 4.854z"/></svg>';
    /*
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
            <path fill="currentColor" d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
        </svg>

        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="40" viewBox="0 0 490 245" x="0px" y="0px" style="enable-background:new 0 0 490 490;" xml:space="preserve">\
                        <g>\
                        <path d="M460.123,0H29.877C13.406,0,0,13.406,0,29.877v131.771c0,16.479,13.406,29.885,29.877,29.885h430.245 c16.471,0,29.877-13.406,29.877-29.885V29.877C490,13.406,476.594,0,460.123,0z M474.688,161.649 c0,8.037-6.535,14.572-14.565,14.572H29.877c-8.03,0-14.565-6.535-14.565-14.572V29.877c0-8.03,6.535-14.565,14.565-14.565h430.245 c8.03,0,14.565,6.535,14.565,14.565V161.649z"/>\
                        <path d="M113.333,47.59c-13.466,0-23.014,0.867-29.817,2.026v96.256h21.855v-34.887c2.026,0.292,4.628,0.434,7.529,0.434\
                            c13.025,0,24.172-3.178,31.694-10.273c5.795-5.503,8.98-13.608,8.98-23.163c0-9.548-4.202-17.653-10.423-22.58\
                            C136.639,50.192,126.941,47.59,113.333,47.59z M112.75,94.484c-3.185,0-5.495-0.142-7.38-0.576V65.101\
                            c1.593-0.434,4.628-0.867,9.122-0.867c10.998,0,17.219,5.361,17.219,14.333C131.711,88.555,124.474,94.484,112.75,94.484z"/>\
                            <polygon points="189.754,48.315 167.608,48.315 167.608,145.872 228.544,145.872 228.544,127.345 189.754,127.345 	"/>\
                            <path d="M265.158,48.315l-29.818,97.557h22.871l6.946-25.04h27.941l7.522,25.04h23.739l-30.251-97.557H265.158z M268.343,104.331 l5.787-20.703c1.593-5.645,3.043-13.025,4.494-18.812h0.284c1.451,5.787,3.185,13.025,4.92,18.812l6.086,20.703H268.343z"/>\
                            <path d="M365.75,71.762c-2.893,6.946-5.211,12.591-7.38,18.67h-0.292c-2.46-6.363-4.486-11.574-7.522-18.67l-9.989-23.447h-25.189 l30.834,57.609v39.949h21.997v-40.674l32.135-56.884h-24.748L365.75,71.762z"/>\
                        </g>\
                    </svg>
    */

    String.prototype.toTitleCase = function () {
        return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase();});
    };
                    
    function num_of_item_per_row() {
        if (window.matchMedia('(min-width: 1400px)').matches) {
            return 6;
        }
        if (window.matchMedia('(min-width: 1200px)').matches) {
            return 6;
        }
        if (window.matchMedia('(min-width: 992px)').matches) {
            return 4;
        }
        if (window.matchMedia('(min-width: 768px)').matches) {
            return 4;
        }
        if (window.matchMedia('(min-width: 576px)').matches) {
            return 3;
        }
        return 1;
    }

    function pack_option(id, image_file, callname, d1_category, d1_value, d2_category, d2_value, full) {
        var d1 = (d1_category == undefined || d1_category == null) ? "" : d1_category.charAt(0).toUpperCase() + d1_category.slice(1) + ': ' + d1_value;
        var d2 = (d2_category == undefined || d2_category == null) ? "" : d2_category.charAt(0).toUpperCase() + d2_category.slice(1) + ': ' + d2_value;

        return '<div class="col-xxl-2 col-xl-2 col-lg-3 col-md-3 col-sm-4 mb-4 itemblock" id="gi-' + id + '">\
        <div class="bg-white rounded shadow-sm"><a href="'+ media_folder_path + full + '" data-toggle="lightbox" class="image_pop_source text-decoration-none"">\
                <img src="'+ media_folder_path + image_file + '" loading="lazy" alt="" class="img-fluid card-img-top"></a>\
                    <div class="p-4">\
                        <h5> <a class="play_btn" href="#" style="text-decoration:none">'+ play_icon + '<span class="text-dark">&nbsp;' + callname + '</span></a></h5>\
                        <p class="small mb-0 meta-p"><span class="font-weight-bold">' + d1 + '</span></p>\
                        <div class="meta-p d-flex align-items-center justify-content-between rounded-pill bg-light px-3 py-2 mt-4">\
                        <div class="badge badge-warning px-3 rounded-pill font-weight-normal"><span class="font-weight-bold  text-dark">' + d2 + '</span></div>\
                    </div>\
                </div>\
            </div>\
        </div>';
    }

    async function getData(catalog_json) {
        // let catalog_json = "catalogs/srkw-call-catalogue-files.json";
        // let response = getCatalog(catalog_json)

        // 1. read yaml https://stackoverflow.com/a/70919596
        // non-blocking version:
        // fetch(LIBRARY + "/" + LIBRARY_INDEX)
        //   .then(response => response.text())
        //   .then(text => {
        //     // once the file has been loaded, we can parse it into an object.
        //     yaml = jsyaml.load(text);
        //     console.log(yaml);
        //   });
        // await response of fetch call
        let response = await fetch(LIBRARY + "/" + LIBRARY_INDEX);

        // only proceed once promise is resolved
        let text = await response.text();
        var yaml = jsyaml.load(text);

        console.log("Catalogs library contains:", yaml[LIBRARY]);

        // if index.yaml does not exist (empty viewer) then it stops some other errors
        if (yaml[LIBRARY] === undefined)
            return;

        yaml = yaml[LIBRARY].reverse(); // reverse() ensures that the catalog added first is the most recent loaded

        // 2. for each catalog in yaml (in reverse order): getCatalog(catalog)
        for (const name of yaml) {
            // Using a for() generator allows to use await inside the loop.
            // In case of yaml.forEach(name =>) with callback function, the callback
            //  would have to be async and could introduce race conditions (unexpected behaviour).
            let response = await getCatalog(LIBRARY + "/" + name + '.json');
        }
        if (!data_initialized)
            setSortableDropdownValues();
        data_initialized = true;
    }
    panel.getData = getData;

    function setSortableDropdownValues() {
        const $dropdown = $('#sort');
        $dropdown.empty();
        sortable_fields.forEach(field => {
            $dropdown.append($('<option>', {
                value: field,
                text: field.charAt(0).toUpperCase() + field.slice(1)
            }))
        });

        $dropdown.selectpicker('refresh');
    }

    /**
     * This is applies the current filters defined in searching_para to our entire dataset in resultData
     * This filtered data is then assigned to entireFilterData for later access
     */
    async function updateCurrentData() {
        window.entireFilterData = resultData; // this resets so that we are checking all of the values
        var params = Object.keys(searching_para);
        params.forEach(p => {
            if (!(["s1", "s2", "s3"].includes(p))) {
                window.entireFilterData = window.entireFilterData.filter(item => { // item is all of the calls in the catalogs
                    if (searching_para[p].length == 0) // if it is empty then it is just true for all
                        return true;

                    if (!(p in item)) // filtering on a different catalog data
                        return true;
                    if (Array.isArray(item[p])) {
                        for (var i = 0; i < item[p].length; i++) {
                            if (searching_para[p].includes(item[p][i])) {
                                return true;
                            }
                        }
                        return false;
                    } else {
                        return searching_para[p].includes(item[p]);
                    }
                })
            }
        });
    }

    /**
     * Ensure that all of the necessary fields are present and set to default values if they do not have values
     * @param {Object} data data for the lity object that needs to get verified
     */
    function validateParameters(data) {
        var keys = Object.keys(data);
        keys.forEach(p => {
            if (data[p] == undefined || data[p] == null) {
                delete data[p];
            }
        })
        return data;
    }

    /**
     * Initialize data on the first call from getData
     * Obtain correct data to display and assign to currentDisplayData and perform correct pagination and URL parameterizing
     * @param {Object} catalog_json path to JSON file
     * @returns 
     */
    async function getCatalog(catalog_json) {
        if (!data_initialized) { // if this is our first time setting params, use filters from JSON

            // await response of fetch call
            let response = await fetch(catalog_json);
            // only proceed once promise is resolved
            let data = await response.text();
            // only proceed once second promise is resolved

            var simple_datasource = JSON.parse(data.replace(/\bNaN\b/g, "null")); // json representation the catalogue.json file

            // get the filter data and set simple_datasource so it is just calls
            var site_details = simple_datasource["site-details"];
            if (site_details['catalogue']['is_root'] === 'true') {
                document.getElementById("catalogue-title").innerHTML = site_details['catalogue']['title'];
            }
            // TODO: temporary hack for the release 1.0 of a single local root catalogue.
            // The hack is not needed when all catalogues are remote catalogues.
            // By design (reasoning?): local catalogues cannot be root catalogues.
            document.getElementById("catalogue-title").innerHTML = site_details['catalogue']['title'];

            var filters = simple_datasource["filters"];
            var population = simple_datasource["population"];
            var searchable = simple_datasource["sortable"];
            var display_data = simple_datasource["display"];
            simple_datasource = simple_datasource["calls"];

            searchable.slice(1).forEach(field => {
                if (!sortable_fields.includes(field))
                    sortable_fields.push(field);
            })
            updateFiltersFromJSON(population, filters);

            var keys = Object.keys(simple_datasource);
            keys.forEach(item => { // this will append all of the items to the resultdata
                // get the old name
                old_d1 = display_data[0]['d1']
                old_d2 = display_data[1]['d2']

                // get the new keys that we want to use
                new_d1 = old_d1.replace(/-/g, '_');
                new_d2 = old_d2.replace(/-/g, '_');

                // create the new display name property in call object and update the display reference
                simple_datasource[item][new_d1] = simple_datasource[item][old_d1];
                simple_datasource[item][new_d2] = simple_datasource[item][old_d2];
                simple_datasource[item]['d1'] = new_d1;
                simple_datasource[item]['d2'] = new_d2;

                // remove the old key that contained '-'s
                delete simple_datasource.old_d1
                delete simple_datasource.old_d2

                resultData[data_index] = validateParameters(simple_datasource[item]);
                data_index++;
            });
            await updateCurrentData(); // apply filters on resultData, populating currentFilteredData accordingly
        }

        filter_result = window.entireFilterData.length; // update the length based off of the filtered data

        $("#total").text(filter_result);
        total_page = Math.floor((filter_result - 1) / page_size) + 1;
        if (total_page <= 0) {
            total_page = 1;
        }
        if (current_page > total_page) {
            current_page = total_page;
        }
        if (current_page < 1) {
            current_page = 1;
        }

        $('#paging > ul > li').removeClass('hidden active disabled');
        if (total_page >= 3) {
            if (current_page === 1) {
                $('#paging > ul > li:nth-child(1)').addClass('disabled');
                $('#paging > ul > li:nth-child(2)').addClass('active').attr('data-flow', '1');
                $('#paging > ul > li:nth-child(2) a').text('1');
                $('#paging > ul > li:nth-child(3) a').text('2');
                $('#paging > ul > li:nth-child(3)').attr('data-flow', '2');
                $('#paging > ul > li:nth-child(4) a').text('3');
                $('#paging > ul > li:nth-child(4)').attr('data-flow', '3');

            }
            else if (current_page >= total_page) {
                //at foremost
                $('#paging > ul > li:nth-child(2) a').text(total_page - 2);
                $('#paging > ul > li:nth-child(2)').attr('data-flow', total_page - 2);
                $('#paging > ul > li:nth-child(3) a').text(total_page - 1);
                $('#paging > ul > li:nth-child(3)').attr('data-flow', total_page - 1);
                $('#paging > ul > li:nth-child(4) a').text(total_page);
                $('#paging > ul > li:nth-child(4)').addClass('active').attr('data-flow', total_page);
                $('#paging > ul > li:nth-child(5)').addClass('disabled');
            }
            else {
                //middle
                $('#paging > ul > li:nth-child(2) a').text(current_page - 1);
                $('#paging > ul > li:nth-child(2)').attr('data-flow', current_page - 1);
                $('#paging > ul > li:nth-child(3) a').text(current_page);
                $('#paging > ul > li:nth-child(3)').addClass('active').attr('data-flow', current_page);
                $('#paging > ul > li:nth-child(4) a').text(current_page + 1);
                $('#paging > ul > li:nth-child(4)').attr('data-flow', current_page + 1);

            }
        }
        else if (total_page === 2) {
            $('#paging > ul > li:nth-child(2)').attr('data-flow', '1');
            $('#paging > ul > li:nth-child(3)').attr('data-flow', '2');
            $('#paging > ul > li:nth-child(2) a').text('1');
            $('#paging > ul > li:nth-child(3) a').text('2');
            $('#paging > ul > li:nth-child(4)').addClass('hidden');
            if (current_page === 1) {
                $('#paging > ul > li:nth-child(1)').addClass('disabled');
                $('#paging > ul > li:nth-child(2)').addClass('active');
            }
            else {
                $('#paging > ul > li:nth-child(3)').addClass('active');
                $('#paging > ul > li:nth-child(5)').addClass('disabled');
            }
        }
        else if (total_page === 1) {
            $('#paging > ul > li:nth-child(1)').addClass('disabled');
            $('#paging > ul > li:nth-child(2)').addClass('active').attr('data-flow', '1');
            $('#paging > ul > li:nth-child(2) a').text('1');
            $('#paging > ul > li:nth-child(3)').addClass('hidden');
            $('#paging > ul > li:nth-child(4)').addClass('hidden');
            $('#paging > ul > li:nth-child(5)').addClass('disabled');
        }

        current_sort = (a, b) => {
            if (Array.isArray(a)) {
                a = a.join(', ');
            }
            if (Array.isArray(b)) {
                b = b.join(', ');
            }
            if (a[sort_by] === b[sort_by]) {
                return 0;
            }
            var smaller = (sort_asc === "as") ? a[sort_by] : b[sort_by];
            var larger = (sort_asc === "as") ? b[sort_by] : a[sort_by];

            // moves fields not filter on to the back of list
            if (larger == undefined)
                return -1;

            if (smaller == undefined)
                return 1;

            if (larger > smaller) {
                return -1;
            }
            else {
                return 1;
            }
        };
        window.entireFilterData.sort(current_sort);

        currentDisplayData = window.entireFilterData.slice((current_page - 1) * page_size, (current_page) * page_size); // obtain the data to display on this page from the entireData slice
        redraw_items(); // draws our new updated items

        if (!data_initialized)
            encoded = btoa(JSON.stringify(searching_para));
        const state = { 'f': encoded, 'p': current_page, 's': sort_by, 'sa': sort_asc };
        const title = '';
        const queryString = window.location.search;
        const params = new URLSearchParams('');
        params.set('f', encoded);
        params.set('p', current_page);
        params.set('s', sort_by);
        params.set('sa', sort_asc);
        params.set('ps', page_size.toString());
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('popup')) {
            params.set('popup', urlParams.get('popup'));
            $('.selecting').removeClass('selecting');
        }

        catalog_library[catalog_json] = resultData;
        console.log("added to library", catalog_library);

        history.pushState(state, title, `${window.location.pathname}?${params}`);
        return;
    }
    panel.getCatalog = getCatalog;

    /**
     * Update the current filters to include the new ones from given catalogue
     * @param {JSON} filters JSON representation of filters for given catalogue
     */
    function updateFiltersFromJSON(population, filters) {
        filters.forEach(element => {
            var filterable = element[0];
            // population will be a global filterable, other ones will be nested inside of the population
            if (filterable === 'population') {
                if (!(filterable in searching_para)) { // filterable is not already in the searchable
                    searching_para[filterable] = element.slice(1); // add the filterable param to the searching_params
                } else { // filterable is already in the parameters. Add all the elements that are not already in it
                    element.slice(1).forEach(val => {
                        if (val && !searching_para[filterable].includes(val)) { // not an empty string and doesn't already exist.
                            searching_para[filterable].push(val);
                        }
                    });
                }
            } else {
                if (!(population in searching_para)) {
                    searching_para[population] = {}
                }

                if (!(filterable in searching_para[population])) { // filterable is not already in the searchable
                    searching_para[population][filterable] = element.slice(1); // add the filterable param to the searching_params //Unknown deprecated with empty string.
                } else { // filterable is already in the parameters. Add all the elements that are not already in it
                    element.slice(1).forEach(val => {
                        if (!searching_para[population][filterable].includes(val)) {
                            searching_para[population][filterable].push(val);
                        }
                    });
                }
            }
            // // ensure that the 'Unknown' field is at the bottom of the dropdown
            // var index = searching_para[filterable].indexOf("Unknown");
            // if (index != -1) {
                //     searching_para[filterable].splice(index, 1);
                //     searching_para[filterable].push('Unknown');
                // }
            });
    }


    function init() {
        resultData = [];
        lity_data = [];
        id_to_seq = {};
        next_drawn = 0;
        selecting = 0;
        pop_opening = false;
        metadata_show = true;

        // TODO: How can this be altered to allow for searching parameters to be picked from the yaml?
        // Does this even matter?? Update params is called on teh loading anyway
        // these are passed through the url to the searching params. Can update these first and then send them to the fellas over there
        searching_para = {
            // s1: ["SRKW", "NRKW"],
            // s2: ["J"],
            // s3: ["J", "K", "L"],
        };
        sort_by = 'call_type';
        sort_asc = 'as';

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('f')) {
            const filter = urlParams.get('f');
            const obj = atob(filter);
            if (obj !== undefined) {
                try {
                    const ev = eval('(' + obj + ')');
                    ['s1', 's2', 's3'].forEach((v) => {
                        if (ev[v] !== undefined) {
                            searching_para[v] = ev[v];
                        }
                    });
                } catch (e) {

                }
            }
        }
        current_page = 1;
        if (urlParams.has('p')) {
            const filter = urlParams.get('p');
            current_page = parseInt(filter);
        }
        if (urlParams.has('s') && urlParams.has('sa')) {
            const filter = urlParams.get('s');
            sort_by = filter;
            const as = urlParams.get('sa');
            sort_asc = as;
        }
        if (urlParams.has('ps')) {
            const filter = urlParams.get('ps');
            const tmp_ps = parseInt(filter);
            if (tmp_ps > 0 && tmp_ps % 12 === 0) {
                page_size = tmp_ps;
            }
        }

        poped = false;
        Panel = $('#resultgrid');

        total_result = 1;
        total_page = 1;

        $('#sort').selectpicker('val', sort_by);
        $('#sort_a').selectpicker('val', sort_asc);
        $('#page_size').selectpicker('val', "" + page_size);
        $('#show_meta').prop('checked', metadata_show);
        bindEvents();
        if (urlParams.has('popup')) {
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            if (urlParams.has('popup')) {
                const filter = urlParams.get('popup');
                try {
                    const obj = atob(filter);
                    if (obj !== undefined) {
                        const data = eval('(' + obj + ')');
                        if (data['filename'] == undefined) {
                            throw new Exception('Parse Error');
                        }
                        //show details
                        var instance = lity('./' + data.image_file);
                        var template = instance.options('template');
                    }
                } catch (e) {
                    document.location.href = page_link;
                }
            }
        }
        getData();
    };
    panel.init = init;

    /**
     * Updates searching_params based on the filters passed through URL
     * Called on filter button clicked
     * @param {Object} params new paramaters to filter on
     */
    function updateFiltersFromURLParams(params) {
        Object.keys(params).forEach((key) => {
            const arr = params[key];
            var filterable = key;

            if (!(filterable in searching_para))
                searching_para[filterable] = arr;
            else {
                arr.slice(1).forEach(val => {
                    if (!searching_para[filterable].includes(val)) {
                        searching_para[filterable].push(val);
                    }
                });
            }
        });
    }

    /**
     * receive new filters, update searching_para, apply filters to update currentDisplayData, call getData to refresh page
     * @param {Object} para search filters selected in search panel
     */
    function get_new(para) {
        searching_para = {}; // reset searching params as we are going to entirely rebuild them
        updateFiltersFromURLParams(para); // updates searching_para with the filters passed through url
        updateCurrentData(); // applies the now updated filters on the resultData, giving us the currentDisplayData that should be displayed
        total_result = undefined;
        current_page = 1;
        getData();
    };
    panel.get_new = get_new;

    function propagate_meta() {
        if (metadata_show) {
            $('#gi-area .meta-p').removeClass('hidden');
        }
        else {
            $('#gi-area .meta-p').addClass('hidden');
        }
    }

    /**
     * Turn data fields into the HTML and append them to the gridView
     */
    function append_items() {
        var i = next_drawn;
        var grid = $('#gi-area').empty();
        for (; i < currentDisplayData.length; i++) {
            var ele = currentDisplayData[i];
            do {
                var tmpid = window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16) + window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
            } while (id_to_seq[tmpid] !== undefined);
            id_to_seq[tmpid] = i;
            var obj = pack_option(tmpid, LIBRARY + '/' + ele.image_file, ele.call_type, ele['d1'], ele[ele.d1], ele.d2, ele[ele.d2], LIBRARY + '/' + ele.image_file);
            grid.append(obj);
        }
        selecting = 0;
        propagate_meta();
        $('#gi-area .itemblock:nth(0)').click();

        if (i !== 0) {
            next_drawn = i;
        }
    };
    function redraw_items() {
        id_to_seq = {};
        next_drawn = 0;
        poped = false;
        append_items();
    };
    panel.redraw_items = redraw_items;
    function bindEvents() {
        $('#gi-area').off('click').on('click', '.itemblock .image_pop_source', function (e) {
            e.stopPropagation();
            e.preventDefault();
            let parent_itemblock = $(this).parents('.itemblock');
            $(parent_itemblock).click();
            var obj_id = $(this).parents('.itemblock').attr('id').substring(3);
            poped = obj_id;
            //var data_target_seq = id_to_seq[poped];
            //var data_target = resultData[data_target_seq];

            var instance = lity($(this).attr('href'));
            var template = instance.options('template');
        });
        $('#gi-area').on('click', '.play_btn', function (e) {
            e.stopPropagation();
            e.preventDefault();
            var obj_id = $(this).parents('.itemblock').attr('id').substring(3);
            var data_target_seq = id_to_seq[obj_id];
            var data_target = currentDisplayData[data_target_seq];
            if (audio_element !== undefined && audio_element !== null && audio_element.pause !== undefined) {
                audio_element.pause();
            }
            audio_element = document.createElement('audio');
            audio_element.setAttribute('src', '');
            audio_element.setAttribute('src', LIBRARY + '/' + data_target.audio_file);
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
            // console.log(obj_id)
            // console.log(audio_element)
        });
        $('#gi-area').on('click', '.itemblock', function (e) {
            $(this).siblings('.itemblock').removeClass('selecting');
            $(this).addClass('selecting');
            selecting = $(this).index();
        });
        var delayed_pop = undefined;
        var keyboard_threshold = 200;
        var keyboard_block = undefined;
        window.addEventListener('keydown', (e) => {
            let diff = 0;
            let prevent_d = true;
            if (keyboard_block === undefined) {
                keyboard_block = setTimeout(() => {
                    keyboard_block = undefined;
                }, keyboard_threshold);
            }
            else {
                return;
            }
            switch (e.key) {
                case 'ArrowUp':
                    diff = -num_of_item_per_row();
                    break;
                case 'ArrowDown':
                    diff = num_of_item_per_row();
                    break;
                case 'ArrowLeft':
                    diff = -1;
                    break;
                case 'ArrowRight':
                    diff = 1;
                    break;
                case ' ':
                    if (pop_opening) {
                        $('#play').click();
                    }
                    else {
                        $('.selecting .play_btn').click();
                    }
                    break;
                case 'Enter':
                    if (!pop_opening) {
                        $('.selecting.itemblock .image_pop_source').click();
                    }
                    break;
                default:
                    prevent_d = false;
                    break;
            }
            if (prevent_d) {
                e.preventDefault();
            }
            if (diff !== 0 && $('.selecting').length > 0) {
                if (selecting + diff >= 0 && selecting + diff < resultData.length) {
                    selecting += diff;
                    let target = $('#gi-area .itemblock:nth(' + selecting + ')');
                    if (target.length >= 0) {
                        $(target).siblings().removeClass('selecting');
                        $(target).addClass('selecting');
                        if (target[0]) { 
                            // handle exception when navigating with arrow keys past the items on the page pagination, 
                            // the additional items are on the next page
                            target[0].scrollIntoView({ block: "end" });
                        }
                        if (poped) {
                            if (delayed_pop !== undefined) {
                                clearTimeout(delayed_pop);
                            }
                            $('.lity-close').click();
                            delayed_pop = setTimeout(() => {
                                $('.selecting.itemblock .image_pop_source').click();
                                if ($('.selecting')[0] !== undefined) {
                                    $('.selecting')[0].scrollIntoView({ block: "end" });
                                }
                                delayed_pop = undefined;
                            }, 100);
                        }
                    }
                    else {
                        selecting -= diff;
                    }
                }
            }
            else if (diff !== 0) {
                //toast
                $('.toast').addClass('show');
                setTimeout(() => {
                    $('.toast').removeClass('show');
                }, 800);
            }
        });
        $('#paging > ul > li').click(function (e) {
            e.stopPropagation();
            e.preventDefault();
            if ($(this).hasClass('disabled') || $(this).hasClass('hidden') || $(this).hasClass('active')) {
                return;
            }
            var data_flow = $(this).attr('data-flow');
            if (data_flow === 'n') {
                current_page += 1;
            }
            else if (data_flow === 'p') {
                current_page -= 1;
            }
            else {
                current_page = parseInt(data_flow);
                if (isNaN(current_page)) {
                    current_page = 1;
                }
            }
            $('#resultgrid > div.container > div.row.justify-content-md-center > div.col.col-12.col-sm-12.col-md-12.col-lg-8.col-xl-6.col-xxl-6.row.align-items-center.align-middle > span').focus();
            scrollBackToResults()
            getData();
        });

        $(document).on('lity:open', function (event, instance) {
            lity_data = [];
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            if (poped != undefined && !urlParams.has('popup')) {
                var data_target_seq = id_to_seq[poped];
                var data_target = currentDisplayData[data_target_seq];
                validateParameters(data_target);
                lity_data = data_target;
                var encoded_data = btoa(JSON.stringify(data_target));
                var encoded = btoa(JSON.stringify(searching_para));
                const state = { 'f': encoded, 'p': current_page, 's': sort_by, 'sa': sort_asc, 'popup': encoded_data };
                const title = 'Details: ' + lity_data.cn + ' (Call Name)';//For Safari only
                const params = new URLSearchParams('');
                params.set('f', encoded);
                params.set('p', current_page);
                params.set('s', sort_by);
                params.set('sa', sort_asc);
                params.set('ps', page_size.toString());
                params.set('popup', encoded_data);

                history.pushState(state, title, `${window.location.pathname}?${params}`);
            }
            else if (urlParams.has('popup')) {
                //may be generated from link
                const filter = urlParams.get('popup');
                const obj = atob(filter);
                if (obj !== undefined) {
                    try {
                        lity_data = eval('(' + obj + ')');
                        $('.selecting').removeClass('selecting');
                    } catch (e) {
                        document.location.href = page_link;
                    }
                }
                else {
                    document.location.href = page_link;
                }
                // console.log(lity_data);
            }
            else {
                //something went wrong
                document.location.href = page_link;
            }
            let play_btn = '<button id="play" class="col btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
                            </svg>Play (Call Name: '+ lity_data.call_type + ') </button>';
            let additional_row = '';


            var temp = Object.keys(lity_data);
            const fields = temp.filter(item => {
                return (!['image_file', 'audio_file', 'description_file', 'call_type', 'filename', 'd1', 'd2'].includes(item));
            })
            var count = fields.length;
            var is_odd = count % 2;

            for (let i = 0; i <= Math.floor(count / 2); i += 2) {
                var first = fields[i];
                var second = fields[i + 1];

                additional_row += '<div class="row text-sm-center text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>' + first.toTitleCase() + ': ' + lity_data[first] + '</span></div>';
                additional_row += '<div class="col-12 col-sm-6"><span>' + second.toTitleCase() + ': ' + lity_data[second] + '</span></div></div>';
            }

            if (is_odd) {
                additional_row += '<div class="row text-sm-center text-start text-info border-2 border-light border-bottom">';
                var field = fields[count - 1];
                additional_row += '<div class="col"><span>' + field + ': ' + lity_data[field] + '</span></div>';
            }
            // all_fields.forEach(field => {
            //     if (lity_data[field] !== undefined && lity_data[field] !== null && lity_data[field].length !== 0) {
            //         additional_row += '<div class="row text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>' + field.charAt(0).toUpperCase() + field.slice(1) + ': ' + lity_data[field] + '</span></div>';
            //     }
            // })
            //lity_data["subclan"] = "Testing Clan";
            //lity_data["subpopulation"] = "Testing Population";
            // if (lity_data["subpopulation"] !== undefined &&
            //     lity_data["subpopulation"] !== null &&
            //     lity_data["subpopulation"].length > 0) {
            //     let population = { 'SRKW': "Southern Resident", 'NRKW': "Northern Resident" }[lity_data['population']];

            //     additional_row += '<div class="row text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>Population: ' + population + '</span></div>';
            //     additional_row += '<div class="col-12 col-sm-6"><span>Sub-Population: ' + lity_data['subpopulation'] + '</span></div></div>';
            // }
            // if (lity_data["subclan"] !== undefined &&
            //     lity_data["subclan"] !== null &&
            //     lity_data["subclan"].length > 0) {
            //     additional_row += '<div class="row text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>Clan: ' + lity_data['clan'] + '</span></div>';
            //     additional_row += '<div class="col-12 col-sm-6"><span>Sub-Clan: ' + lity_data['subclan'] + '</span></div></div>';
            // }
            // let items_count = ((lity_data["sample"] !== undefined &&
            //     lity_data["sample"] !== null &&
            //     lity_data["sample"].length > 0) ? 1 : 0) +
            //     ((lity_data["mar"] !== undefined &&
            //         lity_data["mar"] !== null &&
            //         lity_data["mar"].length > 0) ? 1 : 0);
            // let alignment = "text-sm-center";
            // if (items_count > 1) {
            //     alignment = "";
            // }
            // if (items_count) {
            //     additional_row += '<div class="row ' + alignment + ' text-start text-info border-2 border-light border-bottom">';
            // }

            // if (lity_data["sample"] !== undefined &&
            //     lity_data["sample"] !== null &&
            //     lity_data["sample"].length > 0) {
            //     additional_row += '<div class="col"><span>Sample: ' + lity_data['sample'] + '</span></div>';
            // }
            // if (lity_data["mar"] !== undefined &&
            //     lity_data["mar"] !== null &&
            //     lity_data["mar"].length > 0) {
            //     additional_row += '<div class="col"><span>Matrilines: ' + lity_data['mar'] + '</span></div>';
            // }
            // if (items_count) {
            //     additional_row += '</div';
            // }
            $('.lity-container').append('<div class="container-fluid litybottom"><div class="row">' + play_btn + '</div>' + additional_row + '</div>');

            // file = 'resources_config/sample.md'
            file = LIBRARY + '/' + media_folder_path + lity_data['description_file']
            css_file = 'css/darkdown.css'
            $('.lity-container').append(
                `<div class="container-fluid litybottom"> 
                    <zero-md src='${file}'> 
                        <template> 
                            <link href='${css_file}' rel="stylesheet"> </link>  
                        </template> 
                    </zero-md>
                </div>`);

            pop_opening = true;

            // console.log(lity_data)
        });
        $(document).on('click', '.lity-container #play', function () {
            audio_element = document.createElement('audio');
            $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
            <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
          </svg>Playing  (Call Name: '+ lity_data.call_type + ')');
            $(this).removeClass('btn-primary').addClass('btn-success');
            audio_element.setAttribute('src', '');
            audio_element.setAttribute('src', LIBRARY + '/' + lity_data.audio_file);
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
            audio_element.addEventListener('ended', function () {
                $("#play").html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
              </svg>Play  (Call Name: '+ lity_data.call_type + ')').addClass('btn-primary').removeClass('btn-success');

            })
            // console.log(lity_data)
        });
        $(document).on('lity:close', function (event, instance) {
            if (audio_element !== undefined && audio_element.setAttribute !== undefined) {
                //pause unfinished playing when close
                audio_element.setAttribute('src', '');
                audio_element.pause();
            }
            poped = undefined;
            pop_opening = false;
            var encoded = btoa(JSON.stringify(searching_para));
            const state = { 'f': encoded, 'p': current_page, 's': sort_by, 'sa': sort_asc };
            const title = '';
            const params = new URLSearchParams('');
            params.set('f', encoded);
            params.set('p', current_page);
            params.set('s', sort_by);
            params.set('sa', sort_asc);
            params.set('ps', page_size.toString());
            history.pushState(state, title, `${window.location.pathname}?${params}`);
            if ($('.selecting').length <= 0) {
                $('#gi-area .itemblock:nth(0)').addClass('selecting');
            }
        });
        $('#show_meta').change(function () {
            if ($(this).prop('checked')) {
                metadata_show = true;
            }
            else {
                metadata_show = false;
            }
            propagate_meta();
        });
        $('#sort').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            sort_by = $('#sort').selectpicker('val');
            sort_by = sort_by.replace(/-/g, "_");
            getData();
        });
        $('#sort_a').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            sort_asc = $('#sort_a').selectpicker('val');
            getData();
        });
        $('#page_size').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            page_size = parseInt($('#page_size').selectpicker('val'));
            getData();
        });
    }
}(GridPanel || (GridPanel = {})));
