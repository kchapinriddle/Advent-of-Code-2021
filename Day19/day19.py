# Day 19: Beacon Scanner

# Parts 1,2
# Problem Summary: 

# Approach: Sort beacons by first coordinate, then second, then third
# Compare offsets to detect equivalencies
# Overcome random orientation by trying all 24 orientations for other beacon - brute force works!

# TODO: write code to rotate a scanner
# TODO: write code to check two scanners against each other

def offset(b1, b2):
    return [b1[0]-b2[0],b1[1]-b2[1],b1[2]-b2[2]]

class scanr:
    def __init__(self):
        self.axes = None
        self.beacons = []
    
    def add_beacon(self, beacon):
        self.beacons.append(beacon)
    
    def reorder(self):
        self.beacons.sort()
    
    def try_match(self, other):
        index_matches = set()
        self.reorder()
        other.reorder()
        # For each pair of beacons in self, and each pair of beacons in other
        # compare the offsets. If they match, both beacons are assumed to be the same
        # TODO: Optimize for speed? Probably room.
        for si in range(len(self.beacons)):
            for sj in range(si+1,len(self.beacons)):
                for oi in range(len(other.beacons)):
                    for oj in range(oi+1,len(other.beacons)):
                        if offset(self.beacons[si],self.beacons[sj]) == offset(other.beacons[oi],other.beacons[oj]):
                            index_matches.add(str(si)+','+str(oi))
                            index_matches.add(str(sj)+','+str(oj))
        if len(index_matches) >= 12:
            print("MATCH") # TODO: Logic for successful match
    
    def rotate_X(self): # With axes as [x,y,z], rotate 90 degrees around X
        for b in self.beacons:
            b[0],b[1],b[2] = b[0],b[2],-b[1]
    
    def rotate_Y(self): # With axes as [x,y,z], rotate 90 degrees around Y
        for b in self.beacons:
            b[0],b[1],b[2] = b[2], b[1], -b[0]
    
    def rotate_Z(self): # With axes as [x,y,z], rotate 90 degrees around Z
        for b in self.beacons:
            b[0],b[1],b[2] = b[1],-b[0],b[2]
    
    # Call self.try_match(other) once for each rotation of other
    def try_rotations(self, other):
        for i in range(4):
            other.rotate_Z()
            for j in range(4):
                other.rotate_X()
                self.try_match(other)
        other.rotate_Y()
        for i in range(4):
            other.rotate_X()
            self.try_match(other)
        other.rotate_Y()
        other.rotate_Y()
        for i in range(4):
            other.rotate_X()
            self.try_match(other)
    

with open("input") as f:
    # First, read in all scanners and their beacons
    scanners = []
    cur_scan = scanr()
    for line in f.readlines():
        l = line.strip()
        if l == "": # Blank line indicates end of current scanner
            cur_scan.reorder()
            scanners.append(cur_scan)
        elif l[1] == '-': # Indicates beginning of new scanner
            cur_scan = scanr()
        else: # Otherwise it's a beacon coordinate set
            l = l.split(',')
            beac = [int(l[0]),int(l[1]),int(l[2])]
            cur_scan.add_beacon(beac)
    if not cur_scan in scanners:
        cur_scan.reorder()
        scanners.append(cur_scan)
    scanners[0].try_rotations(scanners[1])

input("Enter to exit")