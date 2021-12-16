# Day 16: Packet Decoder

# Parts 1,2
# Problem Summary: Decode packets, converting first from hex to bin then parsing
# Parsing rules not elegantly summarizeable. See problem statement text files.

version_sum = 0
debug = 0

def parse_literal_packet(data):
    if debug:
        print("Literal packet", data)
    version = data[slice(3)]
    global version_sum
    version_sum += int(version,2)
    typeID = data[slice(3,6)]
    packet_length = 6
    value = ''
    index = 6
    while True:
        packet_length += 5
        workdata = data[slice(index,index+5)] # Get next five bits
        value += workdata[slice(1,5)] # Leading bit ignored, but next four bits are data
        if workdata[0] == '1': # Leading bit of 1 indicates further data
            index += 5
        else:
            break
    return int(value,2), packet_length

def parse_operator_packet(data):
    if debug:
        print("Operator packet", data)
    version = data[slice(3)]
    global version_sum
    version_sum += int(version,2)
    typeID = data[slice(3,6)]
    lengthID = data[6]
    packet_length = 7
    subpacket_values = []
    if lengthID == '0': # Then next 15 bits indicate bitlength of subpackets
        packet_length += 15
        content_length = int(data[slice(7,7+15)],2)
        total_packet_length = packet_length + content_length
        # Repeatedly parse packets until total length matches
        while packet_length != total_packet_length:
            result = parse_packet(data[slice(packet_length,total_packet_length)])
            packet_length += result[1] # Add length of parsed packet
            subpacket_values.append(result[0])
    else: # lengthID == '1', next 11 bits contain number of subpackets contained after this
        packet_length += 11
        content_length = int(data[slice(7,7+11)],2)
        for i in range(content_length): # Parse the indicated number of packets
            result = parse_packet(data[slice(packet_length,len(data))])
            packet_length += result[1] # Add length of parsed packet
            subpacket_values.append(result[0])
    # Now perform operation as per typeID
    result = -1
    if int(typeID,2) == 0: # Sum packet
        result = sum(subpacket_values)
    elif int(typeID,2) == 1: # Product packet
        result = 1
        for i in subpacket_values:
            result *= i
    elif int(typeID,2) == 2: # Minimum packet
        result = min(subpacket_values)
    elif int(typeID,2) == 3: # Maximum packet
        result = max(subpacket_values)
    elif int(typeID,2) == 5: # Greater than packet
        if subpacket_values[0] > subpacket_values[1]:
            result = 1
        else:
            result = 0
    elif int(typeID,2) == 6: # Less than packet
        if subpacket_values[0] < subpacket_values[1]:
            result = 1
        else:
            result = 0
    elif int(typeID,2) == 7: # Equal to packet
        if subpacket_values[0] == subpacket_values[1]:
            result = 1
        else:
            result = 0
    return result, packet_length # TODO probably part 2: What is proper first return value?
    

def parse_packet(data):
    version = data[slice(3)]
    typeID = data[slice(3,6)]
    if int(typeID,2) == 4: # Type ID 4 means literal value
        return parse_literal_packet(data)
    else:
        return parse_operator_packet(data)

with open("input") as f:
    for line in f.readlines():
        raw = line.strip()
        version_sum = 0
        data = bin(int(raw,16)).split('b')[1] #May drop leading zeros, so
        data = "0"*(len(raw)*4 - len(data)) + data
        print("Evaluating packet: ",raw)
        result = parse_packet(data)
        print("Part 1:",version_sum)
        print("Part 2:",result[0])

input("Enter to exit")