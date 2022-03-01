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
    var page_size = 12;
    var total_result = undefined;
    var total_page = undefined;

    var poped = undefined;
    var audio_element = undefined;
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
    function pack_option(id, thumb, callname, matrilines, pod, clan, full){
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
        if (callname === undefined || callname === null){
            callname = "Unknown";
        }
        if (matrilines === undefined || matrilines === null){
            matrilines = "N/A";
        }
        return '<div class="col-xxl-2 col-xl-2 col-lg-3 col-md-3 col-sm-4 mb-4 itemblock" id="gi-'+id+'">\
            <div class="bg-white rounded shadow-sm"><a href="'+full+'" data-toggle="lightbox" class="image_pop_source text-decoration-none" data-type="image" data-gallery="gallery">\
            <img src="'+thumb+'" alt="" class="img-fluid card-img-top"></a>\
            <div class="p-4">\
                <h5> <a class="play_btn" href="#">'+play_icon+'<span class="text-dark">'+callname+'</span></a></h5>\
                <p class="small mb-0 meta-p"><span class="font-weight-bold">Pods: '+pod+'</span></p>\
                <!--<p class="small text-muted mb-0">Matrilines: <br>'+matrilines+'</p>-->\
                <div class="meta-p d-flex align-items-center justify-content-between rounded-pill bg-light px-3 py-2 mt-4">\
                <div class="badge badge-warning px-3 rounded-pill font-weight-normal"><span class="font-weight-bold  text-dark">Clan: '+clan+'</span></div>\
                </div>\
            </div>\
            </div>\
        </div>';
    }
    function open_popup(){

    };
    function close_popup(){

    };
    async function getData(){
        /*
        var fake_datasource = [
            {
                "filename": "BCS44-Jpod",
                "clan": "J",
                "thumb": "BCS44-Jpod.jpg",
                "cn":"BCS44-Jpod",
                "mar": "123123123",
                "pod_cat": ["K", "J"],
                "pod": "J1pod" //useless
            },
            {
                "filename": "BCS01-Jpod",
                "clan": "J",
                "thumb": "BCS01-Jpod.jpg",
                "cn":"BCS01-Jpod",
                "mar": "1fff",
                "pod_cat": ["J"],
                "pod": "Jpod" //useless
            }
        ];*/
        var simple_datasource = [{"filename":"BCS05-Jpod","thumb":"BCS05-Jpod.jpg","clan":"J","cn":"S05","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS05-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS05-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S05","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS05-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS05-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S05","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS18-K01pod-2","thumb":"BCS18-K01pod-2.jpg","clan":"J","cn":"S18","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS22-Lpod","thumb":"BCS22-Lpod.jpg","clan":"J","cn":"S22","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS09-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS09-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S09","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS40-Lpod","thumb":"BCS40-Lpod.jpg","clan":"J","cn":"S40","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS12-Jpod","thumb":"BCS12-Jpod.jpg","clan":"J","cn":"S12","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02iii-L01pod-JL04,L09,L26andL37mat-1","thumb":"BCS02iii-L01pod-JL04,L09,L26andL37mat-1.jpg","clan":"J","cn":"S02iii","pod":"L01pod","mar":"JL04,L09,L26andL37mat-1","pod_cat":["L"]},{"filename":"BCS44-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS44-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S44","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS08i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS08i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S08i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS42-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS42-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S42","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS36-Lpod","thumb":"BCS36-Lpod.jpg","clan":"J","cn":"S36","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS41-Jpod","thumb":"BCS41-Jpod.jpg","clan":"J","cn":"S41","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS37ii-Lpod","thumb":"BCS37ii-Lpod.jpg","clan":"J","cn":"S37ii","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS12-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS12-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S12","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS01-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS01-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S01","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS07-J01pod-1","thumb":"BCS07-J01pod-1.jpg","clan":"J","cn":"S07","pod":"J01pod","mar":"1","pod_cat":["J"]},{"filename":"BCS17-K01andL01pods-2","thumb":"BCS17-K01andL01pods-2.jpg","clan":"J","cn":"S17","pod":"K01andL01pods","mar":"2","pod_cat":["K","L"]},{"filename":"BCS36-K01andL01pods","thumb":"BCS36-K01andL01pods.jpg","clan":"J","cn":"S36","pod":"K01andL01pods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS37i-Jpod","thumb":"BCS37i-Jpod.jpg","clan":"J","cn":"S37i","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS14-Jpod","thumb":"BCS14-Jpod.jpg","clan":"J","cn":"S14","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02ii-Jpod","thumb":"BCS02ii-Jpod.jpg","clan":"J","cn":"S02ii","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS44-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS44-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S44","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS02iii-Lpod","thumb":"BCS02iii-Lpod.jpg","clan":"J","cn":"S02iii","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS16-K01andL01pods-2","thumb":"BCS16-K01andL01pods-2.jpg","clan":"J","cn":"S16","pod":"K01andL01pods","mar":"2","pod_cat":["K","L"]},{"filename":"BCS37i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS37i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S37i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS16-KandLpods","thumb":"BCS16-KandLpods.jpg","clan":"J","cn":"S16","pod":"KandLpods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS13i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS13i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S13i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS09-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS09-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S09","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS12-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS12-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S12","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS03-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS03-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S03","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS06-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS06-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S06","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS31-L01pod-L09andL35mat-2","thumb":"BCS31-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"S31","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS33-K01pod-2","thumb":"BCS33-K01pod-2.jpg","clan":"J","cn":"S33","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS01-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS01-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S01","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS02ii-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS02ii-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S02ii","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS06-Jpod","thumb":"BCS06-Jpod.jpg","clan":"J","cn":"S06","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS40-L01pod-L09andL35mat-1","thumb":"BCS40-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"S40","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS31-L01pod-L09andL35mat-1","thumb":"BCS31-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"S31","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS07-J01pod-2","thumb":"BCS07-J01pod-2.jpg","clan":"J","cn":"S07","pod":"J01pod","mar":"2","pod_cat":["J"]},{"filename":"BCS41-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS41-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S41","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS03-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS03-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S03","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-2","thumb":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-2.jpg","clan":"J","cn":"S13ii","pod":"K01andL01pods","mar":"K01,K04,K07,K18,L04,L12andL25mat-2","pod_cat":["K","L"]},{"filename":"BCS10-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS10-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S10","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS01-Jpod","thumb":"BCS01-Jpod.jpg","clan":"J","cn":"S01","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS02i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S02i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS37i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS37i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S37i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS37ii-L01pod-L09andL35mat-2","thumb":"BCS37ii-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"S37ii","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS42-JandLpods","thumb":"BCS42-JandLpods.jpg","clan":"J","cn":"S42","pod":"JandLpods","mar":null,"pod_cat":["J","L"]},{"filename":"BCS22-K01pod-2","thumb":"BCS22-K01pod-2.jpg","clan":"J","cn":"S22","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS02i-Jpod","thumb":"BCS02i-Jpod.jpg","clan":"J","cn":"S02i","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS33-K01pod-1","thumb":"BCS33-K01pod-1.jpg","clan":"J","cn":"S33","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS19-K01andL01pods","thumb":"BCS19-K01andL01pods.jpg","clan":"J","cn":"S19","pod":"K01andL01pods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS14-J01pod-J02,J07,J08andJ09mat","thumb":"BCS14-J01pod-J02,J07,J08andJ09mat.jpg","clan":"J","cn":"S14","pod":"J01pod","mar":"J02,J07,J08andJ09mat","pod_cat":["J"]},{"filename":"BCS02ii-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS02ii-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S02ii","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS04-Jpod","thumb":"BCS04-Jpod.jpg","clan":"J","cn":"S04","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS10-JKandLpods","thumb":"BCS10-JKandLpods.jpg","clan":"J","cn":"S10","pod":"JKandLpods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS06-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS06-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S06","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS09-Jpod","thumb":"BCS09-Jpod.jpg","clan":"J","cn":"S09","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS42-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS42-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S42","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS17-K01andL01pods-1","thumb":"BCS17-K01andL01pods-1.jpg","clan":"J","cn":"S17","pod":"K01andL01pods","mar":"1","pod_cat":["K","L"]},{"filename":"BCS19-K01pod","thumb":"BCS19-K01pod.jpg","clan":"J","cn":"S19","pod":"K01pod","mar":null,"pod_cat":["K"]},{"filename":"BCS18-Lpod","thumb":"BCS18-Lpod.jpg","clan":"J","cn":"S18","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS08ii-JandLpods","thumb":"BCS08ii-JandLpods.jpg","clan":"J","cn":"S08ii","pod":"JandLpods","mar":null,"pod_cat":["J","L"]},{"filename":"BCS04-J01pod-2","thumb":"BCS04-J01pod-2.jpg","clan":"J","cn":"S04","pod":"J01pod","mar":"2","pod_cat":["J"]},{"filename":"BCS13i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS13i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"S13i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS04-J01pod-1","thumb":"BCS04-J01pod-1.jpg","clan":"J","cn":"S04","pod":"J01pod","mar":"1","pod_cat":["J"]},{"filename":"BCS08i-L01pod-L09andL35mat-1","thumb":"BCS08i-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"S08i","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS08i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS08i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S08i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS16-K01andL01pods-1","thumb":"BCS16-K01andL01pods-1.jpg","clan":"J","cn":"S16","pod":"K01andL01pods","mar":"1","pod_cat":["K","L"]},{"filename":"BCS41-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS41-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S41","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS03-Jpod","thumb":"BCS03-Jpod.jpg","clan":"J","cn":"S03","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS19-J01,K01andL01pods","thumb":"BCS19-J01,K01andL01pods.jpg","clan":"J","cn":"S19","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS18-K01pod-1","thumb":"BCS18-K01pod-1.jpg","clan":"J","cn":"S18","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS37ii-J01,K01andL01pods","thumb":"BCS37ii-J01,K01andL01pods.jpg","clan":"J","cn":"S37ii","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS10-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS10-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S10","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS07-Jpod","thumb":"BCS07-Jpod.jpg","clan":"J","cn":"S07","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS44-Jpod","thumb":"BCS44-Jpod.jpg","clan":"J","cn":"S44","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS36-J01,K01andL01pods","thumb":"BCS36-J01,K01andL01pods.jpg","clan":"J","cn":"S36","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-1","thumb":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-1.jpg","clan":"J","cn":"S13ii","pod":"K01andL01pods","mar":"K01,K04,K07,K18,L04,L12andL25mat-1","pod_cat":["K","L"]},{"filename":"BCS02iii-L01pod-JL04,L09,L26andL37mat-2","thumb":"BCS02iii-L01pod-JL04,L09,L26andL37mat-2.jpg","clan":"J","cn":"S02iii","pod":"L01pod","mar":"JL04,L09,L26andL37mat-2","pod_cat":["L"]},{"filename":"BCS31-Lpod","thumb":"BCS31-Lpod.jpg","clan":"J","cn":"S31","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS08i-L01pod-L09andL35mat-2","thumb":"BCS08i-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"S08i","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS02i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS02i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"S02i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS19-Lpod","thumb":"BCS19-Lpod.jpg","clan":"J","cn":"S19","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS17-KandLpods","thumb":"BCS17-KandLpods.jpg","clan":"J","cn":"S17","pod":"KandLpods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS22-K01pod-1","thumb":"BCS22-K01pod-1.jpg","clan":"J","cn":"S22","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS17-K01andL01pods-3","thumb":"BCS17-K01andL01pods-3.jpg","clan":"J","cn":"S17","pod":"K01andL01pods","mar":"3","pod_cat":["K","L"]},{"filename":"BCS40-L01pod-L09andL35mat-2","thumb":"BCS40-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"S40","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]}];
        var s1 = searching_para['s1'];
        var s2 = searching_para['s2'];
        var s3 = searching_para['s3'];

        //Filter: searching_para
        var resultData1 = simple_datasource.filter(item => s2.includes(item.clan));
        resultData = resultData1.filter((item) => {
            if (item.pod_cat.length === 0){
                return false;
            }
            for (i = 0; i < item.pod_cat.length; i++){
                if (s3.includes(item.pod_cat[i])){
                    return true;
                }
            }
            return false;
        });

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
        }

        history.pushState(state, title, `${window.location.pathname}?${params}`);
        return;
        return $.ajax({});
    }
    panel.getData = getData;

    function init(){
        resultData = [];
        id_to_seq = {};
        next_drawn = 0;
        metadata_show = true;
        searching_para = {
            s1: ["S"],
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
                            var instance = lity('./simple/'+data['filename']+'.jpg');
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
            var obj = pack_option(tmpid, './simple/'+ele.thumb, ele.cn, ele.mar, ele.pod_cat, ele.clan, './simple/'+ele.filename+'.jpg');
            grid.append(obj);
            
        }
        propagate_meta();

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
            var obj_id = $(this).parents('.itemblock').attr('id').substring(3);
            poped = obj_id;
            var data_target_seq = id_to_seq[obj_id];
            var data_target = resultData[data_target_seq];
            
            var instance = lity($(this).attr('href'));
            var template = instance.options('template');
        });
        $('#gi-area').on('click', '.play_btn', function(e){
            e.stopPropagation();
            e.preventDefault();
            var obj_id = $(this).parents('.itemblock').attr('id').substring(3);
            poped = obj_id;
            var data_target_seq = id_to_seq[obj_id];
            var data_target = resultData[data_target_seq];
            if (audio_element !== undefined && audio_element !== null && audio_element.pause !== undefined){
                audio_element.pause();
            }
            audio_element = document.createElement('audio');
            audio_element.setAttribute('src', '');
            audio_element.setAttribute('src', './simple/'+data_target.filename+'.wav');
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
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
            var lity_data = [];
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
                    }catch (e){
                        document.location.href = page_link;
                    }
                }
            }
            else{
                //something went wrong
                document.location.href = page_link;
            }
            $('.lity-container').append('<div class="container litybottom"><div class="row"><button id="play" class="col btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
            <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
          </svg>Play (Call Name: '+lity_data.cn+') </button></div></div>');
            $("#play").off('click').on('click', function(){
                audio_element = document.createElement('audio');
                $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
              </svg>Playing  (Call Name: '+lity_data.cn+')');
                $(this).removeClass('btn-primary').addClass('btn-success');
                audio_element.setAttribute('src', '');
                audio_element.setAttribute('src', './simple/'+lity_data.filename+'.wav');
                audio_element.setAttribute('autoplay', 'autoplay');
                audio_element.load();
                audio_element.addEventListener('ended', function(){
                    $("#play").html('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                    <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
                  </svg>Play  (Call Name: '+lity_data.cn+')').addClass('btn-primary').removeClass('btn-success');
                
                })
            });
        });
        $(document).on('lity:close', function(event, instance) {
            if (audio_element !== undefined && audio_element.setAttribute !== undefined){
                //pause unfinished playing when close
                audio_element.setAttribute('src', '');
                audio_element.pause();
            }
            poped = undefined;
            var encoded = btoa(JSON.stringify(searching_para));
            const state = {'f': encoded, 'p':current_page, 's':sort_by, 'sa':sort_asc};
            const title = '';
            const params = new URLSearchParams('');
            params.set('f', encoded);
            params.set('p', current_page);
            params.set('s', sort_by);
            params.set('sa', sort_asc);
            params.set('ps', page_size.toString());
            history.pushState(state, title, `${window.location.pathname}?${params}`)

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