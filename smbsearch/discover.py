from subprocess import PIPE

import subprocess
import re

file_regex = re.compile('\s{2}(.*?)\s+([ADHSR]*)\s+(\d+)\s+(\w{3}\s+\w{3}\s+\d{1,2}\s\d\d:\d\d:\d\d\s+\d{4})')

class File:
    """Implements a generic file object for storing metadata"""

    def __init__(self, fullpath):
        self.fullpath = fullpath

    def __str__(self):
        return self.fullpath

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
