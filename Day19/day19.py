# Day 19: Beacon Scanner

# Parts 1,2
# Problem Summary: 

# Approach: Sort beacons by first coordinate, then second, then third
# Compare offsets to detect equivalencies
# Overcome random orientation by trying all 24 orientations for other beacon - brute force works!

def offset(b1, b2):
    return [b1[0]-b2[0],b1[1]-b2[1],b1[2]-b2[2]]

ids = 0

class scanr:
    def __init__(self):
        global ids
        self.idcode = ids
        ids += 1
        self.axes = None
        self.beacons = []
        self.offset = [0,0,0]
        self.parent = None
        self.checked_against = set()
    
    def add_beacon(self, beacon):
        self.beacons.append(beacon)
    
    def reorder(self):
        self.beacons.sort()
    
    # Slaves "self" to "other, setting offset as appropriate
    def apply_match(self, other, index_matches):
        match = list(index_matches)[0].split(',')
        match = [int(match[0]),int(match[1])]
        # Set relative offset, then adjust based on parent's offset
        self.offset = offset(other.beacons[match[0]],self.beacons[match[1]])
        for i in range(3):
            self.offset[i] += other.offset[i]
        self.parent = other
    
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
            other.apply_match(self,index_matches)
            return True
        return False
    
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
        if self.idcode in other.checked_against:
            return False #Already tried this one!
        other.checked_against.add(self.idcode)
        for i in range(4):
            other.rotate_Z()
            for j in range(4):
                other.rotate_X()
                if self.try_match(other):
                    return True
        other.rotate_Y()
        for i in range(4):
            other.rotate_X()
            if self.try_match(other):
                return True
        other.rotate_Y()
        other.rotate_Y()
        for i in range(4):
            other.rotate_X()
            if self.try_match(other):
                return True
        return False
    
    # Add own beacons to set of all beacons relative to scanner 0
    def add_global_beacons(self, global_beacons):
        for b in self.beacons:
            b_txt = str(b[0]+self.offset[0])+','+str(b[1]+self.offset[1])+','+str(b[2]+self.offset[2])
            global_beacons.add(b_txt)
    
    

with open("input") as f:
    # First, read in all scanners and their beacons
    scanners = []
    cur_scan = None
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
    scanners[0].parent = scanners[0] #The very first scanner is the objective coordinate source, and never gets matched to anything
    
    parented = []
    unparented = []
    for s in scanners:
        if s.parent == None:
            unparented.append(s)
        else:
            parented.append(s)
    while len(unparented) > 0:
        up = unparented.pop(0)
        for p in parented:
            p.try_rotations(up)
            if up.parent != None:
                print(p.idcode,up.idcode)
                parented.append(up)
                break
        else:
            unparented.append(up)
            print("No parent for",up.idcode,"tried",len(up.checked_against))
            
    global_beacons = set()
    for s in scanners:
        if s.parent == None:
            print("Scanner",s.idcode,"has no parent!")
        s.add_global_beacons(global_beacons)
    print("Part 1:",len(global_beacons))
    
    maxdist = 0
    for s in scanners:
        for ss in scanners:
            x = abs(s.offset[0]-ss.offset[0])
            y = abs(s.offset[1]-ss.offset[1])
            z = abs(s.offset[2]-ss.offset[2])
            maxdist = max(maxdist, sum([x,y,z]))
    print("Part 2:",maxdist)

input("Enter to exit")