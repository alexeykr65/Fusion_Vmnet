#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Configure S-Terra
#
# alexeykr@gmail.com
# coding=utf-8
# import codecs

"""
Configure Vmnet Networks using Vmware Fusion v1.0
"""
import os
from netaddr import IPNetwork
import re
import argparse
from termcolor import colored
# ipdb.set_trace()


def check_argument_parser():
    description_argument_parser = ""
    epilog_argument_parser = ""
    parser = argparse.ArgumentParser(description=description_argument_parser, epilog=epilog_argument_parser)
    parser.add_argument('-a', '--add_net', help='Add VMNET Interfaces ', dest="add_net", default='')
    parser.add_argument('-r', '--rem_net', help='Remove VMNET Interfaces', dest="rem_net", default='')
    parser.add_argument('-rr', '--rem_net_range', help='Remove Range VMNET Interfaces', dest="rem_net_range", default='')
    parser.add_argument('-s', '--service_restart', help='Restart Fusion networking service ', dest="service_restart", action="store_true")
    return parser.parse_args()


def run_cmd(cmds):
    for cmd in cmds:
        print(cmd)
        os.system(cmd)


def remove_interfaces(cmd_rm, num_int):
    vm_net_file = f'/Library/Preferences/VMware Fusion/networking'
    cmd_net_rem = list()
    with open(vm_net_file) as fl:
        for line in fl:
            if re.search(f'VNET_{num_int}', line):
                re_pattern = r'answer\s+(.*)'
                res = re.match(re_pattern, line)
                if res:
                    cmd_net_rem.append(f'{cmd_rm} vnetcfgremove {res[1]}')
    run_cmd(cmd_net_rem)


def add_interfaces(cmd_run, cfg_file):
    vm_net_cfg = list()
    cmd_net_cfg_load = list()
    with open(cfg_file) as fs:
        for f in fs:
            vm_net_cfg.append(f.split(';'))

    # print(vm_net_cfg)
    for net_cfg in vm_net_cfg:
        vm_num = net_cfg[0]
        vm_netmask = net_cfg[3]
        vm_subnet = net_cfg[2]
        vm_adapter_addr = net_cfg[4]

        cmd_net_cfg_load.append(f'{cmd_run} vnetcfgadd VNET_{vm_num}_VIRTUAL_ADAPTER yes')
        cmd_net_cfg_load.append(f'{cmd_run} vnetcfgadd VNET_{vm_num}_HOSTONLY_NETMASK {vm_netmask}')
        cmd_net_cfg_load.append(f'{cmd_run} vnetcfgadd VNET_{vm_num}_HOSTONLY_SUBNET {vm_subnet}')
        cmd_net_cfg_load.append(f'{cmd_run} vnetcfgadd VNET_{vm_num}_VIRTUAL_ADAPTER_ADDR {vm_adapter_addr}')
    run_cmd(cmd_net_cfg_load)


if __name__ == "__main__":
    cmd_vmnet_cfgcli = r'sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cfgcli'
    arg = check_argument_parser()
    vmnet_restart = [
        r'sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --configure',
        r'sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --stop',
        r'sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --start'
    ]
    if arg.rem_net_range:
        for nm in range(10, int(arg.rem_net_range)):
            remove_interfaces(cmd_vmnet_cfgcli, nm)
    if arg.rem_net:
        for nm in arg.rem_net.split(','):
            remove_interfaces(cmd_vmnet_cfgcli, nm)
    if arg.add_net:
        add_interfaces(cmd_vmnet_cfgcli, arg.add_net)
    if arg.service_restart:
        run_cmd(vmnet_restart)

    exit(0)
