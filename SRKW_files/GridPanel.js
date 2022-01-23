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

    var poped = undefined;
    var audio_element = undefined;

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
                <h5> <a class="play_btn" href="#"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                <path fill="currentColor" d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
              </svg><span class="text-dark">'+callname+'</span></a></h5>\
                <p class="small mb-0"><span class="font-weight-bold">Pods: '+pod+'</span></p>\
                <p class="small text-muted mb-0">Matrilines: '+matrilines+'</p>\
                <div class="d-flex align-items-center justify-content-between rounded-pill bg-light px-3 py-2 mt-4">\
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
        var fake_datasource = [{"filename":"BCS05-Jpod","thumb":"BCS05-Jpod.jpg","clan":"J","cn":"BCS05","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS05-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS05-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS05","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS05-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS05-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS05","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS18-K01pod-2","thumb":"BCS18-K01pod-2.jpg","clan":"J","cn":"BCS18","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS22-Lpod","thumb":"BCS22-Lpod.jpg","clan":"J","cn":"BCS22","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS09-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS09-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS09","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS40-Lpod","thumb":"BCS40-Lpod.jpg","clan":"J","cn":"BCS40","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS12-Jpod","thumb":"BCS12-Jpod.jpg","clan":"J","cn":"BCS12","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02iii-L01pod-JL04,L09,L26andL37mat-1","thumb":"BCS02iii-L01pod-JL04,L09,L26andL37mat-1.jpg","clan":"J","cn":"BCS02iii","pod":"L01pod","mar":"JL04,L09,L26andL37mat-1","pod_cat":["L"]},{"filename":"BCS44-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS44-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS44","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS08i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS08i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS08i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS42-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS42-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS42","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS36-Lpod","thumb":"BCS36-Lpod.jpg","clan":"J","cn":"BCS36","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS41-Jpod","thumb":"BCS41-Jpod.jpg","clan":"J","cn":"BCS41","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS37ii-Lpod","thumb":"BCS37ii-Lpod.jpg","clan":"J","cn":"BCS37ii","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS12-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS12-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS12","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS01-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS01-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS01","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS07-J01pod-1","thumb":"BCS07-J01pod-1.jpg","clan":"J","cn":"BCS07","pod":"J01pod","mar":"1","pod_cat":["J"]},{"filename":"BCS17-K01andL01pods-2","thumb":"BCS17-K01andL01pods-2.jpg","clan":"J","cn":"BCS17","pod":"K01andL01pods","mar":"2","pod_cat":["K","L"]},{"filename":"BCS36-K01andL01pods","thumb":"BCS36-K01andL01pods.jpg","clan":"J","cn":"BCS36","pod":"K01andL01pods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS37i-Jpod","thumb":"BCS37i-Jpod.jpg","clan":"J","cn":"BCS37i","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS14-Jpod","thumb":"BCS14-Jpod.jpg","clan":"J","cn":"BCS14","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02ii-Jpod","thumb":"BCS02ii-Jpod.jpg","clan":"J","cn":"BCS02ii","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS44-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS44-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS44","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS02iii-Lpod","thumb":"BCS02iii-Lpod.jpg","clan":"J","cn":"BCS02iii","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS16-K01andL01pods-2","thumb":"BCS16-K01andL01pods-2.jpg","clan":"J","cn":"BCS16","pod":"K01andL01pods","mar":"2","pod_cat":["K","L"]},{"filename":"BCS37i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS37i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS37i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS16-KandLpods","thumb":"BCS16-KandLpods.jpg","clan":"J","cn":"BCS16","pod":"KandLpods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS13i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS13i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS13i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS09-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS09-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS09","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS12-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS12-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS12","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS03-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS03-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS03","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS06-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS06-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS06","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS31-L01pod-L09andL35mat-2","thumb":"BCS31-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"BCS31","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS33-K01pod-2","thumb":"BCS33-K01pod-2.jpg","clan":"J","cn":"BCS33","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS01-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS01-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS01","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS02ii-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS02ii-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS02ii","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS06-Jpod","thumb":"BCS06-Jpod.jpg","clan":"J","cn":"BCS06","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS40-L01pod-L09andL35mat-1","thumb":"BCS40-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"BCS40","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS31-L01pod-L09andL35mat-1","thumb":"BCS31-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"BCS31","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS07-J01pod-2","thumb":"BCS07-J01pod-2.jpg","clan":"J","cn":"BCS07","pod":"J01pod","mar":"2","pod_cat":["J"]},{"filename":"BCS41-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS41-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS41","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS03-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS03-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS03","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-2","thumb":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-2.jpg","clan":"J","cn":"BCS13ii","pod":"K01andL01pods","mar":"K01,K04,K07,K18,L04,L12andL25mat-2","pod_cat":["K","L"]},{"filename":"BCS10-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS10-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS10","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS01-Jpod","thumb":"BCS01-Jpod.jpg","clan":"J","cn":"BCS01","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS02i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS02i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS02i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS37i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS37i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS37i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS37ii-L01pod-L09andL35mat-2","thumb":"BCS37ii-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"BCS37ii","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS42-JandLpods","thumb":"BCS42-JandLpods.jpg","clan":"J","cn":"BCS42","pod":"JandLpods","mar":null,"pod_cat":["J","L"]},{"filename":"BCS22-K01pod-2","thumb":"BCS22-K01pod-2.jpg","clan":"J","cn":"BCS22","pod":"K01pod","mar":"2","pod_cat":["K"]},{"filename":"BCS02i-Jpod","thumb":"BCS02i-Jpod.jpg","clan":"J","cn":"BCS02i","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS33-K01pod-1","thumb":"BCS33-K01pod-1.jpg","clan":"J","cn":"BCS33","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS19-K01andL01pods","thumb":"BCS19-K01andL01pods.jpg","clan":"J","cn":"BCS19","pod":"K01andL01pods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS14-J01pod-J02,J07,J08andJ09mat","thumb":"BCS14-J01pod-J02,J07,J08andJ09mat.jpg","clan":"J","cn":"BCS14","pod":"J01pod","mar":"J02,J07,J08andJ09mat","pod_cat":["J"]},{"filename":"BCS02ii-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS02ii-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS02ii","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS04-Jpod","thumb":"BCS04-Jpod.jpg","clan":"J","cn":"BCS04","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS10-JKandLpods","thumb":"BCS10-JKandLpods.jpg","clan":"J","cn":"BCS10","pod":"JKandLpods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS06-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS06-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS06","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS09-Jpod","thumb":"BCS09-Jpod.jpg","clan":"J","cn":"BCS09","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS42-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS42-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS42","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS17-K01andL01pods-1","thumb":"BCS17-K01andL01pods-1.jpg","clan":"J","cn":"BCS17","pod":"K01andL01pods","mar":"1","pod_cat":["K","L"]},{"filename":"BCS19-K01pod","thumb":"BCS19-K01pod.jpg","clan":"J","cn":"BCS19","pod":"K01pod","mar":null,"pod_cat":["K"]},{"filename":"BCS18-Lpod","thumb":"BCS18-Lpod.jpg","clan":"J","cn":"BCS18","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS08ii-JandLpods","thumb":"BCS08ii-JandLpods.jpg","clan":"J","cn":"BCS08ii","pod":"JandLpods","mar":null,"pod_cat":["J","L"]},{"filename":"BCS04-J01pod-2","thumb":"BCS04-J01pod-2.jpg","clan":"J","cn":"BCS04","pod":"J01pod","mar":"2","pod_cat":["J"]},{"filename":"BCS13i-J01pod-J02,J07,J08andJ09mat-1","thumb":"BCS13i-J01pod-J02,J07,J08andJ09mat-1.jpg","clan":"J","cn":"BCS13i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-1","pod_cat":["J"]},{"filename":"BCS04-J01pod-1","thumb":"BCS04-J01pod-1.jpg","clan":"J","cn":"BCS04","pod":"J01pod","mar":"1","pod_cat":["J"]},{"filename":"BCS08i-L01pod-L09andL35mat-1","thumb":"BCS08i-L01pod-L09andL35mat-1.jpg","clan":"J","cn":"BCS08i","pod":"L01pod","mar":"L09andL35mat-1","pod_cat":["L"]},{"filename":"BCS08i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS08i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS08i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS16-K01andL01pods-1","thumb":"BCS16-K01andL01pods-1.jpg","clan":"J","cn":"BCS16","pod":"K01andL01pods","mar":"1","pod_cat":["K","L"]},{"filename":"BCS41-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS41-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS41","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS03-Jpod","thumb":"BCS03-Jpod.jpg","clan":"J","cn":"BCS03","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS19-J01,K01andL01pods","thumb":"BCS19-J01,K01andL01pods.jpg","clan":"J","cn":"BCS19","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS18-K01pod-1","thumb":"BCS18-K01pod-1.jpg","clan":"J","cn":"BCS18","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS37ii-J01,K01andL01pods","thumb":"BCS37ii-J01,K01andL01pods.jpg","clan":"J","cn":"BCS37ii","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS10-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS10-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS10","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS07-Jpod","thumb":"BCS07-Jpod.jpg","clan":"J","cn":"BCS07","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS44-Jpod","thumb":"BCS44-Jpod.jpg","clan":"J","cn":"BCS44","pod":"Jpod","mar":null,"pod_cat":["J"]},{"filename":"BCS36-J01,K01andL01pods","thumb":"BCS36-J01,K01andL01pods.jpg","clan":"J","cn":"BCS36","pod":"J01,K01andL01pods","mar":null,"pod_cat":["J","K","L"]},{"filename":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-1","thumb":"BCS13ii-K01andL01pods-K01,K04,K07,K18,L04,L12andL25mat-1.jpg","clan":"J","cn":"BCS13ii","pod":"K01andL01pods","mar":"K01,K04,K07,K18,L04,L12andL25mat-1","pod_cat":["K","L"]},{"filename":"BCS02iii-L01pod-JL04,L09,L26andL37mat-2","thumb":"BCS02iii-L01pod-JL04,L09,L26andL37mat-2.jpg","clan":"J","cn":"BCS02iii","pod":"L01pod","mar":"JL04,L09,L26andL37mat-2","pod_cat":["L"]},{"filename":"BCS31-Lpod","thumb":"BCS31-Lpod.jpg","clan":"J","cn":"BCS31","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS08i-L01pod-L09andL35mat-2","thumb":"BCS08i-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"BCS08i","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]},{"filename":"BCS02i-J01pod-J02,J07,J08andJ09mat-2","thumb":"BCS02i-J01pod-J02,J07,J08andJ09mat-2.jpg","clan":"J","cn":"BCS02i","pod":"J01pod","mar":"J02,J07,J08andJ09mat-2","pod_cat":["J"]},{"filename":"BCS19-Lpod","thumb":"BCS19-Lpod.jpg","clan":"J","cn":"BCS19","pod":"Lpod","mar":null,"pod_cat":["L"]},{"filename":"BCS17-KandLpods","thumb":"BCS17-KandLpods.jpg","clan":"J","cn":"BCS17","pod":"KandLpods","mar":null,"pod_cat":["K","L"]},{"filename":"BCS22-K01pod-1","thumb":"BCS22-K01pod-1.jpg","clan":"J","cn":"BCS22","pod":"K01pod","mar":"1","pod_cat":["K"]},{"filename":"BCS17-K01andL01pods-3","thumb":"BCS17-K01andL01pods-3.jpg","clan":"J","cn":"BCS17","pod":"K01andL01pods","mar":"3","pod_cat":["K","L"]},{"filename":"BCS40-L01pod-L09andL35mat-2","thumb":"BCS40-L01pod-L09andL35mat-2.jpg","clan":"J","cn":"BCS40","pod":"L01pod","mar":"L09andL35mat-2","pod_cat":["L"]}];
        var s1 = searching_para['s1'];
        var s2 = searching_para['s2'];
        var s3 = searching_para['s3'];

        //Filter: searching_para
        var resultData1 = fake_datasource.filter(item => s2.includes(item.clan));
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
        redraw_items();
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
        poped = false;
        Panel = $('#resultgrid');
        $('#sort').selectpicker('val', sort_by);
        $('#sort_a').selectpicker('val', sort_asc);
        
        bindEvents();
        getData();
    };
    panel.init = init;

    function get_new(para){
        searching_para = para;
        getData();
    };
    panel.get_new = get_new;

    function append_items(){
        var i = next_drawn;
        var grid = $('#gi-area').empty();
        for (; i < resultData.length; i++){
            var ele = resultData[i];
            do{
                var tmpid = window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16)+window.crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
            }while (id_to_seq[tmpid] !== undefined);
            id_to_seq[tmpid] = i;
            var obj = pack_option(tmpid, './fake/'+ele.thumb, ele.cn, ele.mar, ele.pod_cat, ele.clan, './fake/'+ele.filename+'.jpg');
            grid.append(obj);
            
        }
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
            audio_element.setAttribute('src', './fake/'+data_target.filename+'.wav');
            audio_element.setAttribute('autoplay', 'autoplay');
            audio_element.load();
        });
        $(document).on('lity:open', function(event, instance) {
            $('.lity-container').append('<div class="container"><div class="row"><button id="play" class="col btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
            <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
          </svg>Play</button></div></div>');
            $("#play").off('click').on('click', function(){
                audio_element = document.createElement('audio');
                var data_target_seq = id_to_seq[poped];
                var data_target = resultData[data_target_seq];
                $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
              </svg>Playing');
                $(this).removeClass('btn-primary').addClass('btn-success');
                audio_element.setAttribute('src', '');
                audio_element.setAttribute('src', './fake/'+data_target.filename+'.wav');
                audio_element.setAttribute('autoplay', 'autoplay');
                audio_element.load();
                audio_element.addEventListener('ended', function(){
                    $("#play").html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">\
                    <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/>\
                  </svg>Play').addClass('btn-primary').removeClass('btn-success');
                
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
        });
        
        $('#sort').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            sort_by = $('#sort').selectpicker('val');
            getData();
        });
        $('#sort_a').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            sort_asc = $('#sort_a').selectpicker('val');
            getData();
        });
    }
}(GridPanel || (GridPanel = {})));