odoo.define('sync_pos_coupon_ent.ReceiptScreen', function (require) {
    "use strict";

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const PosReceiptScreen = (ReceiptScreen) =>
        class extends ReceiptScreen {
            mounted() {
                setTimeout(async () => await this.handleAutoPrint(), 500);
            }
        }
    Registries.Component.extend(ReceiptScreen, PosReceiptScreen);

    return ReceiptScreen;
});
