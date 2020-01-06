/********************************************************************************
 *                                                                               *
 * black-widow.js -- Main black-widow javascript                                 *
 *                                                                               *
 ********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
 *                                                                               *
 * This file is part of black-widow.                                             *
 *                                                                               *
 * black-widow is free software: you can redistribute it and/or modify           *
 * it under the terms of the GNU General Public License as published by          *
 * the Free Software Foundation, either version 3 of the License, or             *
 * (at your option) any later version.                                           *
 *                                                                               *
 * black-widow is distributed in the hope that it will be useful,                *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of                *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
 * GNU General Public License for more details.                                  *
 *                                                                               *
 * You should have received a copy of the GNU General Public License             *
 * along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
 *                                                                               *
 ********************************************************************************/

$(function() {
    $('button.upload').click(function() {
        const $label = $(this).parent();
        $label.click();
    });
    $('input.submit').change(function() {
        const $this = $(this);
        const $form = $this.closest('form');
        if ($this.hasClass('force')) {
            $form.find('input:required').prop('required', null);
        }
        $form.submit();
    });
    $('form').submit(function() {
        if (!this.checkValidity()) {
            alert('Fill the required fields!');
            return false;
        }
        const $this = $(this);
        const $checkboxRequired = $this.find('.checkbox-required');
        if ($checkboxRequired.length > 0) {
            const $checkboxes = $checkboxRequired.find('input[type="checkbox"]:checked');
            if ($checkboxes.length === 0) {
                alert('Chose at least one ' + $checkboxRequired.attr('label') + ' !');
                return false;
            }
        }
        return true;
    });
    $('.link').click(function() {
        const $this = $(this);
        const href = $this.attr('href');
        if (href !== null && href !== undefined) {
            window.location.href = href;
        }
    })
});

const urlParams = new URLSearchParams(window.location.search);

/**
 * @param data Anything
 * @param textStatus String
 * @param jqXHR jqXHR
 * @param callback function|null
*/
const responseSuccess = function(data, textStatus, jqXHR, callback=null) {
    // console.info("[RESPONSE SUCCESS]");
    // console.log('data:');
    // console.log(data);
    // console.log('textStatus: ' + textStatus);
    if (callback !== null) {
        callback(data, textStatus, jqXHR);
    }
};

/**
 * @param jqXHR jqXHR
 * @param textStatus String
 * @param errorThrown String
 * @param callback function|null
*/
const responseError = function(jqXHR, textStatus, errorThrown, callback=null) {
    // console.error("[RESPONSE ERROR]");
    // console.log('jqXHR:');
    // console.log(jqXHR);
    // console.log('textStatus: ' + textStatus);
    // console.log('errorThrown: ' + errorThrown);
    if (callback !== null) {
        callback(jqXHR, textStatus, errorThrown);
    }
};

const request = function(
    method,
    url,
    data=null,
    successCallback=null,
    errorCallback=null
) {
    if (method === 'GET' && data !== null) {
        url += '?' + $.param(data);
        data = null;
    }
    $.ajax({
        method: method,
        url: url,
        data: data,
        headers: {
            'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            responseSuccess(data, textStatus, jqXHR, successCallback);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            responseError(jqXHR, textStatus, errorThrown, errorCallback);
        }
    });
};

/**
 *
 * @param values The row values
 * @param action The function to call on row click
 */
$.fn.insertTableRow = function (values, action = null) {
    const $table = $(this);
    let tableRow = '<tr>';
    values.forEach(value => {
        let title = value.title === undefined ? '' : 'title="' + value.title + '"';
        tableRow += '<td '+title+'>' + value.name + '</td>';
    });
    tableRow += '</tr>';
    const $tableRow = $(tableRow).appendTo($table.find('tbody:last-child'));
    if (action !== null && action !== undefined) {
        $tableRow.click(action);
    }
};

$.fn.visible = function() {
    return this.css('visibility', 'visible');
};

$.fn.invisible = function() {
    return this.css('visibility', 'hidden');
};

/**
 * Move the spinner inside the jQuery Element
 * @param message The message to show (default: "Loading...")
 */
$.fn.spinner = function (message='Loading...') {
    moveSpinner($(this), message);
    startSpinner();
};

/**
 * Move the spinner inside $parent
 * @param $parent A jQuery element
 * @param message The message to show (default: "Loading...")
 */
const moveSpinner = function($parent, message='Loading...') {
    $parent.append($('#spinner'));
    $('.spinner-text').html(message);
};

/**
 * Show the spinner
 */
const startSpinner = function() {
    $('#spinner').show();
};


/**
 * Show the spinner
 */
const showingSpinner = function() {
    return $('#spinner').is(':visible');
};

/**
 * Hide the spinner
 */
const stopSpinner = function() {
    $('#spinner').hide();
};

/**
 *
 * @param msg
 * @param type success|warning|danger
 * @param icon https://material.io/resources/icons
 * @param from
 * @param align
 */
const notify = function(msg, type='warning', icon='warning', from='top', align='right') {
    $.notify({
        icon: icon,
        message: msg
    },{
        type: type,
        timer: 3000,
        placement: {
            from: from,
            align: align
        }
    });
};

const initAccordions = function() {
    const $toggle = $('.toggle');
    $toggle.each(function() {
        const $this = $(this);
        $this.unbind();
        $this.click(function() {
            if ($this.next().hasClass('show')) {
                // Hide
                $this.find('.arrow').html('keyboard_arrow_right');
                $this.next().removeClass('show');
                $this.next().slideUp(350);
            } else {
                // Show
                const $parent = $this.parent().parent();
                $parent.find('.arrow').html('keyboard_arrow_right');
                const $innerParent = $parent.find('li .inner');
                $innerParent.removeClass('show');
                $innerParent.slideUp(350);
                $this.next().toggleClass('show');
                $this.find('.arrow').html('keyboard_arrow_down');
                $this.next().slideToggle(350);
                let $container = $this.closest('.modal');
                if ($container.length === 0) {
                    $container = $('html');
                }
                setTimeout(function () {
                    const top = $this.offset().top - $container.offset().top + $container.scrollTop();
                    $container.animate({ scrollTop: top }, 300);
                }, 350);
            }
        });
    });

};
initAccordions();
