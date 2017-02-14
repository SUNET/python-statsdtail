# -*- coding: utf-8 -*-

import argparse
import sys
import daemon
import time
import re
import yaml
from tailhead import follow_path
import statsd


__author__ = 'lundberg'

CONFIG_FILE = '/etc/python-statsdtail.yaml'


class Statsd(object):

    def __init__(self, host, port, prefix=None):
        self.client = statsd.StatsClient(host, port, prefix=prefix)

    def count(self, name, value=1):
        self.client.incr(name, count=value)


class Matcher(object):

    def __init__(self, config, match):
        self.patterns = []
        self.statsd_clients = {}
        for name in match:
            if name in config.get('patterns', []):
                prefix = config['patterns'][name]['stats']['prefix']
                if prefix not in self.statsd_clients:
                    host = config['statsd']['host']
                    port = config['statsd']['port']
                    self.statsd_clients[prefix] = Statsd(host, port, prefix)
                self.patterns.append(config['patterns'][name])
        if not self.patterns:
            print('No patter configuration found for {}. Exiting.'.format(match))
            sys.exit(1)

    def match(self, line):
        matched = False
        for pattern in self.patterns:
            if pattern['match'].search(line):
                matched = True
                statsd_client = self.statsd_clients[pattern['stats']['prefix']]
                statsd_client.count(pattern['stats']['name'])
        return matched


def load_config(config_file):
    try:
        with open(config_file) as f:
            config = yaml.load(f)
    except IOError as e:
        print(e)
        sys.exit(1)
    # Compile regex
    patterns = config.get('patterns', [])
    for pattern in patterns:
        patterns[pattern]['match'] = re.compile(patterns[pattern]['match'])
    config['patterns'].update(patterns)
    return config


def main():
    # User friendly usage output
    parser = argparse.ArgumentParser()
    parser.add_argument('logfile', nargs='?', type=str)
    parser.add_argument('-m', '--match', action='append', help='Match configuration to use', required=True, type=str)
    parser.add_argument('-c', '--config', help='Config file', required=False, type=str, default=CONFIG_FILE)
    parser.add_argument('-d', '--detach', help='Run daemon in foreground', default=False,
                        action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose output', default=False,
                        action='store_true')
    args = parser.parse_args()
    config = load_config(args.config)
    # Use config to set up core functionality
    core_config = config.get('core', {})
    working_dir = core_config.get('working_directory', '/tmp')
    try:
        # Starts the daemon reading the log file, matches
        context = daemon.DaemonContext(working_directory=working_dir)
        if not args.detach:
            context.detach_process = False
            context.stdout = sys.stdout
            context.stderr = sys.stderr

        with context:
            # Set up matcher in context to not lose open sockets (in Statsd objects)
            matcher = Matcher(config, args.match)

            if not args.detach:
                print('Looking for matches: {}'.format(args.match))
                print('Collecting stats for: {}:{}'.format(config['statsd']['host'], config['statsd']['port']))
                print('Reading from {}...'.format(args.logfile))

            for line in follow_path(args.logfile):
                if line is None:
                    time.sleep(1)
                    continue
                matched = matcher.match(line)
                if matched and args.verbose:
                    print('Matched line: {}'.format(line))
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
