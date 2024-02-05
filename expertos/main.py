#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import aiofiles
import logging
import sys
import tomllib
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from datetime import datetime
from datetime import date
from expert import Expert
from openai import ChatGPT
from telegram import Telegram

FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Sanic(__name__)


@app.before_server_start
async def attach_db(app, loop):
    experts = {}
    async with aiofiles.open("config.toml", mode="r") as fr:
        contents = await fr.read()
        data = tomllib.loads(contents)
        logger.debug(data)
        for data_expert in data["experts"]:
            experts[data_expert["name"]] = Expert(data_expert)
    app.ctx.experts = experts
    app.ctx.chat_gpt = ChatGPT(
        data["openai"]["url"],
        data["openai"]["endpoint"],
        data["openai"]["token"],
        data["openai"]["model"],
    )
    app.ctx.telegram = Telegram(data["telegram"]["url"], data["telegram"]["token"])


def get_variables(expert_name: str):
    variables = {"now": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    if expert_name == "shell":
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


@app.get("/status")
async def status_handler(request: Request):
    logger.info("status_handler")
    return json({"status": "Ok", "message": "up and running"})


@app.get("/query/<expert_name>", name="query_expert_name")
@app.get("/query")
async def query_handler(request: Request, expert_name: str | None = None):
    experts_name = list(app.ctx.experts.keys())
    if expert_name:
        if expert_name in experts_name:
            expert = app.ctx.experts[expert_name]
            variables = get_variables(expert_name)
            response = await app.ctx.chat_gpt.post(expert, variables)
            return json({"status": "Ok", "advice": response})
        else:
            return json({"status": "Ko", "message": f"{expert_name} not found"})
    else:
        logger.debug(experts_name)
        return json({"status": "Ok", "data": {"experts": experts_name}})


@app.get("/post/<expert_name>", name="post_expert_name")
async def post_handler(request: Request, expert_name: str):
    experts_name = list(app.ctx.experts.keys())
    if expert_name:
        if expert_name in experts_name:
            expert = app.ctx.experts[expert_name]
            variables = get_variables(expert_name)
            advice = await app.ctx.chat_gpt.post(expert, variables)
            response = await app.ctx.telegram.post(expert, advice)
            logger.debug(response)
            return json(response)
        else:
            return json({"status": "Ko", "message": f"{expert_name} not found"})
    else:
        logger.debug(experts_name)
        return json({"status": "Ko", "message": "expert_name is mandatory"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
