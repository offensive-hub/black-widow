/********************************************************************************
 *                                                                               *
 * job.js -- black-widow jobs javascript                                         *
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
    let jobId = urlParams.get('id');
    let lastProcessStatus = null;
    let lastJobDataCount = 0;
    let lastJobDataPage = -1;
    let emptyCount = -1;
    let jobRestarted = false;

    const $dataTable = $('#data-table').find('table').first();
    const $playBtn = $('#play-btn');
    const $pauseBtn = $('#pause-btn');
    const $stopBtn = $('#stop-btn');
    const $deleteBtn = $('#delete-btn');
    const $restartBtn = $('#restart-btn');
    const $downloadBtn = $('#download-btn');
    const $pagination = $('#pagination');
    const $mainBody = $('#main-body');
    const parentUrl = $('ol.breadcrumb').find('.parent').attr('href');

    $mainBody.spinner('Setting up job...');

    let currentPage = 1;
    let pages = 1;

    if (window.location.hash.indexOf('#page-') === 0) {
        const tmpCurrentPage = parseInt(window.location.hash.substr(6, 1));
        if (tmpCurrentPage) {
            currentPage = tmpCurrentPage;
            pages = tmpCurrentPage;
        }
    }

    // Pagination
    $pagination.pagination({
        dataSource: [],
        pageNumber: 1,
        items: 0,
        pages: pages,
        currentPage: currentPage,
        itemsOnPage: 10,
        cssStyle: 'dark-theme'
    });

    const updateData = function(sleep, loop=false) {
        window.setTimeout(function() {
            if (jobRestarted) {
                console.log('jobRestarted');
                jobRestarted = false;
                return;
            }
            if (loop && $pauseBtn.hasClass('disabled')) {
                return;
            }
            request('POST', window.location.pathname, {
                'id': jobId,
                'page':  $pagination.pagination('getCurrentPage'),
                'page_size': 10
            }, function(data) {
                if (data.job.status !== lastProcessStatus) {
                    lastProcessStatus = data.job.status;
                    if (data.job.status === 'SIGCONT') {
                        // Process running
                        $pauseBtn.removeClass('disabled').show();
                        $playBtn.addClass('disabled').hide();
                        $stopBtn.removeClass('disabled');
                        emptyCount = 0;
                    } else if (data.job.status === 'SIGSTOP') {
                        // Process paused
                        $pauseBtn.addClass('disabled').hide();
                        $playBtn.removeClass('disabled').show();
                        $stopBtn.removeClass('disabled');
                    } else if (data.job.status === 'SIGKILL') {
                        // Process stopped
                        if (showingSpinner()) {
                            stopSpinner();
                        }
                        $pauseBtn.addClass('disabled').hide();
                        $playBtn.addClass('disabled').show();
                        $stopBtn.addClass('disabled');
                        $downloadBtn.removeClass('disabled');
                    }
                }

                if (lastJobDataCount !== data.total || lastJobDataPage !== data.page) {
                    lastJobDataCount = data.total;
                    lastJobDataPage = data.page;
                    $dataTable.find('tbody').html('');
                    showJobData(data.result);

                    // Pagination
                    $pagination.pagination({
                        dataSource: Object.values(data.result),
                        pageNumber: data.page,
                        items: data.total,
                        pages: data.page_end,
                        currentPage: $pagination.pagination('getCurrentPage'),
                        itemsOnPage: 10,
                        cssStyle: 'dark-theme',
                        onPageClick: function() {
                            updateData(0, false);
                        }
                    });

                    if (data.total === 0 && data.job.status !== 'SIGKILL') {
                        $mainBody.spinner('Waiting data...');
                    }

                    if (data.total > 0 && showingSpinner()) {
                        stopSpinner();
                    }
                    emptyCount = 0;
                } else if (data.job.status === 'SIGKILL') {
                    emptyCount += 1;
                    if (emptyCount >= 6) {
                        loop = false;
                    }
                }

                if (loop) {
                    updateData(1300, loop);
                } else {
                    console.log('Retrying data stopped. Refresh the page to re-enable that.');
                }
            }, function() {
                console.error('Request error!');
                window.location.replace(parentUrl);
            });
        }, sleep);
    };

    /**
     * Send a signal to job
     * @param signal The numeric signal to send
     * @param callback The callback to call after signal
     */
    const signJob = function(signal, callback) {
        request('POST', window.location.pathname, {
            'id': jobId,
            'signal': signal
        }, function(data, textStatus, jqXHR) {
            callback(data, textStatus, jqXHR);
        }, function(jqXHR) {
            if (jqXHR.responseJSON) {
                notify(jqXHR.responseJSON.message, 'warning');
            } else {
                console.error('Request error!');
                window.location.replace(parentUrl);
            }
        });
    };

    /**
     * Send a SIGABRT to the current job
     */
    const deleteJob = function() {
        if (confirm("This job will be permanently deleted. Are you sure ?")) {
            // 6 = SIGABRT
            signJob(6, function() {
                window.location.replace($('ol.breadcrumb').find('.parent').attr('href'));
            });
        }
    };
    $deleteBtn.click(deleteJob);

    /**
     * Send a SIGHUP to the current job
     */
    const restartJob = function() {
        $mainBody.spinner('Restarting job...');
        jobRestarted = true;
        $pauseBtn.show().addClass('disabled');
        $playBtn.hide().addClass('disabled');
        pauseJob(false);
        $dataTable.find('tbody').html('');
        $pagination.pagination({
            dataSource: [],
            pageNumber: 1,
            items: 0,
            pages: 1,
            currentPage: 1,
            itemsOnPage: 10,
            cssStyle: 'dark-theme'
        });
        lastJobDataCount = 0;
        lastJobDataPage = -1;
        emptyCount = 0;
        lastProcessStatus = null;
        // 0 = SIGRESTART (custom signal)
        signJob(0, function(data) {
            jobId = data.id;
            history.pushState('data', '', window.location.pathname + '?id=' + jobId);
            $downloadBtn.attr('href', $downloadBtn.attr('base_href') + '?id=' + jobId);
            $playBtn.hide();
            $pauseBtn.show();
            $mainBody.spinner('Waiting data...');
            setTimeout(function() {
                jobRestarted = false;
                playJob();
            }, 1400);

        });
    };
    $restartBtn.click(restartJob);

    /**
     * Send a SIGKILL to the current job
     */
    const stopJob = function() {
        // 9 = SIGKILL
        signJob(9, function() {
            $stopBtn.addClass('disabled');
            $pauseBtn.addClass('disabled').hide();
            $playBtn.addClass('disabled').show();
        });
    };
    $stopBtn.click(stopJob);

    /**
     * Send a SIGSTOP to the current job
     */
    const pauseJob = function(changeButtonStatus = true) {
        // 19 = SIGSTOP
        signJob(19, function() {
            if (changeButtonStatus) {
                $playBtn.removeClass('disabled').show();
                $pauseBtn.addClass('disabled').hide();
            }
            $stopBtn.removeClass('disabled');
        });

    };
    $pauseBtn.click(pauseJob);

    /**
     * Send a SIGCONT to the current job
     */
    const playJob = function() {
        // 18 = SIGCONT
        signJob(18, function() {
            $playBtn.addClass('disabled').hide();
            $pauseBtn.removeClass('disabled').show();
            $stopBtn.removeClass('disabled');
            updateData(300, true);
        });
    };
    $playBtn.click(playJob);

    updateData(300, true);
});
