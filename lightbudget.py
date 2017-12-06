#Script to make light budget calculations for permitted cable lengths for a given TAP or appropriate TAP for current link

#!/usr/bin/python

from decimal import *

def menu():
    option = raw_input("""What would you like to do:
    1 - Calculate the max allowed coupler loss for inserting a TAP into a link
    2 - Calculate the max allowed cable length for a given TAPped link
    3 - Exit
    Enter your selection: """)
    try:
        option = int(option)
        if option not in (1, 2, 3):
            print "That is not a valid input"
            menu()
    except:
        print "That is not a valid input"
        menu()
    if option == 1:
        max_split()
    elif option == 2:
        max_cable()
    elif option == 3:
        print "Goodbye"
        exit()
    else:
        print 'Something went wrong!'
        exit()

def max_split():
    getcontext().prec = 10
    sender = Decimal(raw_input("\nwhat is the sender transmit power: "))
    receiver = Decimal(raw_input("\nWhat is the receiver sensitivity: "))
    link_loss_budget = sender - receiver
    print "\nThe Power Link Loss Budget for this link is %s dB" % link_loss_budget
    print """\nSingle Mode or Multi Mode?
    1 - Single Mode
    2 - Multi Mode"""
    mode = int(raw_input("Enter the number of your selection: "))
    connectors = Decimal(raw_input("\nHow many connectors total are in the path of the link: "))
    if mode == 1:
        connector_loss = Decimal('0.2') * connectors
        mode_type = "Single Mode"
        print """\nWhat is the wavelength being used?
        1 - 1310
        2 - 1550"""
        wave = int(raw_input("\nEnter the number of your selection: "))
        if wave == 1:
            wavelength = 1310
        else:
            wavelength = 1550
    else:
        connector_loss = Decimal('0.5') * connectors
        mode_type = "Multi Mode"
        print """\nWhat is the wavelength being used?
        1 - 850
        2 - 1300"""
        wave = int(raw_input("Enter the number of your selection: "))
        if wave == 1:
            wavelength = 850
        else:
            wavelength = 1300
    print "\nThe total loss introduced for the %s link by connectors is %s dB\n" % (mode_type, connector_loss)
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
    cable_loss = Decimal(cable / 1000.00000) * attenuation
    print "\nThe loss introduced by the cable length for the %s %s link is %s dB based on %s dB/km fiber attenuation.\n" % (mode_type, wavelength, cable_loss, attenuation)
    total_cable_loss = connector_loss + cable_loss
    print "The total connection loss is %s dB\n" % total_cable_loss
    allowable_loss = link_loss_budget - total_cable_loss
    print "The allowable coupler loss allowed for a TAP is a %s dB maximum at the monitor port\n" % allowable_loss
    menu()

def max_cable():
    pass

if __name__ == '__main__':
    menu()
