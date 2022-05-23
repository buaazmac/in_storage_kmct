import xml.etree.ElementTree as ET
import sys

ssdconfig = sys.argv[1]
kc_workload = sys.argv[2]

tree = ET.parse(ssdconfig)
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
workload_config = {}
with open(kc_workload) as f:
    for line in f:
        if line[0] == '#':
            continue
        line_data = line.strip().split(' = ')
        workload_config[line_data[0]] = int(line_data[1])
    
read_len_ = workload_config['read_size'] * 1024 * 1024
n_reader = workload_config['n_readers']
n_page_reads_per_merge = workload_config['n_page_reads_per_merge']
n_smer = workload_config['n_smer']
n_merges_per_write = workload_config['n_merges_per_write']
n_writes_per_migration = workload_config['n_writes_per_migration']
n_counts_per_merge = workload_config['n_counts_per_merge']

# Some ISP configs
pe_level = "chip"

n_chips = n_channels * n_chips_per_channel

sector_size_in_byte = 512

# trace generation
traces = []

# Phase 1: super-mer generation
start_time = 0
read_per_chip = int(read_len_ / n_chips)
n_batches = int(read_per_chip / page_capacity)
combine_factor = 128
if page_capacity * combine_factor > read_per_chip:
    combine_factor = n_batches
print("read_per_chip", read_per_chip, ", n_batches", n_batches)
merge_batches = []
write_batches = []
count_batches = []
for channel in range(n_channels):
    merge_batches.append([])
    write_batches.append([])
    count_batches.append([])
    for chip in range(n_chips_per_channel):
        merge_batches[channel].append({})
        write_batches[channel].append({})
        count_batches[channel].append({})
        for batch in range(n_batches):
            if batch != 0 and batch % n_page_reads_per_merge == 0:
                # if channel == 0 and chip == 0:
                #     print(batch, n_page_reads_per_merge, batch % n_page_reads_per_merge)
                merge_batches[channel][chip][batch] = page_capacity
                idx = batch / n_page_reads_per_merge
                if idx != 0 and idx % n_merges_per_write == 0:
                    write_batches[channel][chip][batch] = page_capacity

            if batch != 0 and batch % n_counts_per_merge == 0:
                count_batches[channel][chip][batch] = page_capacity
        # print(channel, chip, merge_batches[channel][chip])
        # print(channel, chip, write_batches[channel][chip])

        
for batch in range(int(n_batches / combine_factor)):
    for channel in range(n_channels):
        for chip in range(n_chips_per_channel):
            
            if pe_level == "channel":
                chip = 0
            start_lsa = channel * n_chips_per_channel * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page \
                        + chip * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page
            trace = Trace(start_time, 2, start_lsa, page_capacity / sector_size_in_byte * combine_factor, 1)
            traces.append(trace)

            print(channel,chip,int(start_lsa))
            # if batch in merge_batches[channel][chip]:
            #     trace = Trace(start_time, 2, start_lsa, page_capacity / sector_size_in_byte * combine_factor, 0)
            #     traces.append(trace)
            # if batch in write_batches[channel][chip]:
            #     trace = Trace(start_time, 2, start_lsa, write_batches[channel][chip][batch] / sector_size_in_byte, 0)
            #     traces.append(trace)
    start_time += 75000
exit()
with open('./traces/isp-test-phase1.trace', 'w') as f:
    for trace in traces:
        f.write(trace.get_str() + "\n")

traces = []

# Phase 2: kmer counting
# n_batches = 16
for batch in range(n_batches):
    for channel in range(n_channels):
        for chip in range(n_chips_per_channel):
            if pe_level == "channel":
                chip = 0
            start_lsa = channel * n_chips_per_channel * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page \
                        + chip * n_dies_per_chip * n_planes_per_die * n_blocks_per_plane * n_pages_per_block * n_sectors_per_page
            trace = Trace(start_time, 2, start_lsa, page_capacity / sector_size_in_byte, 2)
            traces.append(trace)
            if batch in count_batches[channel][chip]:
                trace = Trace(start_time, 2, start_lsa, count_batches[channel][chip][batch] / sector_size_in_byte, 1)
                traces.append(trace)
            # trace = Trace(start_time, 2, start_lsa, read_per_chip / n_batches / sector_size_in_byte, 0)
            # traces.append(trace)
with open('./traces/isp-test-phase2.trace', 'w') as f:
    for trace in traces:
        f.write(trace.get_str() + "\n")
