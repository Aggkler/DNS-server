from cache import Cache
from dnslib import DNSRecord, RCODE

TRUST_SERVER = "77.88.8.1"


class DNS:
    def __init__(self):
        self.cache = Cache()
        self.cache.load_cache("cache.txt")

    def process(self, query_data):
        try:
            query = DNSRecord.parse(query_data)
            query_key = (query.q.qtype, query.q.qname)

            rdata = self.cache.get_cache(query_key)
            if rdata:
                response = DNSRecord(header=query.header)
                response.add_question(query.q)
                response.rr.extend(rdata)
                print(f"Найдено в кэше:\n{response}\n")
                return response.pack()

            response_data = query.send(TRUST_SERVER, 53, timeout=5)
            response = DNSRecord.parse(response_data)

            if response.header.rcode == RCODE.NOERROR:
                for section in (response.rr, response.auth, response.ar):
                    for rr in section:
                        key = (rr.rtype, rr.rname)
                        self.cache.update_cache(key, [rr], rr.ttl)
            self.cache.save_cache("cache.txt")
            return response.pack()

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return None