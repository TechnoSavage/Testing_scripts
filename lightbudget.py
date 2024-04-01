#!/usr/bin/python3

""" 
Script to make light budget calculations for permitted cable lengths for a given TAP or appropriate TAP for current link.
"""

from decimal import Decimal, getcontext

def menu():
    """ 
    High level menu for available options. 
    """
    
    option = input("""\nWhat would you like to do:
    1 - Calculate the max allowed coupler loss for inserting a TAP into a link
    2 - Calculate the max allowed cable length for a given TAP split ratio in a link
    3 - Display ethernet fiber standards and max cabling distance
    4 - Exit
    Enter your selection: """)
    
    if option not in ('1', '2', '3', '4'):
        print("That is not a valid input")
        menu()
    if option == '1':
        max_split()
    elif option == '2':
        max_cable()
    elif option == '3':
        ethernet_table()
    elif option == '4':
        print('Goodbye')
        exit()
    else:
        print('Something went wrong!')
        exit()

def max_split():
    """ 
    Determine the maximum split ratio that can be used on a given link.
    """
    
    getcontext().prec = 5
    sender = Decimal(input("\nwhat is the sender transmit power (dB): "))
    receiver = Decimal(input("\nWhat is the receiver sensitivity (dB): "))
    link_loss_budget = sender - receiver
    print(f"\nThe Power Link Loss Budget for this link is {link_loss_budget}dB")
    mode = input("""\nSingle Mode or Multi Mode fiber?
    1 - Single Mode
    2 - Multi Mode
    Enter the number of your selection: """)
    if mode not in ('1', '2'):
        print("\nThat is not a valid selection")
        menu()
    connectors = Decimal(input("\nHow many connectors are in the path of the link: "))
    if mode == '1':
        connector_loss = Decimal('0.2') * connectors
        mode_type = "Single Mode"
        wave = input("""\nWhat is the wavelength being used?
        1 - 1310nm
        2 - 1550nm
        Enter the number of your selection: """)
        if wave not in ('1', '2'):
            print("\nThat is not a valid selection")
            menu()
        if wave == '1':
            wavelength = 1310
        else:
            wavelength = 1550
    else:
        connector_loss = Decimal('0.5') * connectors
        mode_type = "Multi Mode"
        wave = input("""\nWhat is the wavelength being used?
        1 - 850nm
        2 - 1300nm
        Enter the number of your selection: """)
        if wave not in ('1', '2'):
            print("\nThat is not a valid selection")
            menu()
        if wave == '1':
            wavelength = 850
        else:
            wavelength = 1300
    print(f"\nThe total loss introduced for the {mode_type} link by connectors is {connector_loss}dB\n")
    cable = int(input("What is the cable length from the sender to the receiver in meters: "))
    if mode_type == 'Single Mode' and wavelength == 1310:
        attenuation = Decimal('0.4')
    elif mode_type == 'Single Mode' and wavelength == 1500:
        attenuation = Decimal('0.3')
    elif mode_type == 'Multi Mode' and wavelength == 850:
        attenuation = Decimal('3.0')
    elif mode_type == 'Multi Mode' and wavelength == 1300:
        attenuation = Decimal('1.0')
    else:
        print('Something went wrong.')
    cable_loss = Decimal(cable / 1000.000) * attenuation
    print(f"\nThe loss introduced by the length of cable for the {mode_type} {wavelength} link is {cable_loss}dB based on {attenuation}dB/km fiber attenuation.\n")
    total_cable_loss = connector_loss + cable_loss
    print(f"The total connection loss is {total_cable_loss}dB\n")
    allowable_loss = link_loss_budget - total_cable_loss
    print(f"The allowable coupler loss for a TAP is a {allowable_loss}dB maximum at the monitor port\n")
    choice = input("""Reference which TAP insertion loss values?
    1 - Industry Standard
    2 - Cubro Average
    Enter your selection: """)
    if choice not in ('1', '2'):
        print("\nThat is not a valid selection")
        menu()
    if choice == '1':
        match_industry(mode_type, allowable_loss)
    if choice == '2':
        match_cubro(mode_type, allowable_loss)

def match_industry(mode, loss):
    """
    Determine available TAP options using industry standard values.
    """
    
    #Maximum recommended values
    taps_mm = {'50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}}
    taps_sm = {'50/50': {'Network': '3.7', 'Monitor': '3.7'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}}
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
        print("\nSomething went wrong")
    print(f"\nThe following split ratios are acceptable for this link {usable}")
    menu()

def match_cubro(mode, loss):
    """
    Determine available TAP options for a given link using Cubro values.
    """
    
    #Adjusted average Cubro values
    taps_mm = {'50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}}
    taps_sm = {'50/50': {'Network': '3.6', 'Monitor': '3.5'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}}
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
        print("\nSomething went wrong")
    print(f"\nThe following split ratios are acceptable for this link {usable}")
    menu()

def max_cable():
    """ Function to determine max cable length for a given link + connectors."""
    getcontext().prec = 5
    sender = Decimal(input("\nwhat is the sender transmit power (dB): "))
    receiver = Decimal(input("\nWhat is the receiver sensitivity (dB): "))
    link_loss_budget = sender - receiver
    print(f"\nThe Power Link Loss Budget for this link is {link_loss_budget}dB")
    mode = input("""\nSingle Mode or Multi Mode fiber?
    1 - Single Mode
    2 - Multi Mode
    Enter the number of your selection: """)
    if mode not in ('1', '2'):
        print("\nThat is not a valid selection.")
        menu()
    connectors = Decimal(input("\nHow many connectors are in the path of the link: "))
    if mode == '1':
        connector_loss = Decimal('0.2') * connectors
        mode_type = 'Single Mode'
        print("""\nWhat is the wavelength being used?
        1 - 1310nm
        2 - 1550nm""")
        wave = input("\nEnter the number of your selection: ")
        if wave not in ('1', '2'):
            print("\nThat is not a valid selection.")
        if wave == '1':
            wavelength = 1310
        else:
            wavelength = 1550
    else:
        connector_loss = Decimal('0.5') * connectors
        mode_type = "Multi Mode"
        wave = input("""\nWhat is the wavelength being used?
        1 - 850nm
        2 - 1300nm
        Enter the number of your selection: """)
        if wave not in ('1', '2'):
            print('That is not a valid selection.')
            menu()
        if wave == '1':
            wavelength = 850
        else:
            wavelength = 1300
    print (f"\nThe total loss introduced for the {mode_type} link by connectors is {connector_loss}dB\n")
    split = input("""\nWhat is the split ratio of the TAP?
    1 - 50/50
    2 - 60/40
    3 - 70/30
    4 - 80/20
    5 - 90/10
    Enter the number of your selection: """)
    if split not in ('1', '2', '3', '4', '5'):
        print('That is not a valid input for split ratio')
        menu()
    split_ratios = {'1': '50/50',
                    '2': '60/40',
                    '3': '70/30',
                    '4': '80/20',
                    '5': '90/10'}
    ratio = split_ratios[split]
    taps_mm = {'50/50': {'Network': '4.5', 'Monitor': '4.5'},
               '60/40': {'Network': '3.1', 'Monitor': '5.1'},
               '70/30': {'Network': '2.4', 'Monitor': '6.3'},
               '80/20': {'Network': '1.8', 'Monitor': '8.1'},
               '90/10': {'Network': '1.3', 'Monitor': '11.5'}}
    taps_sm = {'50/50': {'Network': '3.7', 'Monitor': '3.7'},
               '60/40': {'Network': '2.8', 'Monitor': '4.8'},
               '70/30': {'Network': '2.0', 'Monitor': '6.1'},
               '80/20': {'Network': '1.3', 'Monitor': '8.0'},
               '90/10': {'Network': '0.8', 'Monitor': '12.0'}}
    if mode_type == 'Single Mode':
        for value in taps_sm:
            if ratio == value:
                network = Decimal(taps_sm[value]['Network'])
                monitor = Decimal(taps_sm[value]['Monitor'])
    elif mode_type == 'Multi Mode':
        for value in taps_mm:
            if ratio == value:
                network = Decimal(taps_mm[value]['Network'])
                monitor = Decimal(taps_mm[value]['Monitor'])
    else:
        print('Something went wrong')
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
        print('Something went wrong.')
    cable_net = 1
    cable_loss_net = Decimal(cable_net * (attenuation / 1000))
    while total_loss_net - cable_loss_net > 0:
        cable_net += 1
        cable_loss_net = Decimal(cable_net * (attenuation / 1000))
    cable_mon = 1
    cable_loss_mon = Decimal(cable_mon * (attenuation / 1000))
    while total_loss_mon - cable_loss_mon > 0:
        cable_mon += 1
        cable_loss_mon = Decimal(cable_mon * (attenuation / 1000))
    cable_by_eth_standard(mode_type, cable_net, cable_mon)

def cable_by_eth_standard(mode_type, cable_net, cable_mon):
    """ Determines what the maximum cable length could be given a Ethernet
        fiber standard."""
    if mode_type == 'Multi Mode':
        standard_type = input("""\nWhat is the Ethernet Standard in use?
        1 - OM1-SX
        2 - OM1-LX
        3 - OM2
        4 - OM3
        5 - OM4
        Enter the number of your selection: """)
        if standard_type not in ('1', '2', '3', '4', '5'):
            print('That is not a valid selection.')
            menu()
        standard_table = {'1': 'OM1-SX',
                          '2': 'OM1-LX',
                          '3': 'OM2',
                          '4': 'OM3',
                          '5': 'OM4'}
        standard = standard_table[standard_type]
    speed = input("""\nWhat speed is the link?
    1 - 100M
    2 - 1G
    3 - 10G
    4 - 40G
    5 - 100G
    Enter the number of your selection: """)
    if speed not in ('1', '2', '3', '4', '5'):
        print('That is not a valid selection.')
        menu()
    speed_table = {'1': '100M',
                   '2': '1G',
                   '3': '10G',
                   '4': '40G',
                   '5': '100G'}
    link_speed = speed_table[speed]
    table = {
        'Single Mode':{'100M': 2000,
                       '1G': 5000,
                       '10G': 10000,
                       '40G': 'Unknown',
                       '100G': 'Unknown'},
        'Multi Mode': {'OM1-SX': {'100M': 2000,
                                  '1G': 275,
                                  '10G': 33},
                       'OM1-LX': {'100M': 2000,
                                  '1G': 550,
                                  '10G': 33},
                       'OM2': {'100M': 2000,
                               '1G': 550,
                               '10G': 82},
                       'OM3': {'100M': 2000,
                               '1G': 550,
                               '10G': 300,
                               '40G': 100,
                               '100G': 100},
                       'OM4': {'100M': 2000,
                               '1G': 550,
                               '10G': 400,
                               '40G': 150,
                               '100G': 150}
                      }}
    if mode_type == 'Single Mode':
        try:
            max_standard_length = table['Single Mode'][link_speed]
            if cable_net > max_standard_length:
                cable_net = max_standard_length
            if cable_mon > max_standard_length:
                cable_mon = max_standard_length
        except (KeyError, ValueError) as reason:
            print("That standard does not support that speed.", reason)
    if mode_type == 'Multi Mode':
        try:
            max_standard_length = table['Multi Mode'][standard][link_speed]
            if cable_net > max_standard_length:
                cable_net = max_standard_length
            if cable_mon > max_standard_length:
                cable_mon = max_standard_length
        except KeyError as reason:
            print("That standard does not support that speed.", reason)
    print(f"\nThe maximum combined cable length from sender to TAP and from TAP to receiver is {cable_net} meters")
    print(f"\nThe maximum combined cable length from sender to TAP and from TAP monitor to tool is {cable_mon} meters")
    menu()

def ethernet_table():
    """ Display table of fiber standards. """
    print("""Ethernet Fiber Standards and max cabling distance:
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
    """)
    menu()

if __name__ == '__main__':
    menu()
