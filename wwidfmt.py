#
#   Program: WWIDfmt.py
#
#   Author: Ian Gray
#   Contact: iangray100@gmail.com
#
#  Takes an input string at a user prompt which purports to be a known format for a WWID and ensures
#  said string contains 16 hex characters plus whatever formatting characters are supplied. Note that
#  the input string can be any length but the resulting hex can only be 16 characters.
#
#  It is anticipated that the input will be supplied via a paste operation.
#
#  The program will return all known formats of the supplied WWID with the Brocade format also being
#  automatically sent to the clipboard.
#
#   Versions:
#     1   27/08/2019  Base version
#

import pyperclip                            # This is used to send result to the clipboard
#import pdb                                 # Trace routines - pdb.set_trace()

print("Colon separated strings automatically sent to the clipboard\n")

while True:                                 # Run until use input null

    hexstring = ""                          # Accumulate he characters in this variable

    userstring = input("Enter WWID to format: ")
    if userstring == "":
        exit()

    for userchar in userstring:             # Get each character in the input and isolate hex characters
        userchar = userchar.lower()         # For consistency convert to lower case
        # Only hex values 0-9 and a-f allowed
        if (userchar >= "0" and userchar <= "9") or (userchar >= "a" and userchar <= "f"):
            hexstring = hexstring + userchar    # Form an unformatted string
#
# Should now have a string of length 16. If we haven't then user input was invalid
#
#

    if len(hexstring) != 16:
        print("Input string does not contain 16 hex characters")
    else:
        #
        # Brocaade format 2 chars with colon separator
        #
        brocadefmt = hexstring[0:2] + ":" \
            + hexstring[2:4] + ":" \
            + hexstring[4:6] + ":" \
            + hexstring[6:8] + ":" \
            + hexstring[8:10] + ":" \
            + hexstring[10:12] + ":" \
            + hexstring[12:14] + ":" \
            + hexstring[14:16]
        print(brocadefmt)
        #
        pyperclip.copy(brocadefmt)          # Send to clipboard
        #
        # VMS format 4 chars with hyphen separator
        #
        print(hexstring)                    # Print unformatted string
        print(hexstring.upper())            # And with upper case hex
        #
        vmsfmt = hexstring[0:4] + "-" \
            + hexstring[4:8] + "-" \
            + hexstring[8:12] + "-" \
            + hexstring[12:16]
        print(vmsfmt)
        print ("")
