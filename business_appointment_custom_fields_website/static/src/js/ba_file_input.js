odoo.define('business_appointment_custom_fields_website.ba_file_input.js', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.baBinaryOnFocus = publicWidget.Widget.extend({
        selector: '.ba_custom_fields_portal',
        events: {'focus .ba_binary_input': '_onShowFile',},
        _onShowFile: function (event) {
            if (event.currentTarget.type != "file") {
                event.preventDefault();
                event.stopPropagation(); 
                event.currentTarget.type = "file";
            };
        },
    });

});