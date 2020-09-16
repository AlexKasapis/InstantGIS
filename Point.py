class Point:

    def __init__(self, lon, lat, pp, np):
        self.lon = lon
        self.lat = lat
        self.prev_point = pp
        self.next_point = np
