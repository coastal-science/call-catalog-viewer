var GridPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var resultData = undefined;
    var searching_para = undefined;
    var metadata_show = undefined;
    var sort_by = undefined;
    var sort_asc = undefined;
    var id_to_seq = undefined;
    var next_drawn = undefined;

    var current_page = undefined;
    var page_size = 120;
    var total_result = undefined;
    var total_page = undefined;

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
    function num_of_item_per_row(){
        if (window.matchMedia('(min-width: 1400px)').matches){
            return 6;
        }
        if (window.matchMedia('(min-width: 1200px)').matches){
            return 6;
        }
        if (window.matchMedia('(min-width: 992px)').matches){
            return 4;
        }
        if (window.matchMedia('(min-width: 768px)').matches){
            return 4;
        }
        if (window.matchMedia('(min-width: 576px)').matches){
            return 3;
        }
        return 1;
    }

    function pack_option(id, image_file, callname, pod, clan, full){
        if (Array.isArray(pod)){
            if (pod.length >= 1){
                pod = '['+pod.join(', ')+']';
            }
            else if (pod.length === 1){
                pod = pod[0];
            }
            else{
                pod = 'N/A';
            }
        }

        // checking if values exist in the data. If they do, they will be put there, else they will be unkown or N/A
        if (callname === undefined || callname === null){
            callname = "Not Specified";
        }
        if (pod === undefined) {
            pod = "N/A";
        }
        if (clan === undefined) {
            clan = "N/A";
        }

        
        return '<div class="col-xxl-2 col-xl-2 col-lg-3 col-md-3 col-sm-4 mb-4 itemblock" id="gi-'+id+'">\
            <div class="bg-white rounded shadow-sm"><a href="'+media_folder_path+full+'" data-toggle="lightbox" class="image_pop_source text-decoration-none"">\
            <img src="'+media_folder_path+image_file+'" loading="lazy" alt="" class="img-fluid card-img-top"></a>\
            <div class="p-4">\
                <h5> <a class="play_btn" href="#" style="text-decoration:none">'+play_icon+'<span class="text-dark">&nbsp;'+callname+'</span></a></h5>\
                <p class="small mb-0 meta-p"><span class="font-weight-bold">Pods: '+pod+'</span></p>\
                <div class="meta-p d-flex align-items-center justify-content-between rounded-pill bg-light px-3 py-2 mt-4">\
                <div class="badge badge-warning px-3 rounded-pill font-weight-normal"><span class="font-weight-bold  text-dark">Clan: '+clan+'</span></div>\
                </div>\
            </div>\
            </div>\
        </div>';
    }
    async function getData(catalog_json){
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

        yaml = yaml[LIBRARY].reverse(); // reverse() ensures that the catalog added first is the most recent loaded
        
        // 2. for each catalog in yaml (in reverse order): getCatalog(catalog)
        for (const name of yaml) {
            // Using a for() generator allows to use await inside the loop.
            // In case of yaml.forEach(name =>) with callback function, the callback
            //  would have to be async and could introduce race conditions (unexpected behaviour).
            let response = await getCatalog(LIBRARY + "/" + name + '.json');
        }
    }
    panel.getData = getData;

    async function getCatalog(catalog_json){
        // await response of fetch call
		let response = await fetch(catalog_json);
		// only proceed once promise is resolved
		let data = await response.text();
		// only proceed once second promise is resolved
		
        // need to have the searchable parameters within the json file
        // can add each of the searchable parameters to include what is required
        // add a JSON object right to the start so that simple_datasource[0] contains an object with filters, 
        var simple_datasource = JSON.parse(data); // json representation the catalogue.json file
        
        // get the filter data and set simple_datasource so it is just calls
        var filters = simple_datasource["filters"]; 
        simple_datasource = simple_datasource["calls"];
        // console.log("Starting length: " + simple_datasource.length);
        updateFilters(filters);

        var s1 = searching_para['s1'];
        var s2 = searching_para['s2'];
        var s3 = searching_para['s3'];

        // loop through searching_para using the keys from it as the values to get from json
        var parameters = Object.keys(searching_para); // for each of the parameters to search by, find the intersection of them
        // console.log(parameters);
        parameters.forEach(param => {
            if (!(["s1", "s2", "s3"].includes(param))) {
                simple_datasource = simple_datasource.filter(item => {
                    if (Array.isArray(item[param])) {
                        for (var i = 0; i < item[param].length; i++) {
                            if (searching_para[param].includes(item[param][i])) {
                                return true;
                            }
                        }
                        return false;
                    } else {
                        return searching_para[param].includes(item[param]);
                    }
                })
            }
        });
        resultData = simple_datasource;


        // // //Filter: searching_para
        // var resultData1 = simple_datasource.filter(item => s2.includes(item.clan)).filter(item => s1.includes(item.population));
        // resultData = resultData1.filter((item) => {
        //     return item.pod_cat.filter(value => s3.includes(value)).length; // set intersection
        //     // Entire set intersection is computed =  O(m x p); 
        //     // m = # of s3 filter options
        //     // p = max(# of pod_cat values)
        //     // m, p are expected to be small (in comparison to the number of entries) (?)
        //     // explicit loop version below returns faster (at first match, w/o complete set intersection)
        // });
        console.log("RESULT DATA LENGTH " + resultData.length);
        // resultData = resultData1.filter((item) => {

        //     if (item.pod_cat.length === 0){
        //         return false;
        //     }
        //     for (i = 0; i < item.pod_cat.length; i++){
        //         if (s3.includes(item.pod_cat[i])){
        //             return true;
        //         }
        //     }
        //     return false;
        // });

        total_result = resultData.length;

        $("#total").text(total_result);
        total_page = Math.floor((total_result-1) / page_size) +1;
        if (total_page <= 0){
            total_page = 1;
        }
        if (current_page > total_page){
            current_page = total_page;
        }
        if (current_page < 1){
            current_page = 1;
        }

        $('#paging > ul > li').removeClass('hidden active disabled');
        if (total_page >= 3){
            if (current_page === 1){
                $('#paging > ul > li:nth-child(1)').addClass('disabled');
                $('#paging > ul > li:nth-child(2)').addClass('active').attr('data-flow', '1');
                $('#paging > ul > li:nth-child(2) a').text('1');
                $('#paging > ul > li:nth-child(3) a').text('2');
                $('#paging > ul > li:nth-child(3)').attr('data-flow', '2');
                $('#paging > ul > li:nth-child(4) a').text('3');
                $('#paging > ul > li:nth-child(4)').attr('data-flow', '3');
                
            }
            else if (current_page >= total_page){
                //at foremost
                $('#paging > ul > li:nth-child(2) a').text(total_page-2);
                $('#paging > ul > li:nth-child(2)').attr('data-flow', total_page-2);
                $('#paging > ul > li:nth-child(3) a').text(total_page-1);
                $('#paging > ul > li:nth-child(3)').attr('data-flow', total_page-1);
                $('#paging > ul > li:nth-child(4) a').text(total_page);
                $('#paging > ul > li:nth-child(4)').addClass('active').attr('data-flow', total_page);
                $('#paging > ul > li:nth-child(5)').addClass('disabled');
            }
            else{
                //middle
                $('#paging > ul > li:nth-child(2) a').text(current_page-1);
                $('#paging > ul > li:nth-child(2)').attr('data-flow', current_page-1);
                $('#paging > ul > li:nth-child(3) a').text(current_page);
                $('#paging > ul > li:nth-child(3)').addClass('active').attr('data-flow', current_page);
                $('#paging > ul > li:nth-child(4) a').text(current_page+1);
                $('#paging > ul > li:nth-child(4)').attr('data-flow', current_page+1);
                
            }
        }
        else if (total_page === 2){
            $('#paging > ul > li:nth-child(2)').attr('data-flow','1');
            $('#paging > ul > li:nth-child(3)').attr('data-flow','2');
            $('#paging > ul > li:nth-child(2) a').text('1');
            $('#paging > ul > li:nth-child(3) a').text('2');
            $('#paging > ul > li:nth-child(4)').addClass('hidden');
            if (current_page === 1){
                $('#paging > ul > li:nth-child(1)').addClass('disabled');
                $('#paging > ul > li:nth-child(2)').addClass('active');
            }
            else{
                $('#paging > ul > li:nth-child(3)').addClass('active');
                $('#paging > ul > li:nth-child(5)').addClass('disabled');
            }
        }
        else if (total_page === 1){
            $('#paging > ul > li:nth-child(1)').addClass('disabled');
            $('#paging > ul > li:nth-child(2)').addClass('active').attr('data-flow', '1');
            $('#paging > ul > li:nth-child(2) a').text('1');
            $('#paging > ul > li:nth-child(3)').addClass('hidden');
            $('#paging > ul > li:nth-child(4)').addClass('hidden');
            $('#paging > ul > li:nth-child(5)').addClass('disabled');
        }
        //Sort by: sort_by, sort_asc
        current_sort = (a, b)=>{
            if (Array.isArray(a)){
                a = a.join(', ');
            }
            if (Array.isArray(b)){
                b = b.join(', ');
            }
            if (a[sort_by] === b[sort_by]){
                return 0;
            }
            var smaller = (sort_asc === "as")?a[sort_by]:b[sort_by];
            var larger = (sort_asc === "as")?b[sort_by]:a[sort_by];
            if (larger > smaller){
                return -1;
            }
            else{
                return 1;
            }
        };
        resultData.sort(current_sort);
        // console.log(JSON.stringify(resultData));

        resultData = resultData.splice((current_page-1)*page_size, page_size);
        redraw_items();

        var encoded = btoa(JSON.stringify(searching_para));
        const state = {'f': encoded, 'p':current_page, 's':sort_by, 'sa':sort_asc};
        const title = '';
        const queryString = window.location.search;
        const params = new URLSearchParams('');
        params.set('f', encoded);
        params.set('p', current_page);
        params.set('s', sort_by);
        params.set('sa', sort_asc);
        params.set('ps', page_size.toString());
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('popup')){
            params.set('popup', urlParams.get('popup'));
            $('.selecting').removeClass('selecting');
        }

        catalog_library[catalog_json] = resultData;
        console.log("added to library", catalog_library);

        history.pushState(state, title, `${window.location.pathname}?${params}`);
        return;
        return Promise(resultData);
        return $.ajax({});
    }
    panel.getCatalog = getCatalog;

    /**
     * Update the current filters to include the new ones from given catalogue
     * @param {JSON} filters JSON representation of filters for given catalogue
     */
    function updateFilters(filters) {
        filters.forEach(element => {
            var filterable = element[0]; 
            if (!(filterable in searching_para)) { // filterable is not already in the searchable
                searching_para[filterable] = element.slice(1); // add the filterable param to the searching_params
            } else { // filterable is already in the parameters. Add all the elements that are not already in it
                element.slice(1).forEach (val => {
                    if (!searching_para[filterable].includes(val)) {
                        searching_para[filterable].push(val);
                    }
                });
            }
        });
    }


    function init(){
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
            s1: ["SRKW", "NRKW"],
            s2: ["J"],
            s3: ["J", "K", "L"],
        };
        sort_by = 'cn';
        sort_asc = 'as';

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('f')){
            const filter = urlParams.get('f');
            const obj = atob(filter);
            if (obj !== undefined){
                try{
                    const ev = eval('('+obj+')');
                    ['s1','s2','s3'].forEach((v)=>{
                        if (ev[v] !== undefined){
                            searching_para[v] = ev[v];
                        }
                    });
                }catch (e){

                }
            }
        }
        current_page = 1;
        if (urlParams.has('p')){
            const filter = urlParams.get('p');
            current_page = parseInt(filter);
        }
        if (urlParams.has('s') && urlParams.has('sa')){
            const filter = urlParams.get('s');
            sort_by = filter;
            const as = urlParams.get('sa');
            sort_asc = as;
        }
        if (urlParams.has('ps')){
            const filter = urlParams.get('ps');
            const tmp_ps = parseInt(filter);
            if (tmp_ps > 0 && tmp_ps%12 === 0){
                page_size = tmp_ps;
            }
        }

        poped = false;
        Panel = $('#resultgrid');

        total_result = 1;
        total_page = 1;

        $('#sort').selectpicker('val', sort_by);
        $('#sort_a').selectpicker('val', sort_asc);
        $('#page_size').selectpicker('val', ""+page_size);
        $('#show_meta').prop('checked', metadata_show);
        bindEvents();
        if (urlParams.has('popup')){
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            if (urlParams.has('popup')){
                const filter = urlParams.get('popup');
                try{
                    const obj = atob(filter);
                    if (obj !== undefined){
                        const data = eval('('+obj+')');
                        if (data['filename']==undefined){
                            throw new Exception ('Parse Error');
                        }
                        //show details
                        var instance = lity('./'+data.image_file);
                        var template = instance.options('template');
                    }
                }catch (e){
                    document.location.href = page_link;
                }
            }
        }
        getData();
    };
    panel.init = init;

    function get_new(para){
        searching_para = para;
        total_result = undefined;
        current_page = 1;
        getData();
    };
    panel.get_new = get_new;

    function propagate_meta(){
        if (metadata_show){
            $('#gi-area .meta-p').removeClass('hidden');
        }
        else{
            $('#gi-area .meta-p').addClass('hidden');
        }
    }

    function append_items(){
        var i = next_drawn;
        var grid = $('#gi-area').empty();
        for (; i < resultData.length; i++){
            var ele = resultData[i];
            do{
                var tmpid = window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16)+window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
            }while (id_to_seq[tmpid] !== undefined);
            id_to_seq[tmpid] = i;
            var obj = pack_option(tmpid, LIBRARY+'/'+ele.image_file, ele.call_name, ele.pod, ele.clan, LIBRARY+'/'+ele.image_file);
            grid.append(obj);
            
        }
        selecting = 0;
        propagate_meta();
        $('#gi-area .itemblock:nth(0)').click();
        
        if (i !== 0){
            next_drawn = i;
        }
    };
    function redraw_items(){
        id_to_seq = {};
        next_drawn = 0;
        poped = false;
        append_items();
    };
    panel.redraw_items = redraw_items;
    function bindEvents(){
        $('#gi-area').off('click').on('click', '.itemblock .image_pop_source', function(e){
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
        $('#gi-area').on('click', '.play_btn', function(e){
            e.stopPropagation();
            e.preventDefault();
            var obj_id = $(this).parents('.itemblock').attr('id').substring(3);
            var data_target_seq = id_to_seq[obj_id];
            var data_target = resultData[data_target_seq];
            if (audio_element !== undefined && audio_element !== null && audio_element.pause !== undefined){
                audio_element.pause();
            }
            audio_element = document.createElement('audio');
            audio_element.setAttribute('src', '');
            audio_element.setAttribute('src', LIBRARY+'/'+data_target.wav_file);
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
        });
        $('#gi-area').on('click', '.itemblock', function(e){
            $(this).siblings('.itemblock').removeClass('selecting');
            $(this).addClass('selecting');
            selecting = $(this).index();
        });
        var delayed_pop = undefined;
        var keyboard_threshold = 200;
        var keyboard_block = undefined;
        window.addEventListener('keydown', (e)=>{
            let diff = 0;
            let prevent_d = true;
            if (keyboard_block === undefined){
                keyboard_block = setTimeout(()=>{
                    keyboard_block = undefined;
                }, keyboard_threshold);
            }
            else{
                return;
            }
            switch (e.key){
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
                    if (pop_opening){
                        $('#play').click();
                    }
                    else{
                        $('.selecting .play_btn').click();
                    }
                    break;
                case 'Enter':
                    if (!pop_opening){
                        $('.selecting.itemblock .image_pop_source').click();
                    }
                    break;
                default:
                    prevent_d = false;
                    break;
            }
            if (prevent_d){
                e.preventDefault();
            }
            if (diff !== 0 && $('.selecting').length > 0){
                if (selecting + diff >= 0 && selecting + diff < resultData.length){
                    selecting += diff;
                    let target = $('#gi-area .itemblock:nth('+selecting+')');
                    if (target.length >= 0){
                        $(target).siblings().removeClass('selecting');
                        $(target).addClass('selecting');
                        target[0].scrollIntoView({block: "end"});
                        if (poped){
                            if (delayed_pop !== undefined){
                                clearTimeout(delayed_pop);
                            }
                            $('.lity-close').click();
                            delayed_pop = setTimeout(()=>{
                                $('.selecting.itemblock .image_pop_source').click();
                                if ($('.selecting')[0] !== undefined){
                                    $('.selecting')[0].scrollIntoView({block: "end"});
                                }
                                delayed_pop = undefined;
                            }, 100);
                        }
                    }
                    else{
                        selecting -= diff;
                    }
                }
            }
            else if (diff !== 0){
                //toast
                $('.toast').addClass('show');
                setTimeout(()=>{
                    $('.toast').removeClass('show');
                }, 800);
            }
        });
        $('#paging > ul > li').click(function(e){
            e.stopPropagation();
            e.preventDefault();
            if ($(this).hasClass('disabled') || $(this).hasClass('hidden')  || $(this).hasClass('active')){
                return;
            }
            var data_flow = $(this).attr('data-flow');
            if (data_flow === 'n'){
                current_page += 1;
            }
            else if (data_flow === 'p'){
                current_page -= 1;
            }
            else{
                current_page = parseInt(data_flow);
                if (isNaN(current_page)){
                    current_page = 1;
                }
            }
            $('#resultgrid > div.container > div.row.justify-content-md-center > div.col.col-12.col-sm-12.col-md-12.col-lg-8.col-xl-6.col-xxl-6.row.align-items-center.align-middle > span').focus();
            getData();
        });

        $(document).on('lity:open', function(event, instance) {
            lity_data = [];
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            if (poped != undefined && !urlParams.has('popup')){
                var data_target_seq = id_to_seq[poped];
                var data_target = resultData[data_target_seq];
                lity_data = data_target;
                var encoded_data = btoa(JSON.stringify(data_target));
                var encoded = btoa(JSON.stringify(searching_para));
                const state = {'f': encoded, 'p':current_page, 's':sort_by, 'sa':sort_asc, 'popup':encoded_data};
                const title = 'Details: '+lity_data.cn+' (Call Name)';//For Safari only
                const params = new URLSearchParams('');
                params.set('f', encoded);
                params.set('p', current_page);
                params.set('s', sort_by);
                params.set('sa', sort_asc);
                params.set('ps', page_size.toString());
                params.set('popup', encoded_data);
        
                history.pushState(state, title, `${window.location.pathname}?${params}`);
            }
            else if (urlParams.has('popup')){
                //may be generated from link
                const filter = urlParams.get('popup');
                const obj = atob(filter);
                if (obj !== undefined){
                    try{
                        lity_data = eval('('+obj+')');
                        $('.selecting').removeClass('selecting');
                    }catch (e){
                        document.location.href = page_link;
                    }
                }
                else{
                    document.location.href = page_link;
                }
                // console.log(lity_data);
            }
            else{
                //something went wrong
                document.location.href = page_link;
            }
            let play_btn = '<button id="play" class="col btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
                            </svg>Play (Call Name: '+lity_data.cn+') </button>';
            let additional_row = '';
            //lity_data["subclan"] = "Testing Clan";
            //lity_data["subpopulation"] = "Testing Population";
            if (lity_data["subpopulation"] !== undefined && 
                lity_data["subpopulation"] !== null &&
                lity_data["subpopulation"].length > 0){
                let population = {'SRKW':"Southern Resident", 'NRKW':"Northern Resident"}[lity_data['population']];
                
                additional_row += '<div class="row text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>Population: '+ population +'</span></div>';
                additional_row += '<div class="col-12 col-sm-6"><span>Sub-Population: '+lity_data['subpopulation']+'</span></div></div>';
            }
            if (lity_data["subclan"] !== undefined && 
                lity_data["subclan"] !== null &&
                lity_data["subclan"].length > 0){
                    additional_row += '<div class="row text-start text-info border-2 border-light border-bottom"><div class="col-12 col-sm-6"><span>Clan: '+lity_data['clan']+'</span></div>';
                    additional_row += '<div class="col-12 col-sm-6"><span>Sub-Clan: '+lity_data['subclan']+'</span></div></div>';
            }
            let items_count = ((lity_data["sample"] !== undefined && 
                lity_data["sample"] !== null &&
                lity_data["sample"].length > 0)?1:0) +
                ((lity_data["mar"] !== undefined && 
                lity_data["mar"] !== null &&
                lity_data["mar"].length > 0)?1:0);
            let alignment = "text-sm-center";
            if (items_count > 1){
                alignment = "";
            }
            if (items_count){
                additional_row += '<div class="row '+alignment+' text-start text-info border-2 border-light border-bottom">';
            }
            
            if (lity_data["sample"] !== undefined && 
                lity_data["sample"] !== null &&
                lity_data["sample"].length > 0){
                additional_row += '<div class="col"><span>Sample: '+lity_data['sample']+'</span></div>';
            }
            if (lity_data["mar"] !== undefined && 
                lity_data["mar"] !== null &&
                lity_data["mar"].length > 0){
                additional_row += '<div class="col"><span>Matrilines: '+lity_data['mar']+'</span></div>';
            }
            if (items_count){
                additional_row += '</div';
            }
            $('.lity-container').append('<div class="container-fluid litybottom"><div class="row">'+play_btn+'</div>'+ additional_row+'</div>');
            
            // file = 'resources_config/sample.md'
            file = media_folder_path + lity_data['description-file']
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
        });
        $(document).on('click', '.lity-container #play', function(){
            audio_element = document.createElement('audio');
            $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
            <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
          </svg>Playing  (Call Name: '+lity_data.cn+')');
            $(this).removeClass('btn-primary').addClass('btn-success');
            audio_element.setAttribute('src', '');
            audio_element.setAttribute('src', LIBRARY+'/'+lity_data.wav_file);
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
            audio_element.addEventListener('ended', function(){
                $("#play").html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
              </svg>Play  (Call Name: '+lity_data.cn+')').addClass('btn-primary').removeClass('btn-success');
            
            })
        });
        $(document).on('lity:close', function(event, instance) {
            if (audio_element !== undefined && audio_element.setAttribute !== undefined){
                //pause unfinished playing when close
                audio_element.setAttribute('src', '');
                audio_element.pause();
            }
            poped = undefined;
            pop_opening = false;
            var encoded = btoa(JSON.stringify(searching_para));
            const state = {'f': encoded, 'p':current_page, 's':sort_by, 'sa':sort_asc};
            const title = '';
            const params = new URLSearchParams('');
            params.set('f', encoded);
            params.set('p', current_page);
            params.set('s', sort_by);
            params.set('sa', sort_asc);
            params.set('ps', page_size.toString());
            history.pushState(state, title, `${window.location.pathname}?${params}`);
            if ($('.selecting').length <= 0){
                $('#gi-area .itemblock:nth(0)').addClass('selecting');
            }
        });
        $('#show_meta').change(function(){
            if ($(this).prop('checked')){
				metadata_show = true;
			}
			else{
				metadata_show = false;
			}
            propagate_meta();
		});
        $('#sort').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            sort_by = $('#sort').selectpicker('val');
            getData();
        });
        $('#sort_a').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            sort_asc = $('#sort_a').selectpicker('val');
            getData();
        });
        $('#page_size').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            page_size = parseInt($('#page_size').selectpicker('val'));
            getData();
        });
    }
}(GridPanel || (GridPanel = {})));
