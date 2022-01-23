var SearchPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var originalData = undefined;
    var tmpResult = undefined;
    var s_options = [
        {
            "s": "s1",
            "b": "b1",
            "option":[
                {"v":"S", "text":"Southern Resident", "default":true},
                {"v":"N", "text":"Northern Resident"},
                {"v":"T", "text":"Transient"},
            ]
        },
        {
            "s": "s2",
            "b": "b2",
            "option":[
                {"v":"J", "text":"J", "default":true}
            ]
        },
        {
            "s": "s3",
            "b": "b3",
            "option":[
                {"v":"J", "text":"J", "default":true},
                {"v":"K", "text":"K", "default":true},
                {"v":"L", "text":"L", "default":true},
            ]
        },
    ];
    var dirty = false;
    function pack_option(v, a){
        return '<option value="'+v+'">'+a+'</option>'
    }
    function init(){
        originalData = {
            s1: ["S"],
            s2: ["J"],
            s3: ["J", "K", "L"],
        };
        tmpResult = $.extend(true, {}, originalData);
        Panel = $('.panel');

        s_options.forEach((value)=>{
            Panel.find('#'+value.s).empty();
            var default_option = [];
            value.option.forEach((op_val)=>{
                Panel.find('#'+value.s).append(pack_option(op_val.v, op_val.text));
                if (op_val.default !== undefined && op_val.default){
                    default_option.push(op_val.v);
                }
            });
            $('#'+value.s).selectpicker();
            //mobile only //$('#'+value.s).selectpicker('mobile', true);
            $('#'+value.s).selectpicker('val', default_option);
        });
        bindEvents();
    };
    panel.init = init;

    function bindEvents(){
        $('#s1').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            tmpResult['s1'] = $('#s1').selectpicker('val');
        });
        $('#s2').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            tmpResult['s2'] = $('#s2').selectpicker('val');
        });
        $('#s3').on('changed.bs.select',(e, clickedIndex, isSelected, previousValue)=>{
            tmpResult['s3'] = $('#s3').selectpicker('val');
        });
        Panel.find('#search_now').off('click').click(function(e){
            e.stopPropagation();
            dirty = false;
            originalData = $.extend(true, {}, tmpResult);
            GridPanel.get_new(originalData);
        });
    }
}(SearchPanel || (SearchPanel = {})));