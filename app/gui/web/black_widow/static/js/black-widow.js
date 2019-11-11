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
    $('input.submit').change(function(e) {
        const $form = $(this).closest('form');
        $form.submit();
    });
    $('form').submit(function() {
        if (!this.checkValidity()) {
            alert('Fill the required fields!')
            return false;
        }
        return true;
    });
});

const urlParams = new URLSearchParams(window.location.search);

/**
 * @param Anything data
 * @param String textStatus
 * @param jqXHR jqXHR
 * @param function|null callback
*/
const responseSuccess = function(data, textStatus, jqXHR, callback=null) {
    console.info("[RESPONSE SUCCESS]")
    console.log('data:');
    console.log(data);
    console.log('textStatus: ' + textStatus)
    if (callback !== null) {
        callback(data, textStatus, jqXHR);
    }
}

/**
 * @param jqXHR jqXHR
 * @param String textStatus
 * @param String errorThrown
 * @param function|null callback
*/
const responseError = function(jqXHR, textStatus, errorThrown, callback=null) {
    console.error("[RESPONSE ERROR]")
    console.log('jqXHR:');
    console.log(jqXHR);
    console.log('textStatus: ' + textStatus)
    console.log('errorThrown: ' + errorThrown)
    if (callback !== null) {
        callback(jqXHR, textStatus, errorThrown);
    }
}

const getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
    console.log("[REQUEST]: " + method + ' ' + url);
    console.log("[REQUEST DATA]:");
    console.log(data);
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
        error: function(data, textStatus, jqXHR) {
            responseSuccess(data, textStatus, jqXHR, errorCallback);
        }
    });
};
