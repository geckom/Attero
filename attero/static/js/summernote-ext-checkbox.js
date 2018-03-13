(function (factory) {
    /* global define */
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else if (typeof module === 'object' && module.exports) {
        // Node/CommonJS
        module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        factory(window.jQuery);
    }
}(function ($) {
    // Extends plugins for adding Checkbox.
    $.extend($.summernote.plugins, {
        /**
         * @param {Object} context - context object has status of editor.
         */
        'checkbox': function (context) {
            var self = this;
            var ui = $.summernote.ui;

            context.memo('button.checkbox', function () {
                var button = ui.button({
                    contents: '<i class="glyphicon glyphicon-check"/>',
                    tooltip: 'Checkbox',
                    click: function () {
                        context.invoke('insertNode', self.createCheckbox());
                    }
                });

                return button.render();
            });

            this.createCheckbox = function () {
                // IE workaround: input type must be included within non-contenteditable section, otherwise click event will not trigger.
                var container = document.createElement('span');
                $(container).attr('contenteditable', false);
                var elem = document.createElement('input');
                elem.type = "checkbox";

                $(elem).appendTo($(container));
                return container;
            }

            // These events will be attached when editor is initialized.
            this.events = {
                'summernote.init': function (we, e) {                    
                },
                'summernote.keyup': function (we, e) {                    
                }
            };

            this.initialize = function () {
                var layoutInfo = context.layoutInfo;
                var $editor = layoutInfo.editor;

                $editor.on('click', function (event) {
                    if (event.target.type && event.target.type == 'checkbox') {                        
                        var checked = $(event.target).is(':checked');
                        $(event.target).attr('checked', checked);
                        context.invoke('insertText', '');
                    }
                });
            };

            this.destroy = function () {

            };
        }
    });
}));
