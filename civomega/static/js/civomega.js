/*!
 * civomega jQuery plugin
 */

;(function ( $, window, document, undefined ) {

    // Define plugin defaults
    var pluginName = "civomega",
        defaults = {
            patternUrl: "",    // URL to page which will return matching patterns
            typeUrl: "",       // URL to page which will return entity types
            entityUrl: "",     // URL to page which will return matching entities
            answerUrl: "",     // URL to page which will take a question and return answers
            styleUrl: "",      // URL to dynamic css file
            submitUrl: "",     // URL to submit the file
        };

    // The actual plugin constructor
    function Plugin( element, options ) {
        var self = this;
        self.element = element;
        self.options = $.extend( {}, defaults, options) ;

        self._defaults = defaults;
        self._name = pluginName;

        self.typeCache = null;
        self.patternCache = null;
        self.entityCache = null;

        self.lastLetter = 0;           // Used if you need keydown events but also need the character inputted

        self.lockedPattern = null;  // The pattern that is actively being completed
        self.loadedResults = []; // Do we have loaded results
        self.activeEntity = -1;   // The the ID of the pattern's entity that we want to focus on next
        self.patternSegments = [];  // The pieces of the pattern associated with this question
        self.entityValues = [];     // The values we have collected so far

        self.activeAjax = null;
        self.highlightedIndex = -1;
        self.cursorIndex = -1;

        self.refocus = false;   // Set to true whenever we want to change the active focus based on an event or set of rules

        self.init();
    }

    Plugin.prototype = {

        init: function() {
            var self = this;
            var $el = $(this.element)
                .addClass("civomega");

            self.$el = $el;

            // Add interface elements
            self.interface = [];
            self.interface.questionSegments = [];

            // The form container
            var $form = $("<div>")
                .addClass("civomega-form")
                .appendTo($el);

            // The question container
            var $question = $("<div>")
                .addClass("civomega-question")
                .appendTo($form);
            self.interface.$question = $question;

            // The submit button
            var $submitButton = $("<input>")
                .addClass("btn")
                .addClass("civomega-submit")
                .attr("type","submit")
                .val("Ask!")
                .click(function(e) {
                    self.submit();
                })
                .appendTo($form);
            self.interface.$submitButton = $submitButton;

            // The segment container
            var $questionSegments = $("<div>")
                .addClass("civomega-question-segments")
                .hide()
                .appendTo($question);
            self.interface.$questionSegments = $questionSegments;

            // The actual input for the question
            var $questionInputBase = $("<input>")
                .attr("type","text")
                .addClass("civomega-question-input")
                .addClass("civomega-question-base")
                .keydown(function(e) {
                    return self.processKeydown(e);
                })
                .keyup(function(e) {
                    return self.processKeyup(e);
                })
                .appendTo($question);
            self.interface.$questionInputBase = $questionInputBase;

            // The visual indicator for ajax requests (e.g. spinny wheel)
            var $ajaxStatus = $("<div>")
                .addClass("civomega-ajax-status")
                .hide()
                .appendTo($form);
            self.interface.$ajaxStatus = $ajaxStatus;

            // The list of patterns returned from the server
            var $patternList = $("<ul>")
                .addClass("civomega-patternlist")
                .hide()
                .appendTo($form);
            self.interface.$patternList = $patternList;

            // The list of entities returned from the server
            var $entityList = $("<ul>")
                .addClass("civomega-entitylist")
                .hide()
                .appendTo($form);
            self.interface.$entityList = $entityList;

            // The results pane
            var $results = $("<div>")
                .addClass("civomega-results")
                .hide()
                .appendTo($el);
            self.interface.$results = $results;

            // Load in our registered entity types
            self.activeAjax = $.ajax({
                method: "GET",
                url: self.options.typeUrl,
                dataType: "json",
            })
            .done(function( data ) {
                self.typeCache = data.types;
                self.redraw();
            });

            // Load in our dynamic css
            $('head').append('<link rel="stylesheet" href="' + self.options.styleUrl + '" type="text/css" />');
        },

        processKeydown: function(e) {
            var self = this;

            // Convert the keypress to the appropriate letter
            self.lastLetter = String.fromCharCode(e.keyCode);
            self.lastLetter = e.shiftKey?self.lastLetter:self.lastLetter.toLowerCase();
            self.lastLetter = (self.lastLetter.match(/[a-zA-Z.,?0-9]/)?self.lastLetter:"");
            if(e.keyCode == 32) self.lastLetter = " "; // "space" is the only whitespace we care about

            // Wipe out any results (the user just changed them)
            self.loadedResults = [];

            switch(e.keyCode) {
                case 8: // delete
                    // If we are in the pattern list, delete unhighlights the currently highlighted pattern
                    if(self.isPatternList()) {
                        self.highlightedIndex = -1;
                        self.redraw();
                    } else {
                        if(getCursorPosition() == 0) {
                            if (self.activeEntity == 0) {
                                self.cancelPattern();
                                self.redraw();
                                return false;
                            }
                            else {
                                self.previousEntity();
                                self.redraw();
                                return false;
                            }
                        } else {
                            self.redraw();
                            setTimeout(function() {
                                self.redraw();
                            }, 0);
                        }
                    }
                    break;

                case 13: // enter
                    // If we are in the pattern list, enter locks the currently highlighted pattern
                    if(self.isPatternList() && self.highlightedIndex != -1) {
                        self.lockPattern(self.patternCache[self.highlightedIndex]);
                        self.redraw();
                        return false;
                    }

                    if(self.isPatternLocked()) {
                        if(self.isLastEntity()) {
                            self.submit();
                        }
                        else {
                            self.nextEntity();
                            self.redraw();
                            return false;
                        }
                    }

                    break;

                case 27: // escape

                    // If we are in the pattern list, escape unhighlights the currently highlighted pattern
                    if(self.isPatternList()) {
                        self.highlightedIndex = -1;
                        self.redraw();
                        return false;
                    } else {
                        self.cancelPattern()
                    }
                    break;

                case 37: // left

                    // If we are in the pattern list, left unhighlights the currently highlighted pattern
                    // If we are in the entity entry, and the cursor is at the front, left moves to the previous entry
                    if(self.isPatternList() && self.highlightedIndex != -1) {
                        self.highlightedIndex = -1;
                        self.redraw();
                        return false;
                    } else if(self.isPatternLocked()) {
                        var cursor = getCursorPosition();
                        var entities = self.interface.$questionSegments.find("input");
                        var $entity = $(entities[self.activeEntity]);
                        if(cursor == 0) {
                            // Move to the previous entity
                            self.previousEntity();
                            self.redraw();
                            return false;
                        }
                    } else {
                        self.redraw();
                    }
                    break;

                case 38: // up
                    if(self.isPatternList()) {
                        self.highlightedIndex--;
                        self.highlightedIndex = Math.max(self.highlightedIndex, -1);
                        self.redraw();
                        return false;
                    }
                    break;

                case 39: // right
                    // If we are in the pattern list, right locks the currently highlighted pattern
                    // If we are in the entity entry, and the cursor is at the end of an entity, right moves to the next entry
                    if(self.isPatternList() && self.highlightedIndex != -1) {
                        self.lockPattern(self.patternCache[self.highlightedIndex]);
                        self.redraw();
                        return false;
                    } else if(self.isPatternLocked()) {
                        var cursor = getCursorPosition();
                        var entities = self.interface.$questionSegments.find("input");
                        var $entity = $(entities[self.activeEntity]);
                        if(cursor == $entity.val().length) {
                            // Move to the next entity
                            self.nextEntity();
                            self.redraw();
                            return false;
                         }
                    } else {
                        self.redraw();
                    }
                    break;

                case 40: // down
                    if(self.isPatternList()) {
                        self.highlightedIndex++;
                        self.highlightedIndex = Math.min(self.highlightedIndex, self.patternCache.length - 1);
                        self.redraw();
                        return false;
                    }
                    break;
                default:
                    if(self.isPatternLocked())
                        self.redraw();
                    break;
            }
        },

        processKeyup: function(e) {
            var self = this;
            self.lastLetter = "";
            switch(e.keyCode) {
                case 8: // delete
                    break;
                case 13: // enter
                    break;
                case 27: // escape
                    break;
                case 37: // left
                    break;
                case 38: // up
                    break;
                case 39: // right
                    break;
                case 40: // down
                    break;
                default:
                    if(!self.isPatternLocked())
                        self.refreshPatterns();
                    if(self.isPatternLocked())
                        self.redraw();
                    break;
            }
        },

        refreshPatterns: function() {
            var self = this;
            var text = self.interface.$questionInputBase.val();

            if(text == "") {
                self.patternCache = null;
                self.redraw();
            } else {
                // Look up any matching patterns
                self.activeAjax = $.ajax({
                    method: "GET",
                    url: self.options.patternUrl,
                    dataType: "json",
                    data: {
                        q: text
                    }
                })
                .done(function( data ) {
                    // If there used to be a match, but there isn't any longer...
                    if(data.matches.length == 0 && self.isPatternSelected()) {
                        var pattern = self.patternCache[self.highlightedIndex];
                        var currentText = self.interface.$questionInputBase.val();
                        var patternStem = pattern.pattern.replace(/\{.*/, "");
                        var firstText = currentText.substring(patternStem.length);
                        self.lockPattern(pattern);
                        $(self.interface.$questionSegments.find("input")[0]).val(firstText);
                    } else {
                        if(data.matches.length == 0)
                            self.patternCache = [];
                        else
                            self.patternCache = data.matches;
                        self.activeAjax = null;
                        self.redraw();
                    }

                    // Update (or reset) selected match
                    if(data.matches.length == 0)
                        self.highlightedIndex = -1;
                    else if (!self.isPatternSelected())
                        self.highlightedIndex = 0;

                })
                self.redraw();
            }
        },

        lockPattern: function(pattern) {
            // Select this pattern as the one we want to use
            var self = this;
            self.lockedPattern = pattern;

            // Figure out what buckets we want to populate
            self.patternSegments = self.parsePattern(pattern);

            // Clear out the old forms
            self.interface.$questionSegments.children().remove();


            // Create inputs for each entity
            var totalWidth = 0;
            for(var x in self.patternSegments) {
                var segment = self.patternSegments[x];
                if(segment.type == "text") {
                    var $segmentElement = $("<div>")
                        .addClass("civomega-question-segment")
                        .addClass("civomega-question-segment-text")
                        .text(segment.value)
                        .appendTo(self.interface.$questionSegments);
                    self.interface.questionSegments[x] = $segmentElement;
                } else {
                    var $segmentElement = $("<div>")
                        .addClass("civomega-question-segment")
                        .addClass("civomega-question-segment-input")
                        .addClass("civomega-entity-" + segment.value.code)
                        .appendTo(self.interface.$questionSegments);

                    var $segmentElementQuestion = $("<input>")
                        .attr("type","text")
                        .addClass("civomega-question-input")
                        .keydown(function(e) {
                            return self.processKeydown(e);
                        })
                        .keyup(function(e) {
                            return self.processKeyup(e);
                        })
                        .appendTo($segmentElement);

                    var $segmentElementLabel = $("<label>")
                        .addClass("civomega-question-label")
                        .text(segment.value.display_name)
                        .appendTo($segmentElement);
                    self.interface.questionSegments[x] = $segmentElement;
                }
                self.interface.$questionSegments.width(totalWidth);
            }
            self.activeEntity = 0;
            self.refocus = true;
        },

        submit: function() {
            var self = this;
            if(self.isPatternLocked()) {
                var pattern = self.lockedPattern;
                var entities = self.interface.$questionSegments.find("input");
                var values = [];
                $(entities).each(function(i, entity) {
                    values.push($(entity).val());
                });

                $.ajax({
                    method: "GET",
                    url: self.options.submitUrl,
                    dataType: "json",
                    data: {
                        id: self.lockedPattern.id,
                        args: values
                    }
                })
                .done(function( data ) {
                    self.loadedResults = [data];
                    self.redraw();
                })
                .error(function() {
                    self.loadedResults = ["Something went wrong."];
                    self.redraw();
                });
            }
        },

        cancelPattern: function() {
            // Undo the current pattern
            var self = this;
            self.lockedPattern = null;
        },

        nextEntity: function() {
            var self = this;
            var entities = self.interface.$questionSegments.find("input");
            self.activeEntity = Math.min(entities.length - 1, self.activeEntity + 1);
            self.refocus = true;
        },

        previousEntity: function() {
            var self = this;
            self.activeEntity = Math.max(0, self.activeEntity - 1);
            self.refocus = true;
        },

        activateEntity: function(entity) {
            var self = this;
        },

        cancelEntity: function() {
            var self = this;
        },

        completeEntity: function() {
            var self = this;
        },

        editEntity: function(index) {
            var self = this;
        },

        isLastEntity: function() {
            // Returns true if the user is entering data in the last item on the list
            var self = this;
            var entities = self.interface.$questionSegments.find("input");
            return self.isPatternLocked() && (self.activeEntity == entities.length - 1);
        },

        isPatternSelected: function() {
            // Returns true if the user has highlighted a pattern from the list
            var self = this;
            return self.highlightedIndex != -1;
        },

        isPatternList: function() {
            // Returns true if the user has a pattern cache but hasn't picked a pattern
            var self = this;
            return !self.isPatternLocked() && self.patternCache != null;
        },

        isActiveAjax: function() {
            // Returns true if there is an active ajax call
            var self = this;
            return self.activeAjax != null;
        },

        isPatternLocked: function() {
            // Returns true if the user has locked in a pattern
            var self = this;
            return self.lockedPattern != null;
        },

        isEntityList: function() {
            // Returns true if the user has a pattern cache but hasn't picked a pattern
            var self = this;
            return self.isEntityInput() && self.entityCache != null;
        },
        isEntityInput: function() {
            // Returns true if the user is currently entering an entity
            var self = this;
            return self.activeEntity != -1;
        },
        isLoadedResults: function() {
            // Returns true if there are loaded results
            var self = this;
            return self.loadedResults.length > 0;
        },

        renderPattern: function(pattern) {
            // Takes a pattern string and returns an HTML string
            var self = this;
            var patternText = pattern.pattern;
            var breakdown = patternText.split(/(\{[^\}]*\})/);
            var html = "";
            for(var x in breakdown) {
                var item = breakdown[x];
                if(item.match(/^\{[^\}]*\}$/)) {
                    // This is an entity
                    var typeCode = item.substring(1,item.length-1);

                    var type = {
                        "display_name": typeCode.replace("_"," "),
                        "validation": "/(.)*/",
                        "description": ""
                    }
                    if(typeCode in self.typeCache)
                        var type = self.typeCache[typeCode];
                    
                    html += "<div class='civomega-entity-" + type.code + " civomega-entity'>" + type.display_name +"</div>";

                } else {
                    // This is just text
                    html += item;
                }
            }
            return html;
        },

        parsePattern: function(pattern) {
            // Takes a pattern string and returns a segment array
            var self = this;
            var patternText = pattern.pattern;
            var breakdown = patternText.split(/(\{[^\}]*\})/);
            var segments = [];
            for(var x in breakdown) {
                var item = breakdown[x];
                if(item.match(/^\{[^\}]*\}$/)) {
                    // This is an entity
                    var typeCode = item.substring(1,item.length-1);

                    var type = {
                        code: typeCode,
                        display_name: typeCode.replace("_"," "),
                        validation: "/(.)*/",
                        description: ""
                    }
                    if(typeCode in self.typeCache)
                        var type = self.typeCache[typeCode];
                    
                    segments.push({
                        type: "entity",
                        value: type
                    });
                } else {
                    // This is just text
                    segments.push({
                        type: "text",
                        value: item
                    });
                    continue;
                }
            }
            return segments;
        },

        redraw: function() {
            var self = this;

            // Should we render the AJAX loader?
            if(self.isActiveAjax()) {
                self.interface.$ajaxStatus.show();
            } else {
                self.interface.$ajaxStatus.hide();
            }

            // Should we render the pattern autocomplete?
            if(self.isPatternList()) {
                self.redrawPatterns();
                self.interface.$patternList.slideDown(200);
            } else {
                self.interface.$patternList.slideUp(200);
            }

            // Should we render the entity autocomplete?
            if(self.isEntityList()) {
                self.redrawEntities();
                self.interface.$entityList.slideDown(200);
            } else {
                self.interface.$entityList.slideUp(200);
            }


            // Should we render the results?
            if(self.isLoadedResults()) {
                self.interface.$results.html("");
                for(var x in self.loadedResults) {
                    var result = self.loadedResults[x];
                    
                    var $result = $("<div />")
                        .addClass("civomega-result")
                        .appendTo(self.interface.$results);
 
                    var $title = $("<div />")
                        .addClass("civomega-result-title")
                        .html("")
                        .appendTo($result);

                    var $content = $("<div />")
                        .addClass("civomega-result-content")
                        .html(result.html)
                        .appendTo($result);
                }
                self.interface.$results.slideDown(200);
            } else {
                self.interface.$results.slideUp(200);
                self.interface.$results.html("");
            }

            // Should we replace the current text?
            if(self.isPatternLocked()) {
                self.interface.$questionInputBase.hide();
                self.interface.$questionSegments.show();
                self.redrawQuestion();
            } else {
                self.interface.$questionSegments.hide();
                self.interface.$questionInputBase.show();
                self.interface.$questionInputBase.focus();
            }

            // Add appropriate classes to reflect state
            if(self.isPatternList()) {
                self.$el.addClass("patternList");
            } else {
                self.$el.removeClass("patternList");
            }
        },

        redrawQuestion: function() {
            var self = this;
            if(self.isPatternLocked()) {
                // Set the input field widths to match their content
                self.interface.$questionSegments.find("input").each( function(index){
                    var $this = $(this);
                    var contentWidth = getContentWidth(this, $this.val() + ($this.is(":focus")?self.lastLetter:"")) + 2;
                    $this.width(contentWidth);
                    if(index == self.activeEntity && self.refocus) {
                        self.refocus = false;
                        $this.focus();
                    }
                });

                // Set the segment container field width to match the content
                var totalWidth = 5;
                self.interface.$questionSegments.children().each( function() {
                    totalWidth += $(this).outerWidth();
                });
                self.interface.$questionSegments.width( totalWidth);
                
                // Ensure that the cursor is never further than "centered"
                var cursorPosition = getCursorPosition() + 1; // This is called before the cursor is updated
                var text = $(document.activeElement).val() + self.lastLetter;
                var cursorLeftOffset = getContentWidth(document.activeElement, text.substring(0, cursorPosition)) + $(document.activeElement).position().left;

                // Position the cursor relative to the parent
                var centered = cursorLeftOffset - self.interface.$question.width() / 2;

                position = Math.min(self.interface.$questionSegments.width() - self.interface.$question.width(), centered); // Don't have the right appear before the right
                position = Math.max(0, position); // Dont have the left appear after the left
                self.interface.$questionSegments.css("left", -position);
            } else {
            }
        },

        redrawPatterns: function() {
            // We want to re-render the pattern list
            var self = this;

            self.interface.$patternList.empty();

            // Are there matching patterns?
            if(self.patternCache.length == 0 ) {
                var $li = $("<li>")
                    .html("Sorry, please try another question.")
                    .appendTo(self.interface.$patternList);
            }
            else {
                for(var x in self.patternCache) {
                    var pattern = self.patternCache[x];

                    var $li = $("<li>")
                        .html(self.renderPattern(pattern))
                        .data("civomega-pattern", pattern)
                        .click(function() {
                            // The user wants to lock into this question
                            self.lockPattern($(this).data("civomega-pattern"));
                            self.redraw();
                        })
                        .mouseenter(function() {
                            // If the mouse entered an unihlighted item, highlight it
                            var index = $(this).index();
                            if(self.highlightedIndex != index) {
                                self.highlightedIndex = index;
                                self.redraw();
                            }
                        })
                        .appendTo(self.interface.$patternList);
                    if(x == self.highlightedIndex)
                        $li.addClass("active");
                }
            }
        },

        redrawEntities: function() {
            // We want to re-render the entity list
            var self = this;
        }
    };

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName,
                new Plugin( this, options ));
            }
        });
    };


    // Helper Methods
    function getCursorPosition() {
        var input = document.activeElement;
        if ('selectionStart' in input) {
            // Standard-compliant browsers
            return input.selectionStart;
        } else if (document.selection) {
            // IE
            input.focus();
            var sel = document.selection.createRange();
            var selLen = document.selection.createRange().text.length;
            sel.moveStart('character', -input.value.length);
            return sel.text.length - selLen;
        }
    }
    function getContentWidth(element, text) {
        var $element = $(element);
        var width = 0;
        var $temp = $("<span>")
            .css("font-size", $element.css("font-size"))
            .css("font-weight", $element.css("font-weight"))
            .css("font-family", $element.css("font-family"))
            .css("white-space", "pre")
            .html(text)
            .insertBefore($element);
        width = $temp.width();
        $temp.remove();
        return width;
    }

})( jQuery, window, document );
