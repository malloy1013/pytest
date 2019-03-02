#!/usr/bin/env python3
import os
# import args
import parsing
import progressbar
import display
import interface_type
import checks
import graph
import harvester
from checks import *
import json
cwdpath = os.path.dirname(__file__)

def parse_cisco(filename):

    check_disabled = False


    dict_for_drawing_plot = {}

    config_name = ''


    parsing.parseconfigs(filename, check_disabled)


    global_params = parsing.iface_global
    interfaces = parsing.iface_local
    result_dict = {}

    # global checks
    result_dict.update(checks.services.check(global_params))
    # result_dict.update(checks.users.check(global_params))
    result_dict.update(checks.ip_global.check(global_params))
    result_dict.update(checks.console_vty.check(global_params))
    result_dict.update(checks.lldp.check(global_params))
    result_dict.update(checks.aaa.check(global_params))

    result_cdp, cdp_flag = checks.cdp.global_check(global_params)
    if result_cdp:
        result_dict.update(result_cdp)

    result_vtp = checks.vtp.check(global_params)
    if result_vtp:
        result_dict.update(result_vtp)

    # global checks with necessary flags for further interface checks
    result, bpdu_flag = checks.stp.global_check(global_params)
    result_dict.update(result)

    result_arp, arp_flag = checks.arp_inspection.check_global(global_params, result_dict)
    result_dict.update(result_arp)

    result_dhcp, dhcp_flag = checks.dhcp_snooping.check_global(global_params, result_dict)
    result_dict.update(result_dhcp)

    result_dict['IPv6 options'] = {}

    result_raguard, raguard_flag = checks.ipv6.raguard_global(global_params, result_dict)
    result_dict.update(result_raguard)

    result_snooping, snooping_flag = checks.ipv6.snooping_global(global_params, result_dict)
    result_dict.update(result_snooping)

    result_sourceguard, sourceguard_flag = checks.ipv6.sourceguard_global(global_params, result_dict)
    result_dict.update(result_sourceguard)

    result_dhcpguard, dhcpguard_flag = checks.ipv6.dhcpguard_global(global_params, result_dict)
    result_dict.update(result_dhcpguard)

    result_destinationguard, destinationguard_flag = checks.ipv6.destinationguard_global(global_params, result_dict)
    result_dict.update(result_destinationguard)

    arp_proxy_flag, arp_proxy = checks.arp_proxy.global_check(global_params)

    if arp_proxy_flag:
        result_dict.update(arp_proxy)

    # Adding device name to dictionary
    dict_for_drawing_plot.update({config_name: {}})

    # interface checks
    for iface in interfaces:

        # check interface if it has at least 1 options
        if 'unknown_iface' not in interfaces[iface]:

            # skip loopback and vlan interfaces
            if 'loop' not in iface.lower() and 'vlan' not in iface.lower():

                # skip shutdown interfaces if there was not --disabled-interfaces argument
                if interfaces[iface]['shutdown'] == 'yes' and not check_disabled:
                    continue

                # If an interface has any vlans - it is added to dictionary for graph
                if interfaces[iface]['vlans']:
                    dict_for_drawing_plot[config_name].update({iface: interfaces[iface]['vlans']})

                result_dict[iface] = {}

                # set DISABLE status if interface is shutdown and disabled-interfaces argument is true
                if interfaces[iface]['shutdown'] == 'yes' and check_disabled:
                    result_dict[iface]['status'] = [3, 'SHUTDOWN']

                # If type is not defined - interface is working in Dynamic Auto mode
                if 'type' not in interfaces[iface]:
                    result_dict[iface]['mode'] = [0, 'DYNAMIC',
                                                  'The interfaces of your switches must be in trunk or access mode.']


                vlanmap_result = None

                # access/trunk mode check
                result_dict[iface].update(checks.mode.check(interfaces[iface]))

                # check cdp, dtp, mop and source guard options on current interface
                result_dict[iface].update(checks.dtp.check(global_params, interfaces[iface], vlanmap_result))
                result_dict[iface].update(checks.mop.check(interfaces[iface], vlanmap_result, iface))
                result_dict[iface].update(checks.source_guard.check(interfaces[iface], dhcp_flag, vlanmap_result))

                cdp_result = checks.cdp.iface_check(interfaces[iface], vlanmap_result, cdp_flag)
                if cdp_result:
                    result_dict[iface].update(cdp_result)

                stp_result = checks.stp.iface_check(interfaces[iface], bpdu_flag, vlanmap_result)

                if stp_result:
                    result_dict[iface].update(stp_result)

                dhcp_result = checks.dhcp_snooping.check_iface(interfaces[iface], vlanmap_result,
                                                               None, dhcp_flag)

                if dhcp_result:
                    result_dict[iface].update(dhcp_result)

                if arp_proxy_flag == 0:
                    arp_proxy_result = checks.arp_proxy.iface_check(interfaces[iface], vlanmap_result)
                    result_dict[iface].update(arp_proxy_result)

                arp_result = checks.arp_inspection.check_iface(interfaces[iface], vlanmap_result,
                                                               None,
                                                               arp_flag)
                if arp_result:
                    result_dict[iface].update(arp_result)
                result_dict[iface]['IPv6'] = {}
                sourceguard_result = checks.ipv6.sourceguard_iface(interfaces[iface], vlanmap_result,
                                                                   None, sourceguard_flag)
                if sourceguard_result:
                    result_dict[iface]['IPv6'].update(sourceguard_result)
                raguard_result = checks.ipv6.raguard_iface(interfaces[iface], vlanmap_result,
                                                           None, raguard_flag)
                if raguard_result:
                    result_dict[iface]['IPv6'].update(raguard_result)
                destinationguard_result = checks.ipv6.destinationguard_iface(interfaces[iface], vlanmap_result,
                                                                             None,
                                                                             destinationguard_flag)
                if destinationguard_result:
                    result_dict[iface]['IPv6'].update(destinationguard_result)
                dhcpguard_result = checks.ipv6.dhcpguard_iface(interfaces[iface], vlanmap_result,
                                                               None, dhcpguard_flag)
                if dhcpguard_result:
                    result_dict[iface]['IPv6'].update(dhcpguard_result)


                result_dict[iface].update(checks.storm_control.check(interfaces[iface], vlanmap_result))


                port_result = checks.port_security.check(interfaces[iface], vlanmap_result)

                if port_result:
                    result_dict[iface].update(port_result)


        else:
            result_dict[iface] = {'Unused Interface': [0, 'ENABLED', 'An interface that is not used must be disabled']}


    jobj = json.dumps(result_dict, ensure_ascii=False, indent=2)
    return jobj,result_dict


