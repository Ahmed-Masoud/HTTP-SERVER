import re
from collections import namedtuple

HTTP_Variables = namedtuple('HTTP_Variables', ['request_type', 'method', 'file_path', 'host', 'port'])


# returns a named tuple of the HTTP Variables
def http(req):
    http11_regex = re.compile(r'(GET|POST|UPDATE|DELETE)\s+(/.*)\s+HTTP/1\.1')
    client_regex = re.compile(r'''
                                (GET|POST)\s+ #method
                                (/.*)\s+ #filepath
                                (([0-9]{1,3}\.){3}[0-9]{1,3})\s+ #host name
                                \(([0-9]+)\) #portnumber
                              ''', re.VERBOSE)
    result_11 = http11_regex.search(req)
    result_client = client_regex.search(req)
    if result_11:
        return HTTP_Variables('1.1', result_11.group(1), result_11.group(2), None, None)
    elif result_client:
        return HTTP_Variables('1.0', result_client.group(1), result_client.group(2),
                              result_client.group(3), result_client.group(5))
    else:
        return None
