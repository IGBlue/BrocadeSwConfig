#
#   Program: FabricAnal.py
#
#   Author: Ian Gray
#   Contact: iangray100@gmail.com
#
# This program takes the consolidated output from a Brocade nsshow command and extracts relevant information
# suitable for input into the Fabric or Fabricxl programs. See operational notes regarding manual modification
# of captured NSSHOW output.
#
# The output from this program is a CSV file which can be used for analysis and then used as input to
# the Bfabric programs to generate zoning commands.
#
#   Versions
#     1   17/03/2020 - amendments to handle non printing characters and short lines better
#
#     2   11/06/2020 - port information block terminator changed to "Device link speed"
#
# import pdb                            # pdb.set_trace()
import os                               # Allows for file validation

nsfile = ""                             # Input file location
outline = ""                            # Base value for output line

fabric = ''                             # Fabric identifier
portsymb = ',""'                         # Hint of remote port id (PortSymb)
nodesymb = ',""'                         # Hint of remote device type (NodeSymb)
devwwid = ',""'                          # Remote wwid on this port (Fabric Port Name)
swwwid = ',""'                           # Local switch port wwid (Permanent Port Name)
initgt = ',""'                           # Initiator or target
portx = ',""'                            # Port number on switch (Port Index)

while True:
    folder = input("Enter the working directory: ")         # Directory for CSV file and output files
    if folder == "":                                        # Exit if no input
        exit(1)
    if os.path.isdir(folder):                               # Check only directory name specified
        break
    else:
        print("Folder/directory not valid or filename specified - " + folder)
        print("")

while True:
    nsfile = input("NSSHOW filename in " + folder + ": ")     # CSV filename request
    if nsfile == "":                                       # Exit if no input
        exit(1)
    infile = folder + "\\" + nsfile  # Input file is directory + filename

    if os.path.isfile(infile):                              # Check file exists
        break
    else:
        print("Invalid filename or does not exist - " + infile)
        print("")

outfile = folder + "\\fabanal.csv"
outf = open(outfile, "w")
outf.write("Node,I/f,Subif,Fabric,I/T,WWPN,WWNN,Node Type,Node Id,SWport Index\n")


with open(infile) as inf:

    for inline in inf:                      # Get a line from file
        if len(inline) < 6:                 # Bypass funny characters and unwanted lines
            continue
        # There appears to be a situation where leading characters are non printing.
        # Ignore any leading characters below/above ASCII blank/lower case z
        while inline[0:1] < " " or inline[0:1] > "z":
            inline = inline[1:]
            
        inline = inline.strip()             # Strip leading/training spaces
        inline = " ".join(inline.split())   # And multiple embedded spaces
        
        if inline[0:9] == "Fabric A:" or inline[0:9] == "Fabric B:":    # Look for Fabric identifier
            fabric = ",,," + inline[7:8]
               
        elif inline[0:2] == "N ":           # First line of each port entry has WWPN
            devwwidlist = list(inline.split(";"))
            devwwid = "," + devwwidlist[2]

        elif inline[0:9] == "PortSymb:":    # Look for PortSymb: string
            portsymb = inline.split('"')
            portsymb = ',"' + portsymb[1] + '"'

        elif inline[0:9] == "NodeSymb:":     # Look for NodeSymb: string
            nodesymb = inline.split('"')
            nodesymb = ',"' + nodesymb[1] + '"'

        elif inline[0:12] == "Device type:":    # Initiator or Target type
            initgt = "," + inline[22:23]

        elif inline[0:11] == "Port Index:":  # Switch port (zero relative)
            portx = "," + inline[12:]

        elif inline[0:17] == "Device link speed":         # There is nothing more for this port so write values
            outline = fabric + initgt + devwwid + "," + nodesymb + portsymb + portx + "\n"
            outf.write(outline)

            outline = ',""'   # Base value for output line
            portsymb = ',""'  # Hint of remote port id (PortSymb)
            nodesymb = ',""'  # Hint of remote device type (NodeSymb)
            devwwid = ',""'   # Remote wwid on this port (Fabric Port Name)
            initgt = ',""'    # Initiator or target
            portx = ',""'     # Port number on switch (Port Index)

outf.close()
inf.close()
