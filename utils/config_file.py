#! /usr/bin/env python
# -*- coding: utf-8 -*-
import shutil

import errno

CONF_FILE  = 'config/hcbpy.conf'

import os
def touch(fname, times=None):
    dn = os.path.dirname(fname)

    if not os.path.exists(fname):
       if dn:
            try:
                os.makedirs(os.path.dirname(fname))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
       with open(fname, "w") as f:
           f.write("")

touch(CONF_FILE)

class ConfigEntry:
    key = ''
    val = ''
    comment = ''

    def __init__(self, key, val, comment):
        self.key = key
        self.val = val
        self.comment = comment


def get_all_data(filename=CONF_FILE):
    touch(filename)
    entrys = list()
    # filename = hcb_file(filename)
    f = open(filename, "rt")
    lines = f.read().split("\n")
    del f

    for line in lines:
        if line.__contains__("->"):
            key = line.split("->")[0]
            val = line.split("->")[1]
            comment = get_comment(key)
            entry = ConfigEntry(key, val, comment)
            entrys.append(entry)
    return entrys


def get_field(field_name, filename=CONF_FILE):
    touch(filename)
    # filename = hcb_file(filename)
    with open(filename, 'rt') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and line.split("->")[0].strip() == field_name:
                result = line.split("->")[1].strip().replace("\n", "")
                if result.lower() == "none":
                    return None
                else:
                    return result
        set_field(field_name, "none", filename=filename)
        return ""


def init_field(key, val="none", filename=CONF_FILE):
    if not get_field(key, filename=filename):
        set_field(key, val, filename=filename)


def has(field_name, filename=CONF_FILE):
    init_field(field_name, filename=filename)
    lines = get_lines(filename)

    for line in lines:
        if line.__contains__("->"):
            key = line.split("->")[0].strip()
            val = line.split("->")[1].strip()
            if key == field_name and (val == "1" or val.lower() == "true"):
                return True
    return False


def get_lines(filename):
    touch(filename)
    # filename = hcb_base.hcb_file(filename)
    f = open(filename, "rt")
    lines = f.read().split("\n")
    del f
    return lines


def get_comment(field_name, filename=CONF_FILE):
    lines = get_lines(filename)

    for line in lines:
        if line.__contains__("->"):
            key = line.split("->")[0].strip()
            if key == field_name:
                index = lines.index(line)
                if index >= 1:
                    if lines[index - 1].startswith("#"):
                        return lines[index - 1].replace("#", "").strip()
    return ''


def set_field(field_name, value, filename=CONF_FILE):
    lines = get_lines(filename)

    found = False

    for line in lines:
        if line.__contains__("->"):
            key = line.split("->")[0].strip()
            if key == field_name:
                found = True
                index = lines.index(line)
                del lines[index]
                lines.insert(index, key + "->" + value)

    if not found:
        lines.append(field_name + "->" + value)

    wf = open(filename, "wt")
    for line in lines:
        if line.strip():
            wf.write(line + "\n")
    del wf

    return found
