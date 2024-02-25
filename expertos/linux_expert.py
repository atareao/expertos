#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from datetime import date
from datetime import datetime
from typing import Dict
from expertos import log
from expertos.db import DB
from expertos.expert import Expert


class LinuxExpert(Expert):
    def __init__(self, db: DB, data: Dict[str, str]):
        super().__init__(db, data)
        self._table_name = "linux_expert"
        if not self._db.table_exists(self._table_name):
            self.configure_db()

    def configure_db(self):
        sql = (f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
               "id INTEGER PRIMARY KEY,"
               "command TEXT NOT NULL DEFAULT '',"
               "published BOOLEAN NOT NULL DEFAULT FALSE)")
        self._db.execute(sql)
        sql = f"INSERT INTO {self._table_name} (command) VALUES (?)"
        for command in self.commands():
            self._db.insert(sql, (command,))

    @staticmethod
    def commands():
        commands = [
            "ls", "cd", "pwd", "mkdir", "rmdir", "rm", "cp", "mv", "touch",
            "ln", "grep", "sed", "awk", "cat", "more", "less", "tail", "head",
            "cut", "sort", "uniq", "top", "htop", "ps", "kill", "pkill",
            "chmod", "chown", "df", "du", "free", "uptime", "whoami", "ping",
            "ifconfig", "ip", "netstat", "wget", "curl", "ssh", "scp", "ftp",
            "echo", "date", "tar", "gzip", "gunzip", "zip", "unzip", "find",
            "which", "alias", "history", "man", "chmod", "chown", "crontab",
            "at", "useradd", "usermod", "userdel", "groupadd", "groupmod",
            "groupdel", "passwd", "chage", "su", "sudo", "visudo", "mount",
            "umount", "fsck", "dd", "fdisk", "parted", "mkfs", "lsblk",
            "blkid", "swapon", "swapoff", "lsof", "strace", "nmcli",
            "firewall-cmd", "iptables", "ufw", "journalctl", "systemctl",
            "service", "init", "chkconfig", "dmesg", "hostname", "host", "dig",
            "nslookup", "route", "traceroute", "mtr", "arp", "ethtool",
            "iwconfig", "nmap", "tcpdump", "rsync", "git", "svn", "make",
            "gcc", "g++", "objdump", "strace", "ldd", "nm", "size", "strings",
            "readelf", "diff", "patch", "tar", "bzip2", "xz", "cURL", "wget",
            "scp", "rsync", "nc", "ssh-keygen", "ssh-copy-id", "ssh-add",
            "screen", "tmux", "gzip", "gunzip", "bzip2", "bunzip2", "xz",
            "unxz", "zip", "unzip", "7z", "7za", "locate", "updatedb", "find",
            "grep", "egrep", "fgrep", "rg", "awk", "sed", "diff", "vim",
            "nano", "emacs", "cat", "tac", "less", "more", "head", "tail",
            "cut", "paste", "join", "sort", "uniq", "tr", "fold", "wc", "nl",
            "seq", "split", "csplit", "expand", "unexpand", "fmt", "pr",
            "column", "colrm", "paste", "comm", "cmp", "diff", "sdiff",
            "diff3", "patch", "as", "ld", "gdb", "valgrind", "strace",
            "ltrace", "time", "m4", "make", "cmake", "autoconf", "automake",
            "bison", "flex", "gettext", "patch", "rpm", "yum", "dnf", "apt",
            "apt-get", "apt-cache", "dpkg", "snap", "flatpak", "pip", "gem",
            "npm", "cargo", "systemctl", "journalctl", "loginctl",
            "hostnamectl", "timedatectl", "localectl", "networkctl",
            "firewall-cmd", "iptables", "ss", "ip", "ifconfig", "route",
            "traceroute", "ping", "arp", "ethtool", "mii-tool", "netstat",
            "nmap", "tcpdump", "wireshark", "tshark", "iperf", "iperf3",
            "curl", "wget", "links", "lynx", "mail", "mutt", "alpine",
            "sendmail", "postfix", "dovecot", "procmail", "fetchmail", "imap",
            "pop3", "sftp", "vsftpd", "proftpd", "nfs", "smbclient", "mount",
            "umount", "cryptsetup", "luksOpen", "luksClose", "e2fsck",
            "resize2fs", "dumpe2fs", "tune2fs", "fsck", "parted", "gparted",
            "ntfsfix", "mkfs", "mkswap", "swapon", "swapoff", "dd",
            "genisoimage", "wodim", "brasero", "growisofs", "isoinfo",
            "os-prober", "grub-install", "grub-mkconfig", "update-grub",
            "efibootmgr", "lvm", "pvcreate", "vgcreate", "lvcreate",
            "pvdisplay", "vgdisplay", "lvdisplay", "pvremove", "vgremove",
            "lvremove", "pvresize", "vgextend", "lvextend", "pvreduce",
            "vgsplit", "lvreduce", "vgmerge", "lvs", "vgs", "pvs", "lvrename",
            "vgrename", "lvremove", "vgremove", "pvmove", "lvconvert",
            "vgconvert", "pvscan", "vgscan", "lvscan", "lvchange", "vgchange",
            "pvchange", "lvmdiskscan", "lvmdump", "vgcfgbackup",
            "vgcfgrestore", "lvcreate", "lvremove", "lvresize", "lvextend",
            "lvreduce", "lvrename", "lvs", "vgs", "pvs", "lvdisplay",
            "vgdisplay", "pvdisplay", "lvscan", "vgscan", "pvscan", "lvchange",
            "vgchange", "pvchange", "lvmdiskscan", "lvreduce", "lvextend",
            "fsadm", "lvmsnapshot", "lvm2snapshot", "lvcreate", "lvconvert",
            "lvextend", "lvreduce", "lvremove", "lvs", "vgs", "pvs",
            "lvdisplay", "vgdisplay", "pvdisplay", "lvscan", "vgscan",
            "pvscan"]
        return iter(commands)

    def get_variables(self):
        variables = super().get_variables()
        sql = f"SELECT * FROM {self._table_name} WHERE published = ?"
        values = self._db.select(sql, (False,))
        selected = random.choice(values)
        log.debug(selected)
        variables.update({"command": selected[1]})
        sql = f"UPDATE {self._table_name} SET published = ? WHERE id = ?"
        values = self._db.update(sql, (True, selected[0]))
        log.debug(values)
        return variables
