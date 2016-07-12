import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import re
import requests

base_url = sys.argv[0]
handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def current_server():
    f = file('/etc/resolv.conf', 'r')
    for line in f:
        ns = re.match('nameserver (.*)', line)
        if ns:
            return ns.group(1)

def write_dns(dns):
    f = file('/etc/resolv.conf', 'w')
    f.write('nameserver '+ dns + '\n')
    f.close()

mode = args.get('mode', None)

def main():
    off = (current_server() == '8.8.8.8')
    if off:
        status = xbmcgui.ListItem('Status: [COLOR red]OFF[/COLOR]')
    else:
        status = xbmcgui.ListItem('Status: [COLOR green]ON[/COLOR]')
    xbmcplugin.addDirectoryItem(handle=handle, listitem=status, url='')

    if off:
        turn_on = xbmcgui.ListItem('Turn on')
        xbmcplugin.addDirectoryItem(handle=handle,
                                    listitem=turn_on,
                                    url=build_url({'mode': 'on'}),
                                    isFolder=True)
    else:
        turn_off = xbmcgui.ListItem('Turn off')
        xbmcplugin.addDirectoryItem(handle=handle,
                                    listitem=turn_off,
                                    url=build_url({'mode': 'off'}),
                                    isFolder=True)
        activate = xbmcgui.ListItem('Activate')
        xbmcplugin.addDirectoryItem(handle=handle,
                                    listitem=activate,
                                    url=build_url({'mode': 'activate'}),
                                    isFolder=True)
    xbmcplugin.endOfDirectory(handle)

if mode is None:
    main()
elif mode[0] == 'off':
    write_dns('8.8.8.8')
    main()
elif mode[0] == 'on':
    write_dns('54.93.173.153')
    main()
elif mode[0] == 'activate':
    addon = xbmcaddon.Addon()
    api_key = addon.getSetting('api_key')
    r = requests.get('http://www.smartdnsproxy.com/api/IP/update/' + api_key)
    r.raise_for_status()
    main()
