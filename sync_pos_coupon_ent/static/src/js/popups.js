odoo.define('sync_pos_coupon_ent.popups', function (require) {
"use strict";

    const { useState, useSubEnv } = owl.hooks;
    const { useListener } = require('web.custom_hooks');
    const PosComponent = require('point_of_sale.PosComponent');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');
    const core = require('web.core');
    const _t = core._t;

    class CouponApplyPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.value = this.props.value || '';
        }
        getPayload() {
            var value = $(this.el).find('input').val();
            return value;
        }
    }
    CouponApplyPopup.template = 'CouponApplyPopup';
    Registries.Component.add(CouponApplyPopup);

});
