#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import List, Dict
from jinja2 import Template
from datetime import datetime
from datetime import date

logger = logging.getLogger(__name__)


class Expert:
    def __init__(self, data: Dict[str, str]):
        self._name = data["name"]
        self._prompt = data["prompt"]
        self._question = data["question"]
        self._chat_id = data["chat_id"]
        self._thread_id = data["thread_id"]

    def get_chat_id(self):
        return self._chat_id

    def get_thread_id(self):
        return self._thread_id

    def messages(self) -> List[Dict[str, str]]:
        template_prompt = Template(self._prompt)
        variables = self.get_variables()
        prompt = template_prompt.render(variables)
        template_question = Template(self._question)
        question = template_question.render(variables)
        logger.debug(f"prompt: {prompt}")
        logger.debug(f"question: {question}")
        return [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ]

    def get_variables(self):
        variables = {"now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        if self._name == "shell":
            day1 = datetime.now().date()
            day0 = date(day1.year, 1, 1)
            number_of_days = (day1 - day0).days
            commands = [
                "ls",
                "cd",
                "pwd",
                "mkdir",
                "rmdir",
                "rm",
                "touch",
                "cp",
                "mv",
                "ln",
                "chmod",
                "chown",
                "chgrp",
                "find",
                "grep",
                "sed",
                "awk",
                "cat",
                "more",
                "less",
                "tail",
                "head",
                "diff",
                "tar",
                "gzip",
                "gunzip",
                "bzip2",
                "zip",
                "df",
                "du",
                "ps",
                "kill",
                "top",
                "htop",
                "ps aux",
                "pkill",
                "killall",
                "pgrep",
                "uptime",
                "free",
                "uname",
                "whoami",
                "hostname",
                "ifconfig",
                "ip",
                "ping",
                "traceroute",
                "netstat",
                "ss",
                "route",
                "lsof",
                "iwconfig",
                "iwlist",
                "nmcli",
                "journalctl",
                "systemctl",
                "service",
                "chkconfig",
                "reboot",
                "shutdown",
                "init",
                "useradd",
                "userdel",
                "passwd",
                "usermod",
                "groupadd",
                "groupdel",
                "adduser",
                "deluser",
                "addgroup",
                "delgroup",
                "id",
                "who",
                "w",
                "last",
                "finger",
                "sudo",
                "su",
                "chsh",
                "chfn",
                "visudo",
                "history",
                "echo",
                "printf",
                "read",
                "export",
                "alias",
                "source",
                "script",
                "nohup",
                "bg",
                "fg",
                "jobs",
                "kill",
                "kill -9",
                "ps aux | grep",
                "pgrep",
                "pkill",
                "renice",
                "nice",
                "time",
                "date",
                "cal",
                "sleep",
                "watch",
                "echo $?",
                "exit",
                "logout",
                "clear",
                "reset",
                "man",
                "info",
                "whatis",
                "apropos",
                "locate",
                "updatedb",
                "whereis",
                "which",
                "type",
                "file",
                "stat",
                "du -h",
                "df -h",
                "du -sh *",
                "df -T",
                "mount",
                "umount",
                "fdisk",
                "parted",
                "lsblk",
                "blkid",
                "df -i",
                "sync",
                "lscpu",
                "lsusb",
                "lspci",
                "lsmod",
                "modinfo",
                "insmod",
                "rmmod",
                "lsmod | grep",
                "dmesg",
                "journalctl",
                "ps -eaf",
                "ps aux --forest",
                "top -c",
                "htop",
                "iostat",
                "vmstat",
                "sar",
                "mpstat",
                "nmon",
                "atop",
                "uptime",
                "free",
                "ps -eo pid,user,args | grep",
                "lsof -i",
                "netstat -tulpn",
                "ss -tulpn",
                "ip address show",
                "ip route show",
                "route -n",
                "traceroute",
                "arp",
                "ethtool",
                "ifup",
                "ifdown",
                "nmcli",
                "hostnamectl",
                "systemctl list-units --type service --all",
                "systemctl start",
                "systemctl stop",
                "systemctl restart",
                "systemctl reload",
                "systemctl enable",
                "systemctl disable",
                "journalctl -xe",
                "journalctl -u",
                "journalctl -f",
                "service --status-all",
                "chkconfig --list",
                "chkconfig --add",
                "chkconfig --del",
                "chkconfig --level",
                "reboot",
                "shutdown",
                "init",
                "runlevel",
                "telinit",
                "useradd",
                "userdel",
                "passwd",
                "usermod",
                "groupadd",
                "groupdel",
                "adduser",
                "deluser",
                "addgroup",
                "delgroup",
                "id",
                "who",
                "w",
                "last",
                "finger",
                "passwd",
                "sudo",
                "su",
                "chsh",
                "chfn",
                "visudo",
                "history",
                "echo",
                "printf",
                "read",
                "export",
                "alias",
                "source",
                "script",
                "nohup",
                "bg",
                "fg",
                "jobs",
                "kill",
                "kill -9",
                "ps aux | grep",
                "pgrep",
                "pkill",
                "renice",
                "nice",
                "time",
                "date",
                "cal",
                "sleep",
                "watch",
                "echo $?",
                "exit",
                "logout",
                "clear",
                "reset",
                "man",
                "info",
                "whatis",
                "apropos",
                "locate",
                "updatedb",
                "whereis",
                "which",
                "type",
                "file",
                "stat",
                "du -h",
                "df -h",
                "du -sh *",
                "df -T",
                "mount",
                "umount",
                "fdisk",
                "parted",
                "lsblk",
                "blkid",
                "df -i",
                "sync",
                "lscpu",
                "lsusb",
                "lspci",
                "lsmod",
                "modinfo",
                "insmod",
                "rmmod",
                "lsmod | grep",
                "dmesg",
                "journalctl",
                "ps -eaf",
                "ps aux --forest",
                "top -c",
                "htop",
                "iostat",
                "vmstat",
                "sar",
                "mpstat",
                "nmon",
                "atop",
                "uptime",
                "free",
                "ps -eo pid,user,args | grep",
                "lsof -i",
                "netstat -tulpn",
                "ss -tulpn",
                "ip address show",
                "ip route show",
                "route -n",
                "traceroute",
                "arp",
                "ethtool",
                "ifup",
                "ifdown",
                "nmcli",
                "hostnamectl",
                "systemctl list-units --type service --all",
                "systemctl start",
                "systemctl stop",
                "systemctl restart",
                "systemctl reload",
                "systemctl enable",
                "systemctl disable",
                "journalctl -xe",
                "journalctl -u",
                "journalctl -f",
                "service --status-all",
                "chkconfig --list",
                "chkconfig --add",
                "chkconfig --del",
                "chkconfig --level",
                "reboot",
                "shutdown",
                "init",
                "runlevel",
                "telinit",
            ]
            command = commands[number_of_days]
            variables.update({"command": command})
        return variables
