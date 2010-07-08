from subprocess import PIPE

import subprocess
import re

file_regex = re.compile('\s{2}(.*?)\s+([ADHSR]*)\s+(\d+)\s+(\w{3}\s+\w{3}\s+\d{1,2}\s\d\d:\d\d:\d\d\s+\d{4})')
hostname_regex = re.compile('\s+([-A-Za-z0-9]+?)\s+<20>')

class Host:
    """Implements a generic host object for storing metadata"""

    def __init__(self, address, hostname):
        self.address = address
        self.hostname = hostname


class File:
    """Implements a generic file object for storing metadata"""

    def __init__(self, fullpath):
        self.fullpath = fullpath

    def __str__(self):
        return self.fullpath


class Share:
    """Implements a generic share object for storing metadata"""

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment


def list_hosts(workgroup):
    """Get a list of all SMB-enabled hosts in the given workgroup."""

    hosts = []
    command = ["/usr/local/bin/nmblookup", workgroup]

    process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = process.communicate(input=None)[0]

    if 'name_query failed to find name' in output:
        raise ValueError("Workgroup '%s' does not exist" % workgroup)

    for line in output.split('\n'):
        if line.endswith('<00>'):
            ip = line.split(' ')[0]
            command = ["/usr/local/bin/nmblookup", "-A", ip]
            process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE)
            listing = process.communicate(input=None)[0]
            if 'No reply from' in listing:
                hostname = None
            else:
                m = hostname_regex.search(listing)
                hostname = None
                if m:
                    hostname = m.group(1)
            hosts.append(Host(ip, hostname))
    return hosts


#TODO: Implement this as a C extension around the Samba libraries
def list_files(host, share):
    """Get a list of all files in a given share on the given host (and we mean
    ALL of the files)."""

    files = []
    command = ["/usr/local/bin/smbclient", "-N", "//%s/%s" % (host, share)]
    null = open('/dev/null', 'w')
    process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=null)
    null.close()
    output = process.communicate(input='recurse\nls *')

    if 'Error NT_STATUS_BAD_NETWORK_NAME' in output[0]:
        raise ValueError("Host %s does not exist" % host)
    elif 'tree connect failed: NT_STATUS_BAD_NETWORK_NAME' in output[0]:
        raise ValueError("Share %s does not exist on %s" % (share, host))
    elif 'tree connect failed: NT_STATUS_ACCESS_DENIED' in output[0]:
        raise ValueError("Access denied to %s on %s" % (share, host))

    current_dir = ''
    for line in output[0].split('\n'):
        if line.startswith('\\'):
            current_dir = line[1:]
            continue
        m = file_regex.match(line)
        if m and 'D' not in m.group(2):
            files.append(File(current_dir + '\\' + m.group(1)))
    return files

#TODO: This should be a C extension too
def list_shares(host):
    """Return a list of shares on the given host."""

    shares = []
    command = ["/usr/local/bin/smbclient", "-g", "-N", "-L", host]
    null = open('/dev/null', 'w')
    process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=null)
    null.close()
    output = process.communicate(input=None)[0]

    if 'Error NT_STATUS_BAD_NETWORK_NAME' in output:
        raise ValueError("Host %s does not exist" % host)

    for line in output.split('\n'):
        parts = line.split('|')
        if parts[0] == "Disk":
            shares.append(Share(parts[1], parts[2]))
    return shares
