import re


class Parser:
    # returns a tuple of the HTTP method and the File Path
    @staticmethod
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
            return result_11.groups()
        elif result_client:
            return (result_client.group(1), result_client.group(2), result_client.group(3), result_client.group(5))
        else:
            return None
