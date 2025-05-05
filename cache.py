import time
from dnslib import RR

class Cache:
    def __init__(self):
        self.cache = dict()

    def save_cache(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for (rtype, rname), (records, ttl) in self.cache.items():
                if time.time() < ttl:
                    for record in records:
                        f.write(f"{rtype};{str(rname)};{ttl};{record.toZone()}\n")

    def load_cache(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) != 4:
                        continue
                    rtype = int(parts[0])
                    rname = parts[1]
                    ttl = float(parts[2])
                    zone_str = parts[3]
                    if time.time() < ttl:
                        rr = RR.fromZone(zone_str)[0]
                        key = (rtype, rr.rname)
                        if key not in self.cache:
                            self.cache[key] = ([], ttl)
                        self.cache[key][0].append(rr)
        except FileNotFoundError:
            pass

    def update_cache(self, key, records, ttl):
        self.cache[key] = (records, time.time() + ttl)

    def get_cache(self, key):
        entry = self.cache.get(key)
        if not entry:
            return None
        records, ttl = entry
        if time.time() > ttl:
            del self.cache[key]
            return None
        return records