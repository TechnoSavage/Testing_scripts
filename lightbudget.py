#Script to make light budget calculations for permitted cable lengths for a given TAP or appropriate TAP for current link

#!/usr/bin/python

from decimal import *

def menu():
    option = raw_input("""\nWhat would you like to do:
    1 - Calculate the max allowed coupler loss for inserting a TAP into a link
    2 - Calculate the max allowed cable length for a given TAP split ratio in a link
    3 - Display ethernet fiber standards and max cabling distance
    4 - Exit
    Enter your selection: """)
    if option not in ('1', '2', '3', '4'):
        print "That is not a valid input"
        menu()
    if option == '1':
        max_split()
    elif option == '2':
        max_cable()
    elif option == '3':
        ethernet_table()
    elif option == '4':
        print "Goodbye"
        exit()
    else:
        print 'Something went wrong!'
        exit()

def max_split():
    getcontext().prec = 10
    sender = Decimal(raw_input("\nwhat is the sender transmit power (dB): "))
    receiver = Decimal(raw_input("\nWhat is the receiver sensitivity (dB): "))
    link_loss_budget = sender - receiver
    print "\nThe Power Link Loss Budget for this link is %sdB" % link_loss_budget
    print """\nSingle Mode or Multi Mode fiber?
    1 - Single Mode
    2 - Multi Mode"""
    mode = raw_input("Enter the number of your selection: ")
    if mode not in ('1', '2'):
        print "That is not a valid selection"
        menu()
    connectors = Decimal(raw_input("\nHow many connectors are in the path of the link: "))
    if mode == '1':
        connector_loss = Decimal('0.2') * connectors
        mode_type = "Single Mode"
        print """\nWhat is the wavelength being used?
        1 - 1310nm
        2 - 1550nm"""
        wave = raw_input("\nEnter the number of your selection: ")
        if wave not in ('1', '2'):
            print "\nThat is not a valid selection"
            menu()
        if wave == '1':
            wavelength = 1310
        else:
            wavelength = 1550
    else:
        connector_loss = Decimal('0.5') * connectors
        mode_type = "Multi Mode"
        print """\nWhat is the wavelength being used?
        1 - 850nm
        2 - 1300nm"""
        wave = raw_input("Enter the number of your selection: ")
        if wave not in ('1', '2'):
            print "\nThat is not a valid selection"
            menu()
        if wave == '1':
            wavelength = 850
        else:
            wavelength = 1300
    print "\nThe total loss introduced for the %s link by connectors is %sdB\n" % (mode_type, connector_loss)
    cable = int(raw_input("What is the cable length from the sender to the receiver in meters: "))
    if mode_type == 'Single Mode' and wavelength == 1310:
        attenuation = Decimal('0.4')
    elif mode_type == 'Single Mode' and wavelength == 1500:
        attenuation = Decimal('0.3')
    elif mode_type == 'Multi Mode' and wavelength == 850:
        attenuation = Decimal('3.0')
    elif mode_type == 'Multi Mode' and wavelength == 1300:
        attenuation = Decimal('1.0')
    else:
        print "Something went wrong."
    cable_loss = Decimal(cable / 1000.000) * attenuation
    print """\nThe loss introduced by the length of cable for the %s %s link
    is %sdB based on %sdB/km fiber attenuation.\n""" % (mode_type, wavelength, cable_loss, attenuation)
    total_cable_loss = connector_loss + cable_loss
    print "The total connection loss is %sdB\n" % total_cable_loss
    allowable_loss = link_loss_budget - total_cable_loss
    print """The allowable coupler loss for a TAP is a %sdB
    maximum at the monitor port\n""" % allowable_loss
    print """Reference which TAP insertion loss values?
    1 - Industry Recommended
    2 - Cubro Average"""
    choice = raw_input("Enter your selection: ")
    if choice not in ('1', '2'):
        print "That is not a valid selection"
        menu()
    if choice == '1':
        match_industry(mode_type, allowable_loss)
    if choice == '2':
        match_cubro(mode_type, allowable_loss)

def match_industry(mode, loss):
    #Maximum recommended values
    taps_mm = {
               '50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}
               }
    taps_sm = {
               '50/50': {'Network': '3.7', 'Monitor': '3.7'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}
               }
    usable = []
    if mode == 'Single Mode':
        for split in taps_sm:
            if float(taps_sm[split]['Monitor']) < float(loss):
                usable.append(split)
    elif mode == 'Multi Mode':
        for split in taps_mm:
            if float(taps_mm[split]['Monitor']) < float(loss):
                usable.append(split)
    else:
        print "Something went wrong"
    print """\nThe following split ratios are acceptable for this link
    %s""" % usable
    menu()

def match_cubro(mode, loss):
    #Adjusted average Cubro values
    taps_mm = {
               '50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}
               }
    taps_sm = {
               '50/50': {'Network': '3.6', 'Monitor': '3.5'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}
               }
    usable = []
    if mode == 'Single Mode':
        for split in taps_sm:
            if float(taps_sm[split]['Monitor']) < float(loss):
                usable.append(split)
    elif mode == 'Multi Mode':
        for split in taps_mm:
            if float(taps_mm[split]['Monitor']) < float(loss):
                usable.append(split)
    else:
        print "Something went wrong"
    print """\nThe following split ratios are acceptable for this link
    %s""" % usable
    menu()

def max_cable():
    getcontext().prec = 10
    sender = Decimal(raw_input("\nwhat is the sender transmit power (dB): "))
    receiver = Decimal(raw_input("\nWhat is the receiver sensitivity (dB): "))
    link_loss_budget = sender - receiver
    print "\nThe Power Link Loss Budget for this link is %sdB" % link_loss_budget
    print """\nSingle Mode or Multi Mode fiber?
    1 - Single Mode
    2 - Multi Mode"""
    mode = raw_input("Enter the number of your selection: ")
    if mode not in ('1', '2'):
        print "\nThat is not a valid selection."
        menu()
    connectors = Decimal(raw_input("\nHow many connectors are in the path of the link: "))
    if mode == '1':
        connector_loss = Decimal('0.2') * connectors
        mode_type = "Single Mode"
        print """\nWhat is the wavelength being used?
        1 - 1310nm
        2 - 1550nm"""
        wave = raw_input("\nEnter the number of your selection: ")
        if wave not in ('1', '2'):
            print "\nThat is not a valid selection."
        if wave == '1':
            wavelength = 1310
        else:
            wavelength = 1550
    else:
        connector_loss = Decimal('0.5') * connectors
        mode_type = "Multi Mode"
        print """\nWhat is the wavelength being used?
        1 - 850nm
        2 - 1300nm"""
        wave = raw_input("Enter the number of your selection: ")
        if wave not in ('1', '2'):
            print "That is not a valid selection."
            menu()
        if wave == '1':
            wavelength = 850
        else:
            wavelength = 1300
    print "\nThe total loss introduced for the %s link by connectors is %sdB\n" % (mode_type, connector_loss)
    print """What is the split ratio of the TAP?
    1 - 50/50
    2 - 60/40
    3 - 70/30
    4 - 80/20
    5 - 90/10"""
    split = raw_input("Enter the number of your selection: ")
    if split not in ('1', '2', '3', '4', '5'):
        print "That is not a valid input for split ratio"
        menu()
    if split == '1':
        split = '50/50'
    elif split == '2':
        split = '60/40'
    elif split == '3':
        split = '70/30'
    elif split == '4':
        split = '80/20'
    else:
        split = '90/10'
    taps_mm = {
               '50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}
               }
    taps_sm = {
               '50/50': {'Network': '3.7', 'Monitor': '3.7'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}
               }
    if mode_type == 'Single Mode':
        for ratio in taps_sm:
            if split == ratio:
                network = Decimal(taps_sm[ratio]['Network'])
                monitor = Decimal(taps_sm[ratio]['Monitor'])
    elif mode_type == 'Multi Mode':
        for ratio in taps_mm:
            if split == ratio:
                network = Decimal(taps_mm[ratio]['Network'])
                monitor = Decimal(taps_mm[ratio]['Monitor'])
    else:
        print 'Something went wrong'
    total_loss_net = link_loss_budget - connector_loss - network
    total_loss_mon = link_loss_budget - connector_loss - monitor
    if mode_type == 'Single Mode' and wavelength == 1310:
        attenuation = Decimal('0.4')
    elif mode_type == 'Single Mode' and wavelength == 1500:
        attenuation = Decimal('0.3')
    elif mode_type == 'Multi Mode' and wavelength == 850:
        attenuation = Decimal('3.0')
    elif mode_type == 'Multi Mode' and wavelength == 1300:
        attenuation = Decimal('1.0')
    else:
        print "Something went wrong."
    cable_net = 1
    cable_loss_net = Decimal(cable_net / 1000) * attenuation
    while total_loss_net - cable_loss_net > 0:
        cable_net += 1
        cable_loss_net = Decimal(cable_net / 1000) * attenuation
    cable_mon = 1
    cable_loss_mon = Decimal(cable_mon / 1000) * attenuation
    while total_loss_mon - cable_loss_mon > 0:
        cable_mon += 1
        cable_loss_mon = Decimal(cable_mon / 1000) * attenuation
    if mode_type == 'Single Mode' and cable_net > 10000:
        cable_net = 10000
    if mode_type == 'Single Mode' and cable_mon > 10000:
        cable_mon = 10000
    if mode_type == 'Multi Mode' and cable_net > 2000:
        cable_net = 2000
    if mode_type == 'Multi Mode' and cable_mon > 2000:
        cable_mon = 2000
    print "\nThe maximum combined cable length from sender to TAP and from TAP to receiver is %s meters" % cable_net
    print "\nThe maximum combined cable length from sender to TAP and from TAP monitor to tool is %s meters" % cable_mon
    menu()

def ethernet_table():
    print """Ethernet Fiber Standards and max cabling distance:
     ________________________________________________________________________________________________________________
    |         |    Core/   |      | FastEthernet |  1G Ethernet  |  1G Ethernet  |    10G    |    40G    |    100G   |
    |  Name   |  Cladding  | Type |  100BaseFX   |  1000Base-SX  |  1000Base-LX  |  10GBase  |  40GBase  |  100GBase |
    | ________|____________|______|______________|_______________|_______________|___________|___________|___________|
    |   OM1   |  62.5/125  |  MM  |    2000M     |      275M     |     550M*     |    33M    |     NA    |     NA    |
    |_________|____________|______|______________|_______________|_______________|___________|___________|___________|
    |   OM2   |  62.5/125  |  MM  |    2000M     |      550M     |     550M*     |    82M    |     NA    |     NA    |
    |_________|____________|______|______________|_______________|_______________|___________|___________|___________|
    |   OM3   |   50/125   |  MM  |    2000M     |      550M     |     550M      |   300M    |   100M    |    100M   |
    |_________|____________|______|______________|_______________|_______________|___________|___________|___________|
    |   OM4   |   50/125   |  MM  |    2000M     |      550M     |     550M      |   400M    |   150M    |    150M   |
    |_________|____________|______|______________|_______________|_______________|___________|___________|___________|
    |         |            |      |              |     5km @     |     5km @     |  10km @   |           |           |
    |   SM    |   9/125    |  SM  |    2000M     |    1310nm     |    1310nm     |  1310nm   |           |           |
    |_________|____________|______|______________|_______________|_______________|___________|___________|___________|
    *mode condition patch cable required
    """
    menu()

if __name__ == '__main__':
    menu()
