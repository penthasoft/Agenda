odoo.define('sitrad.dashboard', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var SitradDashboard = AbstractAction.extend({
        template: 'sitrad_dashboard_template',

        events: {
            'click button[data-action="project_action_dashboard"]': '_onProjectDashboardClick',
            'click button[data-action="sitrad_report_action"]': '_onSitradReportClick',
            'click button[data-action="sitrad_reportcem_action"]': '_onSitradReportCemClick',
            'click button[data-action="sitrad_reportvic_action"]': '_onSitradReportVicClick',
            'click button[data-action="sitrad_reportagre_action"]': '_onSitradReportAgreClick',
        },

        start: function() {
            var self = this;
            return this._super().then(function() {
                self.renderElement();
            });
        },

        _onProjectDashboardClick: function(ev) {
            ev.preventDefault();
            this.do_action('project_action_dashboard');
        },

        _onSitradReportClick: function(ev) {
            ev.preventDefault();
            this.do_action('sitrad_report_action');
        },

        _onSitradReportCemClick: function(ev) {
            ev.preventDefault();
            this.do_action('sitrad_reportcem_action');
        },

        _onSitradReportVicClick: function(ev) {
            ev.preventDefault();
            this.do_action('sitrad_reportvic_action');
        },

        _onSitradReportAgreClick: function(ev) {
            ev.preventDefault();
            this.do_action('sitrad_reportagre_action');
        },
    });

    core.action_registry.add('sitrad_dashboard', SitradDashboard);

    return SitradDashboard;
});
