#!/bin/bash

#Calculate the light budget for an optical link and determin appropriate TAP
#split ratios or maximum cable length that can be used with a given TAP

menu () {
  read -p "What would you like to do:
  1 - Calculate the max allowed coupler loss for inserting a TAP into a link
  2 - Calculate the max allowed cable length for a given TAP split ratio in a link
  3 - Display ethernet fiber standards and max cabling distance
  4 - Exit
  Enter your selection: " option
  if [[ $option == 1 ]]; then
    max_split
  elif [[ $option == 2 ]]; then
    max_cable
  elif [[ $option == 3 ]]; then
    ethernet_table
  fi
  return
}

max_split () {
read -p "What is the sender transmit power (dB): " sender
read -p "What is the receiver sensitivity (dB): " receiver
link_loss_budget=$(bc <<< "scale=10;$sender- $receiver")
echo "The Power Link Loss Budget for this link is $link_loss_budget dB"
read -p "Single-Mode or Multi-Mode fiber?
1 - Single-Mode
2 - Multi-Mode
Enter the number of your selection: " mode
read -p "How many connectors are in the path of the link?: " connectors
if [[ $mode == 1 ]]; then
  connector_loss=$(bc <<< "scale=10;0.2* $connectors")
  mode_type="Single-Mode"
  read -p "What is the wavelength being used?
  1 - 1310nm
  2 - 1550nm
  Enter the number of your selection: " wave
  if [[ $wave == 1 ]]; then
    wavelength=1310
  else
    wavelength=1550
  fi
elif [[ $mode == 2 ]]; then
  connector_loss=$(bc <<< "scale=10;0.5* $connectors")
  mode_type="Multi-Mode"
  read -p "What is the wavelength being used?
  1 - 850nm
  2 - 1300nm
  Enter the number of your selection: " wave
  if [[ $wave == 1 ]]; then
    wavelength=850
  else
    wavelength=1300
  fi
else
  echo "That is not a valid input."
  menu
fi
echo "The total loss introduced for the $mode_type link by connectors is $connector_loss dB."
read -p "What is the cable length, in meters, from the sender to the receiver: " cable
if [[ $mode_type == "Single-Mode" && $wavelength == 1310 ]]; then
  attenuation=0.4
elif [[ $mode_type == "Single-Mode" && $wavelength == 1550 ]]; then
  attenuation=0.3
elif [[ $mode_type == "Multi-Mode" && $wavelength == 850 ]]; then
  attenuation=3.0
elif [[ $mode_type == "Multi-Mode" && $wavelength == 1300 ]]; then
  attenuation=1.0
else
  echo "Something went wrong."
  menu
fi
cable_loss=$(bc <<< "scale=10;$cable/1000* $attenuation")
echo "The loss introduced by the length of cable for the $mode_type $wavelength nm link
  is $cable_loss dB based on $attenuation dB/km fiber attenuation."
total_cable_loss=$(bc <<< "scale=10;$connector_loss+ $cable_loss")
echo "The total connection loss is $total_cable_loss dB."
allowable_loss=$(bc <<< "scale=10;$link_loss_budget- $total_cable_loss")
echo "The allowable coupler loss for a TAP is a $allowable_loss dB maximum at the monitor port."
read -p "Reference which TAP insertion loss values?
1 - Industry Standard
2 - Cubro Average
Enter the number of your selection: " choice
if [[ $choice == 1 ]]; then
  match_industry $mode_type $allowable_loss
elif [[ $choice == 2 ]]; then
  match_cubro $mode_type $allowable_loss
else
  echo "Invalid input."
  menu
fi
return
}

match_industry () {
  mode=$1
  loss=$2
  declare -A taps_mm=(["50/50"]=4.5 ["60/40"]=5.1 ["70/30"]=6.3 ["80/20"]=8.1 ["90/10"]=11.5)
  declare -A taps_sm=(["50/50"]=3.7 ["60/40"]=4.8 ["70/30"]=6.1 ["80/20"]=8.0 ["90/10"]=12.0)
  usable=()
  if [[ $mode == "Single-Mode" ]]; then
    for split in ${!taps_sm[@]}
    do
      if (( $( echo "${taps_sm[$split]} < $loss" | bc -l ) )); then
         usable+=($split)
      fi
    done
  elif [[ $mode == "Multi-Mode" ]]; then
    for split in ${!taps_mm[@]}
    do
      if (( $( echo "${taps_mm[$split]} < $loss" | bc -l ) )); then
        usable+=($split)
      fi
    done
  else
    echo "Something went wrong."
    menu
  fi
  echo "The following split ratios are suitable for this link:
  ${usable[@]}."
  menu
return
}

match_cubro () {
  mode=$1
  loss=$2
  declare -A taps_mm=(["50/50"]=4.5 ["60/40"]=5.1 ["70/30"]=6.3 ["80/20"]=8.1 ["90/10"]=11.5)
  declare -A taps_sm=(["50/50"]=3.5 ["60/40"]=4.8 ["70/30"]=6.1 ["80/20"]=8.0 ["90/10"]=12.0)
  usable=()
  if [[ $mode == "Single-Mode" ]]; then
    for split in ${!taps_sm[@]}
    do
      if (( $( echo "${taps_sm[$split]} < $loss" | bc -l ) )); then
         usable+=($split)
      fi
    done
  elif [[ $mode == "Multi-Mode" ]]; then
    for split in ${!taps_mm[@]}
    do
      if (( $( echo "${taps_mm[$split]} < $loss" | bc -l ) )); then
        usable+=($split)
      fi
    done
  else
    echo "Something went wrong."
    menu
  fi
  echo "The following split ratios are suitable for this link:
  ${usable[@]}."
  menu
return
}

max_cable () {
read -p "What is the sender transmit power (dB): " sender
read -p "What is the receiver sensitivity (dB): " receiver
link_loss_budget=$(bc <<< "scale=10;$sender- $receiver")
echo "The Power Link Loss Budget for this link is $link_loss_budget dB."
read -p "Single-Mode or Multi-Mode Fiber?
1 - Single-mode
2 - Multi-Mode
Enter the number of your selection: " mode
read -p "How many connectors are in the path of the link?: " connectors
if [[ $mode == 1 ]]; then
  connector_loss=$(bc <<< "scale=10;0.2* $connectors")
  mode_type="Single-Mode"
  read -p "What is the wavelength being used?
  1 - 1310nm
  2 - 1550nm
  Enter the number of your selection: " wave
  if [[ $wave == 1 ]]; then
    wavelength=1310
  else
    wavelength=1550
  fi
elif [[ $mode == 2 ]]; then
  connector_loss=$(bc <<< "scale=10;0.5* $connectors")
  mode_type="Multi-Mode"
  read -p "What is the wavelength being used?
  1 - 850nm
  2 - 1300nm
  Enter the number of your selection: " wave
  if [[ $wave == 1 ]]; then
    wavelength=850
  else
    wavelength=1300
  fi
else
  echo "That is not a valid input."
  menu
fi
echo "The total loss introduced for the $mode_type link by connectors is $connector_loss dB."
read -p "What is the split ratio of the TAP?
1 - 50/50
2 - 60/40
3 - 70/30
4 - 80/20
5 - 90/10
Enter the number of your selection: " split
if [[ $split == 1 ]]; then
  split="50/50"
elif [[ $split == 2 ]]; then
  split="60/40"
elif [[ $split == 3 ]]; then
  split="70/30"
elif [[ $split == 4 ]]; then
  split="80/20"
elif [[ $split == 5 ]]; then
  split="90/10"
else
  echo "That is not a valid input."
  menu
fi
declare -A taps_mm_net=(["50/50"]=4.5 ["60/40"]=3.1 ["70/30"]=2.4 ["80/20"]=1.8 ["90/10"]=1.3)
declare -A taps_mm_mon=(["50/50"]=4.5 ["60/40"]=5.1 ["70/30"]=6.3 ["80/20"]=8.1 ["90/10"]=11.5)
declare -A taps_sm_net=(["50/50"]=3.7 ["60/40"]=2.8 ["70/30"]=2.0 ["80/20"]=1.3 ["90/10"]=0.8)
declare -A taps_sm_mon=(["50/50"]=3.7 ["60/40"]=4.8 ["70/30"]=6.1 ["80/20"]=8.0 ["90/10"]=12.0)
if [[ $mode_type == "Single-Mode" ]]; then
  for ratio in ${!taps_sm_net[@]}; do
    if [[ $split == $ratio ]]; then
      network=$(${taps_sm_net[$ratio]})
    fi
  done
  for ratio in ${!taps_sm_mon[@]}; do
    if [[ $split == $ratio ]]; then
      monitor=$(${taps_sm_mon[$ratio]})
    fi
  done
elif [[ $mode_type == "Multi-Mode" ]]; then
  for ratio in ${!taps_mm_net[@]}; do
    if [[ $split == $ratio ]]; then
      network=${taps_mm_net[$ratio]}
    fi
  done
  for ratio in ${!taps_mm_mon[@]}; do
    if [[ $split == $ratio ]]; then
      monitor=${taps_mm_mon[$ratio]}
    fi
  done
else
  echo "Something went wrong."
  menu
fi
total_loss_net=$(bc <<< "scale=10;$link_loss_budget- $connector_loss- $network")
total_loss_mon=$(bc <<< "scale=10;$link_loss_budget- $connector_loss- $monitor")
if [[ $mode_type == "Single-Mode" && $wavelength == 1310 ]]; then
  attenuation=0.4
elif [[ $mode_type == "Single-Mode" && $wavelength == 1550 ]]; then
  attenuation=0.3
elif [[ $mode_type == "Multi-Mode" && $wavelength == 850 ]]; then
  attenuation=3.0
elif [[ $mode_type == "Multi-Mode" && $wavelength == 1300 ]]; then
  attenuation=1.0
else
  echo "Something went wrong."
  menu
fi
cable_net=1
cable_loss_net=$(bc <<< "scale=10;$cable_net* $attenuation/1000")
while (( $( echo "$total_loss_net - $cable_loss_net > 0" | bc -l ) )); do
  cable_net+=1
  cable_loss_net=$(bc <<< "scale=10;$cable_net* $attenuation/1000")
done
cable_mon=1
cable_loss_mon=$(bc <<< "scale=10;$cable_mon* $attenuation/1000")
while (( $( echo "$total_loss_mon - $cable_loss_mon > 0" | bc -l ) )); do
  cable_mon+=1
  cable_loss_mon=$(bc <<< "scale=10;$cable_mon* $attenuation/1000")
done
if [[ $mode_type == "Single-Mode" && $( echo "$cable_net > 10000" | bc -l ) == 1 ]]; then
  cable_net=10000
fi
if [[ $mode_type == "Single-Mode" && $( echo "$cable_mon > 10000" | bc -l ) == 1 ]]; then
  cable_mon=10000
fi
if [[ $mode_type == "Multi-Mode" &&  $( echo "$cable_net > 2000" | bc -l ) == 1 ]]; then
  cable_net=2000
fi
if [[ $mode_type == "Multi-Mode" &&  $( echo "$cable_mon > 2000" | bc -l ) == 1 ]]; then
  cable_mon=2000
fi
echo "The maximum combined cable length from sender to TAP and from
TAP to receiver is $cable_net meters"
echo "The maximum combined cable length from sender to TAP and from
TAP monitor to tool is $cable_mon meters"
return
}

ethernet_table () {
  echo "Ethernet Fiber Standards and max cabling distance:
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
    "
  menu
  return
}

menu
