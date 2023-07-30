odoo.define('sync_pos_coupon_ent.CouponPosButton', function (require) {
"use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const core = require('web.core');
    const _t = core._t;

    class UpdatePromotionsButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            var order = this.env.pos.get_order();
            if (order) {
                order.updatePromotions();
            }
        }
    }
    UpdatePromotionsButton.template = 'UpdatePromotions';

    ProductScreen.addControlButton({
        component: UpdatePromotionsButton,
        condition: function() {
            return this.env.pos.config.iface_order_coupon;
        },
    });

    Registries.Component.add(UpdatePromotionsButton);

    class OrderCouponButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            var order = this.env.pos.get_order();
            if (order) {
                const { confirmed, payload } = await this.showPopup('CouponApplyPopup', {
                    title: _t('Apply Coupon'),
                    value: order.get_coupon(),
                });
                if (confirmed) {
                    if(payload) {
                        order.processCoupon(payload);
                    } else {
                        return ;
                    }
                } else {
                    return ;
                }
            }
        }
    }
    OrderCouponButton.template = 'OrderCouponButton';

    ProductScreen.addControlButton({
        component: OrderCouponButton,
        condition: function() {
            return this.env.pos.config.iface_order_coupon;
        },
    });

    Registries.Component.add(OrderCouponButton);

    return [UpdatePromotionsButton, OrderCouponButton];
});
