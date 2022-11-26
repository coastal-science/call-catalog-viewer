var SearchPanel = undefined;
(function (panel) {
    var Panel = undefined;
    var originalData = undefined;
    var tmpResult = undefined;
    var s_options = [
        {
            "s": "s1",
            "b": "b1",
            "option": [
                { "v": "SRKW", "text": "Southern Resident" },
                { "v": "NRKW", "text": "Northern Resident" },
                { "v": "T", "text": "Transient" },
            ]
        },
        {
            "s": "s2",
            "b": "b2",
            "option": [
                { "v": "J", "text": "J" }
            ]
        },
        {
            "s": "s3",
            "b": "b3",
            "option": [
                { "v": "J", "text": "J" },
                { "v": "K", "text": "K" },
                { "v": "L", "text": "L" },
            ]
        }
    ];
    var dirty = false;
    var s_index = 1;

    const LIBRARY = 'catalogs';
    const LIBRARY_INDEX = 'index.yaml';

    function pack_option(v, a) {
        return '<option value="' + v + '">' + a + '</option>'
    }

    function buildDropdowns() {
        s_options.forEach((value) => {
            Panel.find('#' + value.s).empty();
            var default_option = [];
            value.option.forEach((op_val) => {
                Panel.find('#' + value.s).append(pack_option(op_val.v, op_val.text));
                if (originalData[value.s].indexOf(op_val.v) >= 0) {
                    default_option.push(op_val.v);
                }
            });
            $('#' + value.s).selectpicker();
            $('#' + value.s).selectpicker('val', default_option);
        });
        bindEvents();
    }

    function updateOptions(originalData) {
         
    }

    function init() {
        originalData = {
            // s1: ["SRKW", "NRKW"],
            // s2: ["J"],
            // s3: ["J", "K", "L"],
        };
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        if (urlParams.has('f')) {
            const filter = urlParams.get('f');
            const obj = atob(filter); // this is the filters passed through the url
            console.log("OBJ: " + obj);
            if (obj !== undefined) {
                try {
                    const ev = eval('(' + obj + ')');
                    var keys = Object.keys(ev);
                    keys.forEach((item) => {
                        originalData[item] = ev[item];
                    });
                } catch (e) {

                }
            }
        }

        updateOptions(originalData);
        console.log("Original Data:" + originalData);

        tmpResult = $.extend(true, {}, originalData);
        Panel = $('.panel');

        s_options.forEach((value) => {
            console.log(value);
            Panel.find('#' + value.s).empty();
            var default_option = [];
            value.option.forEach((op_val) => {
                Panel.find('#' + value.s).append(pack_option(op_val.v, op_val.text));
                if (originalData[value.s].indexOf(op_val.v) >= 0) {
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
        $('#s1').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            tmpResult['s1'] = $('#s1').selectpicker('val');
        });
        $('#s2').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            tmpResult['s2'] = $('#s2').selectpicker('val');
        });
        $('#s3').on('changed.bs.select', (e, clickedIndex, isSelected, previousValue) => {
            tmpResult['s3'] = $('#s3').selectpicker('val');
        });
        Panel.find('#search_now').off('click').click(function (e) {
            dirty = false;
            originalData = $.extend(true, {}, tmpResult);
            GridPanel.get_new(originalData);
        });
    }
}(SearchPanel || (SearchPanel = {})));