function menu {
  [int]$option = Read-Host 'What would you like to do:
  1 - Calculate the max allowed coupler loss for inserting a TAP into a link
  2 - Calculate the max allowed cable length for a given TAP split ratio in a link
  3 - Display ethernet fiber standards and max cabling distance
  4 - Exit
  Enter your selection'
  If ($option -eq 1) {max_split}
  ElseIf ($option -eq 2) {max_cable}
  ElseIf ($option -eq 3) {ethernet_table}
  ElseIf ($option -eq 4) {Exit}
  Else {Write-Host 'Invalid Option'
        Exit}
}

function max_split {
  $sender = Read-Host 'What is the sender transmit power (dB)'
  $receiver = Read-Host 'What is the receiver sensitivity (dB)'
  $link_loss_budget = $sender - $receiver
  Write-Host "The Power Link Loss Budget for this link is $link_loss_budget dB."
  [int]$mode = Read-Host 'Single-Mode or Multi-Mode fiber?
  1 - Single-Mode
  2 - Multi-Mode
  Enter the number of your selection '
  $connectors = Read-Host 'How many connectors are in the path of the link?'
  If ($mode -eq 1) {
    $connector_loss = 0.2 * $connectors
    $mode_type = 'Single-Mode'
    [int]$wave = Read-Host 'What is the wavelength being used?
    1 - 1310nm
    2 - 1550nm
    Enter the number of your selection'
    If ($wave -eq 1) {[int]$wavelength = 1310}
    Else {[int]$wavelength = 1550}
  }
  ElseIf ($mode -eq 2) {
    $connector_loss = 0.5 * $connectors
    $mode_type = 'Multi-Mode'
    [int]$wave = Read-Host 'What is the wavelength being used?
    1 - 850nm
    2 - 1300nm
    Enter the number of your selection'
    If ($wave -eq 1) {[int]$wavelength = 850}
    Else {[int]$wavelength = 1300}
  }
  Else {Write-Host 'That is not a valid input.'
    menu}
  Write-Host "The total loss introduced for the $mode_type link by connectors is $connector_loss dB."
  [int]$cable = Read-Host 'What is the cable length, in meters, from the sender to the receiver'
  If ($mode_type -eq 'Single-Mode' -and $wavelength -eq 1310) {
    $attenuation = 0.4}
  ElseIf ($mode_type -eq 'Single-Mode' -and $wavelength -eq 1550) {
    $attenuation = 0.3}
  ElseIf ($mode_type -eq 'Multi-Mode' -and $wavelength -eq 850) {
    $attenuation = 3.0}
  ElseIf ($mode_type -eq 'Multi-Mode' -and $wavelength -eq 1300) {
    $attenuation = 1.0}
  Else {Write-Host 'Something went wrong.'
    menu}
  $cable_loss = $cable / 1000 * $attenuation
  Write-Host "The loss introduced by the length of cable for the $mode_type $wavelength nm link
    is $cable_loss dB based on $attenuation dB/km fiber attenuation."
  $total_cable_loss = $connector_loss + $cable_loss
  Write-Host "The total connection loss is $total_cable_loss dB."
  $allowable_loss = $link_loss_budget - $total_cable_loss
  Write-Host "The allowable coupler loss for a TAP is a $allowable_loss dB maximum at the monitor port."
  [int]$choice = Read-Host 'Reference which TAP insertion loss values?
  1 - Industry Standard
  2 - Cubro Average
  Enter the number of your selection'
  If ($choice -eq 1) {match_industry $mode_type $allowable_loss}
  ElseIf ($choice -eq 2) {match_cubro $mode_type $allowable_loss}
  Else {Write-Host 'Invalid input'
    menu}
}

function match_industry {
  param ([parameter(Mandatory=$true)]
         [string]$mode_type,
         [float]$allowable_loss)
  $taps_mm=[ordered]@{'50/50'=[ordered]@{Network=4.5; Monitor=4.5}
             '60/40'=[ordered]@{Network=3.1; Monitor=5.1}
             '70/30'=[ordered]@{Network=2.4; Monitor=6.3}
             '80/20'=[ordered]@{Network=1.8; Monitor=8.1}
             '90/10'=[ordered]@{Network=1.3; Monitor=11.5}
             }
  $taps_sm=[ordered]@{'50/50'=[ordered]@{Network=3.7; Monitor=3.7}
             '60/40'=[ordered]@{Network=2.8; Monitor=4.8}
             '70/30'=[ordered]@{Network=2.0; Monitor=6.1}
             '80/20'=[ordered]@{Network=1.3; Monitor=8.0}
             '90/10'=[ordered]@{Network=0.8; Monitor=12.0}
             }
  $usable = @()
  If ($mode_type -eq 'Single-Mode') {
    foreach ($split in $taps_sm.Keys) {
      If ($taps_sm.$split.Monitor -lt $allowable_loss) {
        $usable += $split
      }
    }
  }
  ElseIf ($mode_type -eq 'Multi-Mode') {
    foreach ($split in $taps_mm.Keys) {
      If ($taps_mm.$split.Monitor -lt $allowable_loss) {
        $usable += $split
      }
    }
  }
  Else {Write-Host 'Something went wrong.'}
  Write-Host "The following split ratios are acceptable for this link $usable"
}

function match_cubro {
  param ([parameter(Mandatory=$true)]
         [string]$mode_type,
         [float]$allowable_loss)
  $taps_mm=[ordered]@{'50/50'=[ordered]@{Network=4.5; Monitor=4.5}
             '60/40'=[ordered]@{Network=3.1; Monitor=5.1}
             '70/30'=[ordered]@{Network=2.4; Monitor=6.3}
             '80/20'=[ordered]@{Network=1.8; Monitor=8.1}
             '90/10'=[ordered]@{Network=1.3; Monitor=11.5}
             }
  $taps_sm=[ordered]@{'50/50'=[ordered]@{Network=3.6; Monitor=3.5}
             '60/40'=[ordered]@{Network=2.8; Monitor=4.8}
             '70/30'=[ordered]@{Network=2.0; Monitor=6.1}
             '80/20'=[ordered]@{Network=1.3; Monitor=8.0}
             '90/10'=[ordered]@{Network=0.8; Monitor=12.0}
             }
  $usable = @()
  If ($mode_type -eq 'Single-Mode') {
    foreach ($split in $taps_sm.Keys) {
      If ($taps_sm.$split.Monitor -lt $allowable_loss) {
        $usable += $split
      }
    }
  }
  ElseIf ($mode_type -eq 'Multi-Mode') {
    foreach ($split in $taps_mm.Keys) {
      If ($taps_mm.$split.Monitor -lt $allowable_loss) {
        $usable += $split
      }
    }
  }
  Else {Write-Host 'Something went wrong.'}
  Write-Host "The following split ratios are acceptable for this link $usable"
}

function max_cable {
  $sender = Read-Host 'What is the sender transmit power (dB)'
  $receiver = Read-Host 'What is the receiver sensitivity (dB)'
  $link_loss_budget = $sender - $receiver
  Write-Host "The Power Link Loss Budget for this link is $link_loss_budget dB."
  [int]$mode = Read-Host 'Single-Mode or Multi-Mode fiber?
  1 - Single-Mode
  2 - Multi-Mode
  Enter the number of your selection '
  $valid_input = 1, 2
  If ($mode -notin $valid_input) {
    Write-Host "$mode is not a valid input."
    menu}
  $connectors = Read-Host 'How many connectors are in the path of the link?'
  If ($mode -eq 1) {
    $connector_loss = 0.2 * $connectors
    $mode_type = 'Single-Mode'
    [int]$wave = Read-Host 'What is the wavelength being used?
    1 - 1310nm
    2 - 1550nm
    Enter the number of your selection'
    If ($wave -notin $valid_input) {
      Write-Host "$wave is not a valid option."
      menu}
    If ($wave -eq 1) {[int]$wavelength = 1310}
    Else {[int]$wavelength = 1550}
  }
  ElseIf ($mode -eq 2) {
    $connector_loss = 0.5 * $connectors
    $mode_type = 'Multi-Mode'
    [int]$wave = Read-Host 'What is the wavelength being used?
    1 - 850nm
    2 - 1300nm
    Enter the number of your selection'
    If ($wave -notin $valid_input) {
      Write-Host "$wave is not a valid option."
      menu}
    If ($wave -eq 1) {[int]$wavelength = 850}
    Else {[int]$wavelength = 1300}
  }
  Else {Write-Host "$mode is not a valid input."
    menu}
  Write-Host "The total loss introduced for the $mode_type link by connectors is $connector_loss dB."
  [int]$split = Read-Host 'What is the split ratio of the TAP?
    1 - 50/50
    2 - 60/40
    3 - 70/30
    4 - 80/20
    5 - 90/10
    Enter the number of your selection '
  $valid_split = 1, 2, 3, 4, 5
  If ($split -notin $valid_split) {
    Write-Host "$split is not a valid option."
    menu}
  $split_ratios=[ordered]@{1='50/50'
                           2='60/40'
                           3='70/30'
                           4='80/20'
                           5='90/10'}
  $ratio = $split_ratios[$split]
  $taps_mm=[ordered]@{'50/50'=[ordered]@{Network=4.5; Monitor=4.5}
              '60/40'=[ordered]@{Network=3.1; Monitor=5.1}
              '70/30'=[ordered]@{Network=2.4; Monitor=6.3}
              '80/20'=[ordered]@{Network=1.8; Monitor=8.1}
              '90/10'=[ordered]@{Network=1.3; Monitor=11.5}
              }
  $taps_sm=[ordered]@{'50/50'=[ordered]@{Network=3.6; Monitor=3.5}
              '60/40'=[ordered]@{Network=2.8; Monitor=4.8}
              '70/30'=[ordered]@{Network=2.0; Monitor=6.1}
              '80/20'=[ordered]@{Network=1.3; Monitor=8.0}
              '90/10'=[ordered]@{Network=0.8; Monitor=12.0}
              }
  If ($mode_type -eq 'Single-Mode') {
    foreach ($value in $taps_sm.Keys) {
      If ($ratio -eq $value) {
        $network = $taps_sm.$value.Network
        $monitor = $taps_sm.$value.Monitor
      }
    }
  }
  ElseIf ($mode_type -eq 'Multi-Mode') {
    foreach ($value in $taps_mm.Keys) {
      If ($ratio -eq $value) {
        $network = $taps_mm.$value.Network
        $monitor = $taps_mm.$value.Monitor
      }
    }
  }
  Else {Write-Host 'Something went wrong.'
    menu}
  $total_loss_net = $link_loss_budget - $connector_loss - $network
  $total_loss_mon = $link_loss_budget - $connector_loss - $monitor
  If ($mode_type -eq 'Single-Mode' -and $wavelength -eq 1310) {
      $attenuation = 0.4
  }
  Elseif ($mode_type -eq 'Single-Mode' -and $wavelength -eq 1500) {
      $attenuation = 0.3
  }
  Elseif ($mode_type -eq 'Multi-Mode' -and $wavelength -eq 850) {
      $attenuation = 3.0
  }
  Elseif ($mode_type -eq 'Multi-Mode' -and $wavelength -eq 1300) {
      $attenuation = 1.0
  }
  Else {Write-Host 'Something went wrong.'}
  $cable_net = 1
  $cable_loss_net = $cable_net * $attenuation/1000
  while ($total_loss_net - $cable_loss_net -gt 0) {
    $cable_net += 1
    $cable_loss_net = $cable_net * $attenuation/1000
  }
  $cable_mon = 1
  $cable_loss_mon = $cable_mon * $attenuation/1000
  while ($total_loss_mon - $cable_loss_mon -gt 0) {
    $cable_mon += 1
    $cable_loss_mon = $cable_mon * $attenuation/1000
  }
  cable_by_eth_standard $mode_type $cable_net $cable_mon
}

function cable_by_eth_standard {
  param ([parameter(Mandatory=$true)]
         [string]$mode_type,
         [int]$cable_net,
         [int]$cable_mon)
  $valid_input = 1, 2, 3, 4, 5
  If ($mode_type -eq 'Multi-Mode') {
    [int]$standard_type = Read-Host 'What is the Ethernet Standard in use?
        1 - OM1-SX
        2 - OM1-LX
        3 - OM2
        4 - OM3
        5 - OM4
        Enter the number of your selection '
    If ($standard_type -notin $valid_input) {
      Write-Host "$standard_type is not a valid input."
      menu
    }
    $standard_table = [ordered]@{1='OM1-SX'
                                 2='OM1-LX'
                                 3='OM2'
                                 4='OM3'
                                 5='OM4'}
    $standard = $standard_table[$standard_type]
  }
  [int]$speed = Read-Host 'What speed is the link?
    1 - 100M
    2 - 1G
    3 - 10G
    4 - 40G
    5 - 100G
    Enter the number of your selection '
  If ($speed -notin $valid_input) {
    Write-Host "$speed is not a valid input."
    menu
  }
  $speed_table = [ordered]@{1='100M'
                            2='1G'
                            3='10G'
                            4='40G'
                            5='100G'}
  $link_speed = $speed_table.$speed
  $table = [ordered]@{
        'Single-Mode'=[ordered]@{'100M'=2000
                                 '1G'=5000
                                 '10G'=10000
                                 '40G'='Unknown'
                                 '100G'='Unknown'}
        'Multi-Mode'=[ordered]@{'OM1-SX'=[ordered]@{'100M'=2000
                                                    '1G'=275
                                                    '10G'=33}
                                'OM1-LX'=[ordered]@{'100M'=2000
                                                    '1G'=550
                                                    '10G'=33}
                                'OM2'=[ordered]@{'100M'=2000
                                                 '1G'=550
                                                 '10G'=82}
                                'OM3'=[ordered]@{'100M'=2000
                                                 '1G'=550
                                                 '10G'=300
                                                 '40G'=100
                                                 '100G'=100}
                                'OM4'=[ordered]@{'100M'=2000
                                                 '1G'=550
                                                 '10G'=400
                                                 '40G'=150
                                                 '100G'=150}
                                }
                      }
  If ($mode_type -eq 'Single-Mode') {
    $max_standard_length = $table.'Single-Mode'.$link_speed
    If ($cable_net -gt $max_standard_length) {
      $cable_net = $max_standard_length
    }
    If ($cable_mon -gt $max_standard_length) {
      $cable_mon = $max_standard_length
    }
  }
  If ($mode_type -eq 'Multi-Mode') {
    $max_standard_length = $table.'Multi-Mode'.$standard.$link_speed
    If ($cable_net -gt $max_standard_length) {
      $cable_net = $max_standard_length}
    If ($cable_mon -gt $max_standard_length) {
      $cable_mon = $max_standard_length}
  Write-Host "The maximum combined cable length from sender to TAP and from
              TAP to receiver is $cable_net meters"
  Write-Host "The maximum combined cable length from sender to TAP and from
              TAP monitor to tool is $cable_mon meters"
  menu
  }
}

function ethernet_table {
  Write-Host 'Ethernet Fiber Standards and max cabling distance:
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
    '
    menu
}

menu
