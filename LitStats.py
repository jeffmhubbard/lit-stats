#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# LitStats.py - display stats from Litcube's Universe

from __future__ import print_function
import os, sys
from time import sleep
from math import floor

# settings
interval = 10
log_file = '~/.config/EgoSoft/X3AP/log09004.txt'

# return comma seperated numbers ie. 1,000,000,000
def add_commas(amount): 
    return ("{:,}".format(int(amount)))

# calculate fightrank loot chance
def calc_flc(rank):
    total = 1000000
    factor = 385
    chance = floor((rank * 100) / total) 
    x = floor((rank * 1000) / factor)
    chance = chance * floor(x / 1000)
    chance = chance / 10000
    return chance

# format time for humans
def time_format(ntime):
    days = floor(floor(floor(ntime/60)/60)/24)
    hours = floor(floor((ntime-((days*24)*60*60))/60)/60)
    minutes = floor((ntime-((((days*24)+hours)*60)*60))/60)
    seconds = ntime-(((((days*24)+hours)*60)+minutes)*60)
    if minutes < 10: minutes = str.join('',('0',str(minutes)))
    if seconds < 10: seconds = str.join('',('0',str(seconds)))
    return "{} Days, {}:{}:{}".format(
            int(float(days)),
            int(float(hours)),
            int(float(minutes)),
            int(float(seconds)))

# returns dictionary of preformatted strings
def get_stats(file):
    file = os.path.expanduser(file)
    with open(file) as fp:
    
        lines = fp.read().split('\n')
        data = {}
    
        credits = lines[0] #1
        credits = add_commas(credits)
        data['Credits'] = credits
    
        playtime = lines[1] #2
        playtime = time_format(int(playtime))
        data['PlayTime'] = playtime
    
        realtime = lines[2] #3
        realtime = time_format(int(realtime))
        data['RealTime'] = realtime
    
        argon_percent = lines[3] #4
        data['NotorietyPercentArgon'] = argon_percent
    
        argon_title = lines[4] #5
        data['NotorietyTitleArgon'] = argon_title
    
        boron_percent = lines[5] #6
        data['NotorietyPercentBoron'] = boron_percent
    
        boron_title = lines[6] #7
        data['NotorietyTitleBoron'] = boron_title
    
        split_percent = lines[7] #8
        data['NotorietyPercentSplit'] = split_percent
    
        split_title = lines[8] #9
        data['NotorietyTitleSplit'] = split_title
    
        paranid_percent = lines[9] #10
        data['NotorietyPercentParanid'] = paranid_percent
    
        paranid_title = lines[10] #11
        data['NotorietyTitleParanid'] = paranid_title
    
        teladi_percent = lines[11] #12
        data['NotorietyPercentTeladi'] = teladi_percent
    
        teladi_title = lines[12] #13
        data['NotorietyTitleTeladi'] = teladi_title
    
        goner_percent = lines[13] #14
        data['NotorietyPercentGoner'] = goner_percent
    
        goner_title = lines[14] #15
        data['NotorietyTitleGoner'] = goner_title
    
        terran_percent = lines[15] #16
        data['NotorietyPercentTerran'] = terran_percent
    
        terran_title = lines[16] #17
        data['NotorietyTitleTerran'] = terran_title
    
        atf_percent = lines[17] #18
        data['NotorietyPercentATF'] = atf_percent
    
        atf_title = lines[18] #19
        data['NotorietyTitleATF'] = atf_title
    
        pirates_percent = lines[19] #20
        data['NotorietyPercentPirates'] = pirates_percent
    
        pirates_title = lines[20] #21
        data['NotorietyTitlePirates'] = pirates_title
    
        yaki_percent = lines[21] #22
        data['NotorietyPercentYaki'] = yaki_percent
    
        yaki_title = lines[22] #23
        data['NotorietyTitleYaki'] = yaki_title
    
        count_m1 = lines[23] #24
        count_m1 = add_commas(count_m1)
        data['PropertyCountM1'] = count_m1
    
        count_m2 = lines[24] #25
        count_m2 = add_commas(count_m2)
        data['PropertyCountM2'] = count_m2
    
        count_m3 = lines[25] #26
        count_m3 = add_commas(count_m3)
        data['PropertyCountM3'] = count_m3
    
        count_m4 = lines[26] #27
        count_m4 = add_commas(count_m4)
        data['PropertyCountM4'] = count_m4
    
        count_m5 = lines[27] #28
        count_m5 = add_commas(count_m5)
        data['PropertyCountM5'] = count_m5
    
        count_m6 = lines[28] #29
        count_m6 = add_commas(count_m6)
        data['PropertyCountM6'] = count_m6
    
        count_m7 = lines[29] #30
        count_m7 = add_commas(count_m7)
        data['PropertyCountM7'] = count_m7
    
        count_m8 = lines[30] #31
        count_m8 = add_commas(count_m8)
        data['PropertyCountM8'] = count_m8
    
        count_ts = lines[31] #32
        count_ts = add_commas(count_ts)
        data['PropertyCountTS'] = count_ts
    
        count_tp = lines[32] #33
        count_tp = add_commas(count_tp)
        data['PropertyCountTP'] = count_tp
    
        count_tm = lines[33] #34
        count_tm = add_commas(count_tm)
        data['PropertyCountTM'] = count_tm
    
        count_tl = lines[34] #35
        count_tl = add_commas(count_tl)
        data['PropertyCountTL'] = count_tl
    
        count_station = lines[35] #36
        count_station = add_commas(count_station)
        data['PropertyCountStation'] = count_station
    
        count_sat = lines[36] #37
        count_sat = add_commas(count_sat)
        data['PropertyCountSatellite'] = count_sat
    
        trade_percent = lines[37] #38
        data['TradeRankPercent'] = trade_percent
    
        trade_title = lines[38] #39
        data['TradeRankTitle'] = trade_title
    
        fight_percent = lines[39] #40
        data['FightRankPercent'] = fight_percent
    
        fight_title = lines[40] #41
        data['FightRankTitle'] = fight_title
    
        flc_rank = lines[41] #42
        flc_percent = calc_flc(int(flc_rank))
        flc_percent = round(flc_percent, 5)
        data['FLCPercent'] = flc_percent

        blank = lines[42] #43

    return data

# displays data with snazzy colors and line art
def display(data):
    print(chr(27) + "[2J") # clears terminal
    print("\033[90m╭╼\033[97;3;1m Litcube's Universe \033[90m╾╮\033[00m",
        "\033[90m├──────────────────────┴───────────────────────────╼\033[00m",
        "\033[90m│ \033[97mCredits\033[00m:\t{}".format(data['Credits']),
        "\033[90m│ \033[97mTrade Rank\033[00m:\t{}%\t{}".format(data['TradeRankPercent'],data['TradeRankTitle']),
        "\033[90m│ \033[97mFight Rank\033[00m:\t{}%\t{}".format(data['FightRankPercent'],data['FightRankTitle']),
        "\033[90m│ \033[97mF.L.C.\033[00m:\t{}%".format(data['FLCPercent']),
        "\033[90m│ \033[97mPlay Time\033[00m:\t{}".format(data['PlayTime']),
        "\033[90m│ \033[97mReal Time\033[00m:\t{}".format(data['RealTime']),
        "\033[90m├──────────────────────────────╼\033[00m",
        "\033[90m│ \033[94mArgon\033[00m:\t{}%\t{}".format(data['NotorietyPercentArgon'],data['NotorietyTitleArgon']),
        "\033[90m│ \033[92mBoron\033[00m:\t{}%\t{}".format(data['NotorietyPercentBoron'],data['NotorietyTitleBoron']),
        "\033[90m│ \033[33mParanid\033[00m:\t{}%\t{}".format(data['NotorietyPercentParanid'],data['NotorietyTitleParanid']),
        "\033[90m│ \033[35mSplit\033[00m:\t{}%\t{}".format(data['NotorietyPercentSplit'],data['NotorietyTitleSplit']),
        "\033[90m│ \033[93mTeladi\033[00m:\t{}%\t{}".format(data['NotorietyPercentTeladi'],data['NotorietyTitleTeladi']),
        "\033[90m│ \033[34mGoner\033[00m:\t{}%\t{}".format(data['NotorietyPercentGoner'],data['NotorietyTitleGoner']),
        "\033[90m│ \033[36mTerran\033[00m:\t{}%\t{}".format(data['NotorietyPercentTerran'],data['NotorietyTitleTerran']),
        "\033[90m│ \033[36mATF\033[00m:\t\t{}%\t{}".format(data['NotorietyPercentATF'],data['NotorietyTitleATF']),
        "\033[90m│ \033[31mPirates\033[00m:\t{}%\t{}".format(data['NotorietyPercentPirates'],data['NotorietyTitlePirates']),
        "\033[90m│ \033[95mYaki\033[00m:\t\t{}%\t{}".format(data['NotorietyPercentYaki'],data['NotorietyTitleYaki']),
        "\033[90m├──────────╼\033[00m",
        "\033[90m│ \033[32mM5\033[00m:\t{}\t\t\033[32mM1\033[00m:\t{}".format(data['PropertyCountM5'],data['PropertyCountM1']),
        "\033[90m│ \033[32mM4\033[00m:\t{}\t\t\033[32mM2\033[00m:\t{}".format(data['PropertyCountM4'],data['PropertyCountM2']),
        "\033[90m│ \033[32mM3\033[00m:\t{}\t\t\033[32mTS\033[00m:\t{}".format(data['PropertyCountM3'],data['PropertyCountTS']),
        "\033[90m│ \033[32mM6\033[00m:\t{}\t\t\033[32mTP\033[00m:\t{}".format(data['PropertyCountM6'],data['PropertyCountTP']),
        "\033[90m│ \033[32mM8\033[00m:\t{}\t\t\033[32mTL\033[00m:\t{}".format(data['PropertyCountM8'],data['PropertyCountTL']),
        "\033[90m│ \033[32mM7\033[00m:\t{}\t\t\033[32mSt\033[00m:\t{}".format(data['PropertyCountM7'],data['PropertyCountStation']),
        "\033[90m│ \033[32mTM\033[00m:\t{}\t\t\033[32mSat\033[00m:\t{}".format(data['PropertyCountTM'],data['PropertyCountSatellite']),
        "\033[90m╰╼\033[00m",
        sep='\n')

def main():
    # loop or die
    while True:
        display(data=get_stats(log_file))
        sleep(interval)

if __name__ == "__main__":
    main()

# vim: set ft=python:
