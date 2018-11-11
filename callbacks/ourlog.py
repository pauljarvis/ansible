from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import sys
from datetime import datetime

try:
    from ansible.utils.color import colorize, hostcolor
    from ansible.plugins.callback import CallbackBase
except ImportError:
    class CallbackBase:
        pass

# Fields we will delete from the result
DELETABLE_FIELDS = [
    'stdout', 'stdout_lines', 'rc', 'stderr', 'start', 'end',
    '_ansible_verbose_always', '_ansible_no_log', 'diff', 'changed'
]

ANSIBLE_STATUSES = [
    "OK", "CHANGED", "SKIPPED", "FAILED", "UNREACHABLE"
]

# Colours
COLOUR_CHANGED = 'yellow'
COLOUR_OK = 'green'
COLOUR_SKIPPED = 'cyan'
COLOUR_INCLUDED = 'cyan'
COLOUR_FAILED = 'red'
COLOUR_UNREACHABLE = 'red'
COLOUR_EXTRA = 'magenta'


def override(o):
    return o


def deep_serialize_list(data, indent=1):
    padding = " " * indent * 2
    output = "\n"
    for item in data:
        output = "%s->%s%s" % (
            output,
            padding,
            deep_serialize(item, indent + 1)
        )

    return output


def deep_serialize_dict(data, indent=1):
    padding = " " * indent * 2
    if "_ansible_no_log" in data and data["_ansible_no_log"]:
        data = {
            "censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result"
        }

    for key in DELETABLE_FIELDS:
        if key in data.keys():
            del data[key]

    output = "\n"
    for key, value in data.items():
        output = "%s%s%s: %s\n" % (
            output,
            padding,
            key,
            deep_serialize(value, indent + 1)
        )

    return output


def deep_serialize_string(data):
    string_form = str(data)
    if len(string_form) == 0:
        return '""'
    else:
        return string_form


def deep_serialize(data, indent=0):
    if isinstance(data, list):
        return deep_serialize_list(data, indent)
    elif isinstance(data, dict):
        return deep_serialize_dict(data, indent)
    else:
        return deep_serialize_string(data)


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'ourlog'

    def _capture_task_start(self):
        self.task_started = datetime.now()

    def _capture_task_end(self):
        self.task_ended = datetime.now()

    def _get_duration(self):
        self.task_ended = datetime.now()
        total_duration = (self.task_ended - self.task_started)
        return total_duration.total_seconds() * 1000

    def _emit_line(self, lines, color='normal'):
        for line in lines.splitlines():
            self._display.display(line, color=color)

    def _host_string(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)

        if delegated_vars:
            host_string = "%s -> %s" % (
                result._host.get_name(), delegated_vars['ansible_host']
            )
        else:
            host_string = result._host.get_name()

        return host_string

    def _output_result(self, color, status, host, msg="", extra_msgs=[]):
        line = " %s | %s | %s | %s" % (
            host.ljust(self.host_len),
            status.ljust(self.stat_len),
            ("%dms" % self._get_duration()).ljust(self.ms_len),
            msg
        )

        self._display.display(line, color)
        if extra_msgs:
            self._display.display(extra_msgs, COLOUR_EXTRA)

    def _collect_host_info(self, hosts):
        self.host_count = len(hosts)
        self.host_len = 0
        for host in hosts:
            self.host_len = max(self.host_len, len(str(host)))
        self.stat_len = len(max(ANSIBLE_STATUSES, key=len))
        self.ms_len = 8

    def _is_changed(self, result):
        return result._result.get('changed', False)

    def _is_verbose(self, result):
        return (self._display.verbosity > 0 or ('_ansible_verbose_always' in result._result)) \
               and not ('_ansible_verbose_override' in result._result)

    @override
    def v2_playbook_on_play_start(self, *args, **kwargs):
        self._collect_host_info(
            args[0].get_variable_manager()._inventory.get_hosts()
        )

    @override
    def v2_playbook_on_task_start(self, task, is_conditional):
        self._capture_task_start()
        self._emit_line(
            "[{}] {} ...".format(
                self.task_started.strftime("%H:%M:%S"),
                task.get_name()
            )
        )

    @override
    def v2_playbook_on_handler_task_start(self, task):
        self._emit_line(
            "triggering handler | %s " %
            task.get_name().strip()
        )

    @override
    def v2_runner_on_failed(self, result, ignore_errors=False):
        extra_msgs = ""

        if self._is_verbose(result):
            extra_msgs = deep_serialize(result._result)

        self._output_result(
            COLOUR_FAILED,
            "FAILED",
            self._host_string(result),
            result._result.get('msg', ''),
            extra_msgs
        )

    @override
    def v2_on_file_diff(self, result):
        if result._task.loop and 'results' in result._result:
            for res in result._result['results']:
                if 'diff' in res and res['diff'] and res.get('changed', False):
                    diff = self._get_diff(res['diff'])
                    if diff:
                        self._emit_line(diff)

        elif 'diff' in result._result and \
                result._result['diff'] and \
                result._result.get('changed', False):
            diff = self._get_diff(result._result['diff'])
            if diff:
                self._emit_line(diff)

    @override
    def v2_runner_on_ok(self, result):
        self._clean_results(result._result, result._task.action)
        self._handle_warnings(result._result)
        extra_msgs = ""

        if self._is_verbose(result):
            extra_msgs = deep_serialize(result._result)

        if self._is_changed(result):
            self._output_result(
                COLOUR_CHANGED,
                "CHANGED",
                self._host_string(result),
                result._result.get('msg', ''),
                extra_msgs
            )
        else:
            self._output_result(
                COLOUR_OK,
                "OK",
                self._host_string(result),
                result._result.get('msg', ''),
                extra_msgs
            )

    @override
    def v2_runner_on_unreachable(self, result):
        extra_msgs = ""

        if self._is_verbose(result):
            extra_msgs = deep_serialize(result._result)

        self._output_result(
            COLOUR_UNREACHABLE,
            "UNREACHABLE",
            self._host_string(result),
            result._result.get('msg', '')
        )

    @override
    def v2_runner_on_skipped(self, result):
        extra_msgs = ""

        if self._is_verbose(result):
            extra_msgs = deep_serialize(result._result)

        self._output_result(
            COLOUR_SKIPPED,
            "SKIPPED",
            self._host_string(result)
        )

    @override
    def v2_playbook_on_include(self, included_file):
        self._emit_line(
            'included: %s for %s' % (
                included_file._filename,
                ", ".join([h.name for h in included_file._hosts])
            ),
            color=COLOUR_SKIPPED
        )

    @override
    def v2_playbook_on_stats(self, stats):
        self._emit_line("-- Summary --")

        hosts = sorted(stats.processed.keys())
        for host in hosts:
            totals = stats.summarize(host)
            self._emit_line(
                u" %s : %s %s %s %s" % (
                    hostcolor(host, totals),
                    colorize(u'ok', totals['ok'], COLOUR_OK),
                    colorize(u'changed', totals['changed'], COLOUR_CHANGED),
                    colorize(u'unreachable', totals['unreachable'], COLOUR_UNREACHABLE),
                    colorize(u'failed', totals['failures'], COLOUR_FAILED)
                )
            )

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)

        # Python2
        try:
            reload(sys).setdefaultencoding('utf8')
        except:
            pass
