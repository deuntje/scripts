#!/usr/bin/python3

import dns
import dns.name
import dns.query
import dns.resolver
import sys

#resolvers = {'google': '8.8.8.8', 'ns1': '212.115.192.193', 'ns2': '62.238.255.69', 'ns3': '212.115.192.100', 'new-ns': '212.115.192.112', 'opendns': '208.67.222.222', 'verisign': '64.6.64.6', 'localhost': '127.0.0.1'}
resolvers = {'ns1': '212.115.192.193', 'ns2': '62.238.255.69', 'ns3': '212.115.192.100', 'localhost': '127.0.0.1'}

if len(sys.argv) > 1:
	domains2check = open(sys.argv[1]).readlines()
else:
	domains2check = open("domains/domains.txt").readlines()
domains2check = [dm.replace('\n', '') for dm in domains2check]
hprinted = 0

for domain in domains2check:
    results = {}
    for resolver in resolvers:
        r = dns.resolver.Resolver(configure=False)
        r.nameservers = [resolvers[resolver]]
        r.cache = 0
        r.timeout = 1

        d = dns.name.from_text(domain)

        try:
            answer = r.query(d, "A")
            results[resolver] = dns.rcode.to_text(answer.response.rcode())

        except dns.exception.Timeout:
            results[resolver] = 'TIMEOUT'
            pass
        except dns.resolver.NoAnswer:
            results[resolver] = 'NOANSWER'
            pass
        except dns.resolver.NXDOMAIN:
            results[resolver] = 'NXDOMAIN'
            pass
        except dns.resolver.NoNameservers:
            results[resolver] = 'NONSSERVER'
            pass
        except:
            raise

    tmp = ('%-125s' % domain)
    header = ('%-125s' % "")
    for res in results:
        tmp += ('%-14s' % results[res])
        header += ('%-14s' % res)
    if hprinted == 0:
        print(header)
    hprinted += 1
    if hprinted == 50:
        hprinted = 0
    print(tmp)
