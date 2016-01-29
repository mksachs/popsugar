#! /bin/sh
""":"
exec python $0 ${1+"$@"}
"""

import sys
import urllib
import os
import logging
import collections
import re
import math
import argparse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append('./')

# Will skip any log lines that don't have a client or a process_time
log_format_pat = re.compile(
    r'(?P<ip>\S+)\s+'
    r'(?P<client>\S+)\s+'
    r'(?P<auth>\S+\s+\S+)\s+'
    r'(?P<timestamp>\[[^]]+\])\s+'
    r'(?P<process_time>\S+)\s+'
    r'"(?P<action>[^"]+)"\s+'
    r'(?P<status>[0-9]+)\s+'
    r'(?P<size>[-0-9]+)\s+'
    r'"(?P<referrer>[^"]*)"\s+'
    r'"(?P<useragent>[^"]*)"\s+'
    r'"(?P<other>[^"]*)"'
)

Logline = collections.namedtuple(
    'Logline',
    [
        'ip', 'client', 'auth', 'timestamp', 'process_time', 'action', 'status', 'size', 'referrer',
        'useragent', 'other'
    ]
)


def log_line_iter(in_source_iter):
    for line in (l.rstrip() for l in in_source_iter):
        match = log_format_pat.match(line)
        if match:
            yield Logline(**match.groupdict())


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--plot', help='Output data for plotting.', dest='plot', action='store_true')

    args = parser.parse_args()

    log_file = 'test-access.log'

    if not os.path.isfile('test-access.log'):
        file_source = 'http://www.popsugar.com/files/docs/test-access.log'
        logger.info('Downloading log file from {} to {}.'.format(file_source, log_file))
        log_file_download = urllib.URLopener()
        log_file_download.retrieve(file_source, log_file)

    status_codes = {}
    process_times = []
    for log_line in log_line_iter(open(log_file, 'r')):
        if log_line.status in status_codes:
            status_codes[log_line.status] += 1
        else:
            status_codes[log_line.status] = 1
        process_times.append(float(log_line.process_time))

    sorted_process_times = sorted(process_times, reverse=True)

    if len(sorted_process_times) % 2 == 0:
        primary_index = int(float(len(sorted_process_times)) / 2.0)
        median = (sorted_process_times[primary_index] + sorted_process_times[primary_index - 1]) / 2.0
    else:
        median = sorted_process_times[int(math.floor(float(len(sorted_process_times)) / 2.0))]

    average = sum(sorted_process_times) / float(len(sorted_process_times))

    logger.info('Processing Times')
    logger.info('Median: {}'.format(median))
    logger.info('Average: {}'.format(average))
    logger.info('Top 10 processing times:')
    for n, processing_time in enumerate(sorted_process_times[0:10]):
        logger.info('    {}: {}'.format(n + 1, processing_time))
    logger.info('')

    logger.info('Status Codes (code: count)')
    for code in sorted(status_codes, key=lambda (k): status_codes[k], reverse=True):
        logger.info('{}: {}'.format(code, status_codes[code]))

    if args.plot:
        logger.info('--------------------')
        logger.info('Plotable histogram:')
        print 'code,count'
        for code in sorted(status_codes, key=lambda (k): status_codes[k], reverse=True):
            print '{},{}'.format(code, status_codes[code])
        logger.info('')

        logger.info('Plotable cumulative frequency process time:')
        print 'process_time,cumulative_frequency'
        for n, process_time in enumerate(sorted(process_times)):
            print '{},{}'.format(process_time, len(process_times) - n - 1)


if __name__ == "__main__":
    sys.exit(main())


__author__ = 'Michael Sachs'
