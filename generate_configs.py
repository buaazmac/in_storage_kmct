import xml.etree.ElementTree as ET
import sys

workload_file = sys.argv[1]

tree = ET.parse(workload_file)
root = tree.getroot()

workloads = ["balbisiana", "crassa", "gallus", "thaliana", "vesca"]

methods = ["heu1", "RR", "rand"]

archs = ["8chan_4chip", "32chan_4chip", "8chan_16chip"]

phases = ["phase1"]

tags = ["1.0"]

for tag in tags:
    for workload in workloads:
        for method in methods:
            for arch in archs:
                if arch == "8chan_4chip":
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Channel_IDs')
                    sh.text = '0,1,2,3,4,5,6,7'
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Chip_IDs')
                    sh.text = '0,1,2,3'
                elif arch == "32chan_4chip":
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Channel_IDs')
                    sh.text = ','.join([str(i) for i in range(32)])
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Chip_IDs')
                    sh.text = '0,1,2,3'
                elif arch == "8chan_16chip":
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Channel_IDs')
                    sh.text = '0,1,2,3,4,5,6,7'
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('Chip_IDs')
                    sh.text = ','.join([str(i) for i in range(16)])

                for phase in phases:
                    phase_folder = 'phase_one'
                    trace_file = 'traces/trace/%s/%s/%s/%s/%s_%s_%s_%s_%s.trace' % (workload, tag, phase_folder, arch, workload, method, arch, phase, tag)
                    sh = tree.find('IO_Scenario').find('IO_Flow_Parameter_Set_Trace_Based').find('File_Path')
                    sh.text = trace_file
                    config_file = 'configs/%s_%s_%s_%s_%s.xml' % (workload, method, arch, phase, tag)
                    with open(config_file, 'wb') as f:
                        f.write(ET.tostring(root))
