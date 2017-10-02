/*!
 * lcextractor.js
 *
 * Copyright (c) Damien Churchill 2010 <damoxc@gmail.com>
 *
 * This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
 * the additional special exception to link portions of this program with the OpenSSL library.
 * See LICENSE for more details.
 *
 */

Ext.ns('Deluge.ux.preferences');

/**
 * @class Deluge.ux.preferences.LCExtractorPage
 * @extends Ext.Panel
 */
Deluge.ux.preferences.LCExtractorPage = Ext.extend(Ext.Panel, {

    title: _('LCExtractor'),
    layout: 'fit',
    border: false,
    configLoaded: false,

    initComponent: function() {
        Deluge.ux.preferences.LCExtractorPage.superclass.initComponent.call(this);

        this.form = this.add({
            xtype: 'form',
            layout: 'form',
            border: false,
            autoHeight: true
        });

        fieldset = this.form.add({
            xtype: 'fieldset',
            border: false,
            title: '',
            autoHeight: true,
            labelAlign: 'top',
            labelWidth: 80,
            defaultType: 'textfield'
        });

        this.extract_path = fieldset.add({
            fieldLabel: _('Extract to:'),
            labelSeparator : '',
            name: 'extract_path',
            width: '97%'
        });


        this.use_name_folder = fieldset.add({
            xtype: 'checkbox',
            name: 'use_name_folder',
            height: 22,
            hideLabel: true,
            boxLabel: _('Create torrent name sub-folder')
        });

        this.in_place_extraction = fieldset.add({
            xtype: 'checkbox',
            name: 'in_place_extraction',
            height: 22,
            hideLabel: true,
            boxLabel: _('Extract torrent in-place')
        });

        this.sonarr_radarr_support = fieldset.add({
            xtype: 'checkbox',
            name: 'sonarr_radarr_support',
            height: 22,
            hideLabel: true,
            boxLabel: _('Enable support for Sonarr and Radarr')
        });

        this.on('show', this.updateConfig, this);
    },

    onApply: function() {
        // Only apply the settings if we've previously loaded them (or else we end up resetting the config!).
        if (this.configLoaded) {
          // build settings object
          var config = { }

          config['extract_path'] = this.extract_path.getValue();
          config['use_name_folder'] = this.use_name_folder.getValue();
          config['in_place_extraction'] = this.in_place_extraction.getValue();
          config['sonarr_radarr_support'] = this.sonarr_radarr_support.getValue();

          deluge.client.lcextractor.set_config(config);
        }
    },

    onOk: function() {
        this.onApply();
    },

    updateConfig: function() {
        deluge.client.lcextractor.get_config({
            success: function(config) {
                this.extract_path.setValue(config['extract_path']);
                this.use_name_folder.setValue(config['use_name_folder']);
                this.in_place_extraction.setValue(config['in_place_extraction']);
                this.sonarr_radarr_support.setValue(config['sonarr_radarr_support']);
                this.configLoaded = true;
            },
            scope: this
        });
    }
});


Deluge.plugins.LCExtractorPlugin = Ext.extend(Deluge.Plugin, {

    name: 'LCExtractor',

    onDisable: function() {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function() {
        this.prefsPage = deluge.preferences.addPage(new Deluge.ux.preferences.LCExtractorPage());
    }
});
Deluge.registerPlugin('LCExtractor', Deluge.plugins.LCExtractorPlugin);
