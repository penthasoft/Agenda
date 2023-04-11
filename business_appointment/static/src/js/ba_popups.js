odoo.define('business_appointment.ba_popups', function (require) {
"use strict";

    const Notification = require('web.Notification');
    const session = require('web.session');
    const WebClient = require('web.WebClient');

    const BaPopUpNotification = Notification.extend({
        template: "BaPopUpNotification",
        init: function(parent, params) {
            this._super(parent, params);
            this.eid = params.eventID;
            this.sticky = true;
            this.alarmID = params.alarmID;
            this.partner = params.partner;
            this.service = params.service;
            this.resource = params.resource;     
            this.icon = "fa-calendar";       
            this.events = _.extend(this.events || {}, {
                'click .link2event': function() {
                    var self = this;
                    this._rpc({
                        model: "business.appointment",
                        method: "action_open_form_view",
                        args: [[self.eid], self.alarmID],
                    }).then(function (action) {
                        return self.do_action(action);
                    });
                },
                'click .link2recall': function() {
                    this.destroy(true);
                },
                'click .link2showed': function() {
                    var self = this;
                    this._rpc({
                        model: "alarm.task",
                        method: "action_mark_popup_done",
                        args: [[self.alarmID]],
                    }).then(this.destroy.bind(this), this.destroy.bind(this));
                },
            });
        },
    });

    WebClient.include({
        /**
         *  The method to process showing up poup notifications
        */
        display_ba_popup_notifications: function(notifications) {
            var self = this;
            var last_notif_timer = 0;
            // Clear previously set timeouts and destroy currently displayed calendar notifications
            clearTimeout(this.get_next_ba_popup_notif_timeout);
            _.each(this.ba_popup_notif_timeouts, clearTimeout);
            _.each(this.ba_popup_notif_timeouts, function (notificationID) {
                self.call('notification', 'close', notificationID, true);
            });
            this.ba_popup_notif_timeouts = {};

            _.each(notifications, function(notif) {
                var key = notif.event_id + ',' + notif.alarm_id;
                if (key in self.ba_popup_notif_notif) {
                    return;
                }
                self.ba_popup_notif_timeouts[key] = setTimeout(function() {
                    var notificationID = self.call('notification', 'notify', {
                        Notification: BaPopUpNotification,
                        title: notif.title,
                        message: notif.message,
                        eventID: notif.event_id,
                        alarmID: notif.alarm_id,
                        partner: notif.partner,
                        service: notif.service,
                        resource: notif.resource,
                        onClose: function () {
                            delete self.ba_popup_notif_notif[key];
                        },
                    });
                    self.ba_popup_notif_notif[key] = notificationID;
                }, notif.timer * 1000);
                last_notif_timer = Math.max(last_notif_timer, notif.timer);
            });
            if (last_notif_timer  > 0) {
                this.get_next_ba_popup_notif_timeout = setTimeout(this.get_next_ba_popup_notif.bind(this), last_notif_timer  * 1000);
            };
        },
        /**
         *  The method to retrieve all possible popup alarms by appointment
        */
        get_next_ba_popup_notif: function() {
            session.rpc("/business/appointment/popup/notify", {}, {shadow: true})
                .then(this.display_ba_popup_notifications.bind(this))
                .guardedCatch(function(reason) { //
                    var err = reason.message;
                    var ev = reason.event;
                    if(err.code === -32098) {
                        ev.preventDefault();
                    }
                });
        },
        /**
         *  An event is triggered on the bus each time alarm.task is created or modified
        */
        show_application: function() {
            this.ba_popup_notif_timeouts = {};
            this.ba_popup_notif_notif = {};
            this.call('bus_service', 'onNotification', this, function (notifications) {
                _.each(notifications, (function (notification) {
                    if (notification[0][1] === 'alarm.task') {
                        this.display_ba_popup_notifications(notification[1]);
                    }
                }).bind(this));
            });
            return this._super.apply(this, arguments).then(this.get_next_ba_popup_notif.bind(this));
        },
    });    

});
