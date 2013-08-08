/*
 * Treeview 1.4 - jQuery plugin to hide and show branches of a tree
 * 
 * http://bassistance.de/jquery-plugins/jquery-plugin-treeview/
 * http://docs.jquery.com/Plugins/Treeview
 *
 * Copyright (c) 2007 JÃ¶rn Zaefferer
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Revision: $Id: jquery.treeview.js 4684 2008-02-07 19:08:06Z joern.zaefferer $
 *
 */

;(function($) {

    $.extend($.fn, {
        swapClass: function(c1, c2) {
            var c1Elements = this.filter('.' + c1);
            this.filter('.' + c2).removeClass(c2).addClass(c1);
            c1Elements.removeClass(c1).addClass(c2);
            return this;
        },
        replaceClass: function(c1, c2) {
            return this.filter('.' + c1).removeClass(c1).addClass(c2).end();
        },
        hoverClass: function(className) {
            className = className || "hover";
            return this.hover(function() {
                $(this).addClass(className);
            }, function() {
                $(this).removeClass(className);
            });
        },
        heightToggle: function(animated, callback) {
            animated ?
                this.animate({ height: "toggle" }, animated, callback) :
                this.each(function(){
                    jQuery(this)[ jQuery(this).is(":hidden") ? "show" : "hide" ]();
                    if(callback)
                        callback.apply(this, arguments);
                });
        },
        heightHide: function(animated, callback) {
            if (animated) {
                this.animate({ height: "hide" }, animated, callback);
            } else {
                this.hide();
                if (callback)
                    this.each(callback);                
            }
        },
        prepareBranches: function(settings) {
            if (!settings.prerendered) {
                // collapse whole tree, or only those marked as closed, anyway except those marked as open
                this.filter((settings.collapsed ? "" : "." + CLASSES.closed) + ":not(." + CLASSES.open + ")").find(">ul").hide();
            }
            // return all items with sublists
            return this.filter(":has(>ul)");
        },
        applyClasses: function(settings, toggler) {
            this.filter(":has(>ul):not(:has(>a))").find(">span").click(function(event) {
                toggler.apply($(this).next());
            }).add( $("a", this) ).hoverClass();
            
            if (!settings.prerendered) {
                // handle closed ones first
                this.filter(":has(>ul:hidden)")
                        .addClass(CLASSES.expandable)
                        
                // handle open ones
                this.not(":has(>ul:hidden)")
                        .addClass(CLASSES.collapsable)
            }
        },
        treeview: function(settings) {
            
            settings = $.extend({
                cookieId: "treeview"
            }, settings);
            
            if (settings.add) {
                return this.trigger("add", [settings.add]);
            }
            
            if ( settings.toggle ) {
                var callback = settings.toggle;
                settings.toggle = function() {
                    return callback.apply($(this).parent()[0], arguments);
                };
            }
        
            // factory for treecontroller
            function treeController(tree, control) {
                // factory for click handlers
                function handler(filter) {
                    return function() {
                        // reuse toggle event handler, applying the elements to toggle
                        return false;
                    };
                }
                // click on first element to collapse tree
                $("a:eq(0)", control).click( handler(CLASSES.collapsable) );
                // click on second to expand tree
                $("a:eq(1)", control).click( handler(CLASSES.expandable) );
                // click on third to toggle tree
                $("a:eq(2)", control).click( handler() ); 
            }
        
            // handle toggle event
            function toggler() {
                $(this)
                    .parent()
                    // swap classes for parent li
                    .swapClass( CLASSES.collapsable, CLASSES.expandable )
                    // find child lists
                    .find( ">ul" )
                    // toggle them
                    .heightToggle( settings.animated, settings.toggle );
                if ( settings.unique ) {
                    $(this).parent()
                        .siblings()
                        .replaceClass( CLASSES.collapsable, CLASSES.expandable )
                        .find( ">ul" )
                        .heightHide( settings.animated, settings.toggle );
                }
            }
            
            function serialize() {
                function binary(arg) {
                    return arg ? 1 : 0;
                }
                var data = [];
                branches.each(function(i, e) {
                    data[i] = $(e).is(":has(>ul:visible)") ? 1 : 0;
                });
                $.cookie(settings.cookieId, data.join("") );
            }
            
            function deserialize() {
                var stored = $.cookie(settings.cookieId);
                if ( stored ) {
                    var data = stored.split("");
                    branches.each(function(i, e) {
                        $(e).find(">ul")[ parseInt(data[i]) ? "show" : "hide" ]();
                    });
                }
            }
            
            // add treeview class to activate styles
            this.addClass("treeview");
            
            // prepare branches and find all tree items with child lists
            var branches = this.find("li").prepareBranches(settings);
            
            switch(settings.persist) {
            case "cookie":
                var toggleCallback = settings.toggle;
                settings.toggle = function() {
                    serialize();
                    if (toggleCallback) {
                        toggleCallback.apply(this, arguments);
                    }
                };
                deserialize();
                break;
            case "location":
                var current = this.find("a").filter(function() { return this.href.toLowerCase() == location.href.toLowerCase(); });
                if ( current.length ) {
                    current.addClass("selected").parents("ul, li").add( current.next() ).show();
                }
                break;
            }
            
            branches.applyClasses(settings, toggler);
                
            // if control option is set, create the treecontroller and show it
            if ( settings.control ) {
                treeController(this, settings.control);
                $(settings.control).show();
            }
            
            return this.bind("add", function(event, branches) {
                $(branches).find("li").andSelf().prepareBranches(settings).applyClasses(settings, toggler);
            });
        }
    });
    
    // classes used by the plugin
    // need to be styled via external stylesheet, see first example
    var CLASSES = $.fn.treeview.classes = {
        open: "open",
        closed: "closed",
        expandable: "expandable",
        expandableHitarea: "expandable-hitarea",
        lastExpandableHitarea: "lastExpandable-hitarea",
        collapsable: "collapsable",
        collapsableHitarea: "collapsable-hitarea",
        lastCollapsableHitarea: "lastCollapsable-hitarea",
        lastCollapsable: "lastCollapsable",
        lastExpandable: "lastExpandable",
        last: "last",
        hitarea: "hitarea"
    };
    
    // provide backwards compability
    $.fn.Treeview = $.fn.treeview;
    
})(jQuery);
