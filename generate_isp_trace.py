import xml.etree.ElementTree as ET

tree = ET.parse('ssdconfig.xml')
root = tree.getroot()

class Trace:
    def __init__(self, time, level, lsa, size, type):
        self.time = time
        self.level = level
        self.lsa = lsa
        self.size = size
        self.type = type
    
    def get_str(self):
        return "%d %d %d %d %d" % (self.time, self.level, self.lsa, self.size, self.type)

device_para_node = root.find('Device_Parameter_Set')
n_channels = int(device_para_node.find('Flash_Channel_Count').text)
n_chips_per_channel = int(device_para_node.find('Chip_No_Per_Channel').text)

flash_para_node = device_para_node.find('Flash_Parameter_Set')
n_dies_per_chip = int(flash_para_node.find('Die_No_Per_Chip').text)
n_planes_per_die = int(flash_para_node.find('Plane_No_Per_Die').text)
n_blocks_per_plane = int(flash_para_node.find('Block_No_Per_Plane').text)
n_pages_per_block = int(flash_para_node.find('Page_No_Per_Block').text)
page_capacity = int(flash_para_node.find('Page_Capacity').text)

n_pages_per_channel = n_pages_per_block * n_blocks_per_plane * n_planes_per_die * n_dies_per_chip * n_chips_per_channel
print(n_pages_per_channel)

sector_size = 512
n_sectors_per_page = page_capacity / sector_size

print(n_sectors_per_page)

# The key is to generate logical sector addresses (LSAs) for k-mer operation (trace)
k_ = 21
read_len_ = 8 * 1024 * 1024
s_ = 10

# Some ISP configs
pe_level = "chip"

n_chips = n_channels * n_chips_per_channel

sector_size_in_byte = 512

# trace generation
traces = []

# Phase 1: super-mer generation
start_time = 0
read_per_chip = read_len_ / n_chips
n_batches = 1
for batch in range(n_batches):
    for channel in range(n_channels):
        for chip in range(n_chips_per_channel):
            if pe_level == "channel":
                chip = 0
            start_lsa = channel * n_chips_per_channel * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page \
                        + chip * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 2)
            traces.append(trace)
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 1)
            traces.append(trace)
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 0)
            traces.append(trace)
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 3)
            traces.append(trace)
            # with open('./traces/isp-test.trace', 'w') as f:
            #     for trace in traces:
            #         f.write(trace.get_str() + "\n")
            # exit()

# Phase 2: kmer counting
n_batches = 1
for batch in range(n_batches):
    for channel in range(n_channels):
        for chip in range(n_chips_per_channel):
            if pe_level == "channel":
                chip = 0
            start_lsa = channel * n_chips_per_channel * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page \
                        + chip * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 2)
            traces.append(trace)
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 1)
            traces.append(trace)
            trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 0)
            traces.append(trace)
            # trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 0)
            # traces.append(trace)

with open('./traces/isp-test.trace', 'w') as f:
    for trace in traces:
        f.write(trace.get_str() + "\n")