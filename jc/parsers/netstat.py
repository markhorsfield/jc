"""jc - JSON CLI output utility netstat Parser

Usage:
    specify --netstat as the first argument if the piped input is coming from netstat

Example:

$ netstat | jc --netstat -p

$ netstat -lp | jc --netstat -p
"""

output = {}

class state():
    section = ''
    session = ''
    network = ''

    client_tcp_ip4 = []
    client_tcp_ip6 = []
    client_udp_ip4 = []
    client_udp_ip6 = []
    
    server_tcp_ip4 = []
    server_tcp_ip6 = []
    server_udp_ip4 = []
    server_udp_ip6 = []

def parse_line(entry):
    parsed_line = entry.split()
    print(parsed_line)

    output_line = {}

    output_line['local'] = parsed_line[3]
    output_line['foreign'] = parsed_line[4]
    # output_line['state'] = parsed_line[6]
    output_line['recvq'] = int(parsed_line[1])
    output_line['sendq'] = int(parsed_line[2])
    # output_line['pid'] = int(parsed_line[1])
    # output_line['pname'] = int(parsed_line[1])

    return output_line

def parse(data):
    cleandata = data.splitlines()

    for line in cleandata:
        if line.find('Active Internet connections (w/o servers)') == 0:
            state.section = "client"
            continue

        if line.find('Active Internet connections (only servers)') == 0:
            state.section = "server"
            continue
        
        if line.find('Proto') == 0:
            continue

        if line.find('Active UNIX') == 0:
            break
        
        if state.section == "client":
            if line.find('tcp') == 0:
                state.session = 'tcp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'
            elif line.find('udp') == 0:
                state.session = 'udp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'

        if state.section == "server":
            if line.find('tcp') == 0:
                state.session = 'tcp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'
            elif line.find('udp') == 0:
                state.session = 'udp'
                if line.find('p6') == 2:
                    state.network = 'ipv6'
                else:
                    state.network = 'ipv4'

        if state.section == 'client' and state.session == 'tcp' and state.network == 'ipv4':
            state.client_tcp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'tcp' and state.network == 'ipv6':
            state.client_tcp_ip6.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv4':
            state.client_udp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv6':
            state.client_udp_ip6.append(parse_line(line))


        if state.section == 'server' and state.session == 'tcp' and state.network == 'ipv4':
            state.server_tcp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'tcp' and state.network == 'ipv6':
            state.server_tcp_ip6.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv4':
            state.server_udp_ip4.append(parse_line(line))

        if state.section == 'client' and state.session == 'udp' and state.network == 'ipv6':
            state.server_udp_ip6.append(parse_line(line))

    # build dictionary
    if state.client_tcp_ip4:
        if 'client' not in output:
            output['client'] = {}
        if 'tcp' not in output['client']:
            output['client']['tcp'] = {}
        output['client']['tcp']['ipv4'] = state.client_tcp_ip4

    if state.client_tcp_ip6:
        if 'client' not in output:
            output['client'] = {}
        if 'tcp' not in output['client']:
            output['client']['tcp'] = {}
        output['client']['tcp']['ipv6'] = state.client_tcp_ip6

    if state.client_udp_ip4:
        if 'client' not in output:
            output['client'] = {}
        if 'udp' not in output['client']:
            output['client']['udp'] = {}
        output['client']['udp']['ipv4'] = state.client_udp_ip4

    if state.client_udp_ip6:
        if 'client' not in output:
            output['client'] = {}
        if 'udp' not in output['client']:
            output['client']['udp'] = {}
        output['client']['udp']['ipv6'] = state.client_udp_ip6
    
    
    if state.server_tcp_ip4:
        if 'server' not in output:
            output['server'] = {}
        if 'tcp' not in output['server']:
            output['server']['tcp'] = {}
        output['server']['tcp']['ipv4'] = state.server_tcp_ip4

    if state.server_tcp_ip6:
        if 'server' not in output:
            output['server'] = {}
        if 'tcp' not in output['server']:
            output['server']['tcp'] = {}
        output['server']['tcp']['ipv6'] = state.server_tcp_ip6

    if state.server_udp_ip4:
        if 'server' not in output:
            output['server'] = {}
        if 'udp' not in output['server']:
            output['server']['udp'] = {}
        output['server']['udp']['ipv4'] = state.server_udp_ip4
    
    if state.server_udp_ip6:
        if 'server' not in output:
            output['server'] = {}
        if 'udp' not in output['server']:
            output['server']['udp'] = {}
        output['server']['udp']['ipv6'] = state.server_udp_ip6

    return output