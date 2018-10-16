#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# LitStats.py - display stats from Litcube's Universe


import os, sys
import traceback
import curses

from time import sleep
from math import floor


__TIMER__ = 1
__INFILE__ = '~/.config/EgoSoft/X3AP/log09004.txt'


def add_commas(amount): 
    """Return comma separated numbers"""
    return ("{:,}".format(int(amount)))


def get_flc_perc(rank):
    """Calculate fightrank loot chance"""
    total = 1000000
    factor = 385
    chance = floor((rank * 100) / total) 
    x = floor((rank * 1000) / factor)
    chance = chance * floor(x / 1000)
    chance = chance / 10000
    return chance


def get_time_string(dtime):
    """Return time string"""
    days = floor(floor(floor(dtime/60)/60)/24)
    hours = floor(floor((dtime-((days*24)*60*60))/60)/60)
    minutes = floor((dtime-((((days*24)+hours)*60)*60))/60)
    seconds = dtime-(((((days*24)+hours)*60)+minutes)*60)
    days = str(int(float(days)))
    hours = str(int(float(hours)))
    minutes = str(int(float(minutes)))
    seconds = str(int(float(seconds)))
    if int(hours) < 10: hours = str.join('',('0',hours))
    if int(minutes) < 10: minutes = str.join('',('0',minutes))
    if int(seconds) < 10: seconds = str.join('',('0',seconds))
    return "{} Days, {}:{}:{}".format(days,hours,minutes,seconds)


def get_rank_title(title):
    """Split rank from title string, return (rank,title)"""
    return title.split(" - ")


def cp_scale(n,nmax):
    """Return color_pair number based on percentage"""
    if n == 0: n = 1
    perc = 100 * float(n)/float(nmax)
    if perc >= 80: color = 3 # green
    elif perc < 80 and perc >= 60: color = 7 # cyan
    elif perc < 60 and perc >= 40: color = 8 # white
    elif perc < 40 and perc >= 20: color = 4 # yellow
    else: color = 2 # red
    return color


def get_stats(file):
    """Reads log file, returns dict"""
    file = os.path.expanduser(file)
    with open(file) as fp:
        lines = fp.read().split('\n')
        lc = len(lines)
        if len(lines) < 42:
            return None
        data = {
            'credits':          lines[0],
            'time_played':      lines[1],
            'time_real':        lines[2],
            'argon_perc':       lines[3],
            'argon_title':      lines[4],
            'boron_perc':       lines[5],
            'boron_title':      lines[6],
            'split_perc':       lines[7],
            'split_title':      lines[8],
            'paranid_perc':     lines[9],
            'paranid_title':    lines[10],
            'teladi_perc':      lines[11],
            'teladi_title':     lines[12],
            'goner_perc':       lines[13],
            'goner_title':      lines[14],
            'terran_perc':      lines[15],
            'terran_title':     lines[16],
            'atf_perc':         lines[17],
            'atf_title':        lines[18],
            'pirates_perc':     lines[19],
            'pirates_title':    lines[20],
            'yaki_perc':        lines[21],
            'yaki_title':       lines[22],
            'count_m1':         lines[23],
            'count_m2':         lines[24],
            'count_m3':         lines[25],
            'count_m4':         lines[26],
            'count_m5':         lines[27],
            'count_m6':         lines[28],
            'count_m7':         lines[29],
            'count_m8':         lines[30],
            'count_ts':         lines[31],
            'count_tp':         lines[32],
            'count_tm':         lines[33],
            'count_tl':         lines[34],
            'count_station':    lines[35],
            'count_sat':        lines[36],
            'trade_perc':       lines[37],
            'trade_title':      lines[38],
            'combat_perc':      lines[39],
            'combat_title':     lines[40],
            'flc_rank':         lines[41],
        }
    return data


def write_stats(scr,width):
    """Format and write out stats"""
    data = get_stats(__INFILE__)

    if data is not None:
        credits = add_commas(data['credits'])
        scr.addstr(1,16,credits,curses.color_pair(4))

        trade_rank, trade_title = get_rank_title(data['trade_title'])
        trade_perc = data['trade_perc']
        rank = cp_scale(trade_rank,30)
        perc = cp_scale(trade_perc,100)
        scr.addnstr(2,16,trade_rank,2,curses.color_pair(rank))
        scr.addnstr(2,20,trade_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(2,25,trade_title,width-5)

        combat_rank, combat_title = get_rank_title(data['combat_title'])
        combat_perc = data['combat_perc']
        rank = cp_scale(combat_rank,30)
        perc = cp_scale(combat_perc,100)
        scr.addnstr(3,16,combat_rank,2,curses.color_pair(rank))
        scr.addnstr(3,20,combat_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(3,25,combat_title,width-5)

        flc_perc = get_flc_perc(int(data['flc_rank']))
        flc_perc = str(flc_perc) 
        perc = cp_scale(flc_perc,100)
        scr.addnstr(4,16,flc_perc+'%',width-21,curses.color_pair(perc))

        time_played = get_time_string(int(data['time_played']))
        scr.addnstr(5,16,time_played,width-21)

        time_real = get_time_string(int(data['time_real']))
        scr.addnstr(6,16,time_real,width-21)

        argon_rank, argon_title = get_rank_title(data['argon_title'])
        argon_perc = data['argon_perc']
        rank = cp_scale(argon_rank,10)
        perc = cp_scale(argon_perc,100)
        scr.addnstr(8,16,argon_rank,2,curses.color_pair(rank))
        scr.addnstr(8,20,argon_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(8,25,argon_title,width-26)

        boron_rank, boron_title = get_rank_title(data['boron_title'])
        boron_perc = data['boron_perc']
        rank = cp_scale(boron_rank,10)
        perc = cp_scale(boron_perc,100)
        scr.addnstr(9,16,boron_rank,2,curses.color_pair(rank))
        scr.addnstr(9,20,boron_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(9,25,boron_title,width-26)

        paranid_rank, paranid_title = get_rank_title(data['paranid_title'])
        paranid_perc = data['paranid_perc']
        rank = cp_scale(paranid_rank,10)
        perc = cp_scale(paranid_perc,100)
        scr.addnstr(10,16,paranid_rank,2,curses.color_pair(rank))
        scr.addnstr(10,20,paranid_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(10,25,paranid_title,width-26)

        split_rank, split_title = get_rank_title(data['split_title'])
        split_perc = data['split_perc']
        rank = cp_scale(split_rank,10)
        perc = cp_scale(split_perc,100)
        scr.addnstr(11,16,split_rank,2,curses.color_pair(rank))
        scr.addnstr(11,20,split_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(11,25,split_title,width-26)

        teladi_rank, teladi_title = get_rank_title(data['teladi_title'])
        teladi_perc = data['teladi_perc']
        rank = cp_scale(teladi_rank,10)
        perc = cp_scale(teladi_perc,100)
        scr.addnstr(12,16,teladi_rank,2,curses.color_pair(rank))
        scr.addnstr(12,20,teladi_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(12,25,teladi_title,width-26)

        terran_rank, terran_title = get_rank_title(data['terran_title'])
        terran_perc = data['terran_perc']
        rank = cp_scale(terran_rank,10)
        perc = cp_scale(terran_perc,100)
        scr.addnstr(13,16,terran_rank,2,curses.color_pair(rank))
        scr.addnstr(13,20,terran_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(13,25,terran_title,width-26)

        atf_rank, atf_title = get_rank_title(data['atf_title'])
        atf_perc = data['atf_perc']
        rank = cp_scale(atf_rank,10)
        perc = cp_scale(atf_perc,100)
        scr.addnstr(14,16,atf_rank,2,curses.color_pair(rank))
        scr.addnstr(14,20,atf_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(14,25,atf_title,width-26)

        goner_rank, goner_title = get_rank_title(data['goner_title'])
        goner_perc = data['goner_perc']
        rank = cp_scale(goner_rank,10)
        perc = cp_scale(goner_perc,100)
        scr.addnstr(15,16,goner_rank,2,curses.color_pair(rank))
        scr.addnstr(15,20,goner_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(15,25,goner_title,width-26)

        yaki_rank, yaki_title = get_rank_title(data['yaki_title'])
        yaki_perc = data['yaki_perc']
        rank = cp_scale(yaki_rank,10)
        perc = cp_scale(yaki_perc,100)
        scr.addnstr(16,16,yaki_rank,2,curses.color_pair(rank))
        scr.addnstr(16,20,yaki_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(16,25,yaki_title,width-26)

        pirates_rank, pirates_title = get_rank_title(data['pirates_title'])
        pirates_perc = data['pirates_perc']
        rank = cp_scale(pirates_rank,10)
        perc = cp_scale(pirates_perc,100)
        scr.addnstr(17,16,pirates_rank,2,curses.color_pair(rank))
        scr.addnstr(17,20,pirates_perc+'%',4,curses.color_pair(perc))
        scr.addnstr(17,25,pirates_title,width-26)

        count_m5 = add_commas(data['count_m5'])
        scr.addnstr(19,6,count_m5,6)
        count_m4 = add_commas(data['count_m4'])
        scr.addnstr(20,6,count_m4,6)
        count_m3 = add_commas(data['count_m3'])
        scr.addnstr(21,6,count_m3,6)
        count_m6 = add_commas(data['count_m6'])
        scr.addnstr(22,6,count_m6,6)

        count_m8 = add_commas(data['count_m8'])
        scr.addnstr(19,18,count_m8,6)
        count_m7 = add_commas(data['count_m7'])
        scr.addnstr(20,18,count_m7,6)
        count_m1 = add_commas(data['count_m1'])
        scr.addnstr(21,18,count_m1,6)
        count_m2 = add_commas(data['count_m2'])
        scr.addnstr(22,18,count_m2,6)

        count_tm = add_commas(data['count_tm'])
        scr.addnstr(19,30,count_tm,6)
        count_ts = add_commas(data['count_ts'])
        scr.addnstr(20,30,count_ts,6)
        count_tp = add_commas(data['count_tp'])
        scr.addnstr(21,30,count_tp,6)
        count_tl = add_commas(data['count_tl'])
        scr.addnstr(22,30,count_tl,6)

        count_station = add_commas(data['count_station'])
        scr.addnstr(19,42,count_station,6)
        count_sat = add_commas(data['count_sat'])
        scr.addnstr(20,42,count_sat,6)

        scr.refresh()


def window(scr,y,x):
    """Draw container and labels"""
    scr.erase()

    scr.box()

    scr.addstr(0,3," Litcube's Universe ",curses.color_pair(7)|curses.A_BOLD)

    scr.addstr(1,2,"Credits",curses.color_pair(8)|curses.A_BOLD)
    scr.addstr(2,2,"Trade Rank",curses.color_pair(8)|curses.A_BOLD)
    scr.addstr(3,2,"Combat Rank",curses.color_pair(8)|curses.A_BOLD)
    scr.addstr(4,2,"Loot Chance",curses.color_pair(8)|curses.A_BOLD)
    scr.addstr(5,2,"Play Time",curses.color_pair(8)|curses.A_BOLD)
    scr.addstr(6,2,"Real Time",curses.color_pair(8)|curses.A_BOLD)

    scr.hline(7,2,curses.ACS_HLINE,x-4)
    scr.addstr(7,3," Factions ",curses.color_pair(8)|curses.A_BOLD)

    scr.addstr(8,2,"Argon",curses.color_pair(5)|curses.A_BOLD)
    scr.addstr(9,2,"Boron",curses.color_pair(3)|curses.A_BOLD)
    scr.addstr(10,2,"Paranid",curses.color_pair(2)|curses.A_BOLD)
    scr.addstr(11,2,"Split",curses.color_pair(6)|curses.A_BOLD)
    scr.addstr(12,2,"Teldai",curses.color_pair(4)|curses.A_BOLD)
    scr.addstr(13,2,"Terran",curses.color_pair(7)|curses.A_BOLD)
    scr.addstr(14,2,"ATF",curses.color_pair(7)|curses.A_BOLD)
    scr.addstr(15,2,"Goner",curses.color_pair(5)|curses.A_BOLD)
    scr.addstr(16,2,"Yaki",curses.color_pair(6)|curses.A_BOLD)
    scr.addstr(17,2,"Pirates",curses.color_pair(2)|curses.A_BOLD)

    scr.hline(18,2,curses.ACS_HLINE,x-4)
    scr.addstr(18,3," Properties ",curses.color_pair(8)|curses.A_BOLD)

    scr.addstr(19,2,"M5",curses.color_pair(3))
    scr.addstr(20,2,"M4",curses.color_pair(3))
    scr.addstr(21,2,"M3",curses.color_pair(3))
    scr.addstr(22,2,"M6",curses.color_pair(3))

    scr.addstr(19,14,"M8",curses.color_pair(3))
    scr.addstr(20,14,"M7",curses.color_pair(3))
    scr.addstr(21,14,"M1",curses.color_pair(3))
    scr.addstr(22,14,"M2",curses.color_pair(3))

    scr.addstr(19,26,"TM",curses.color_pair(3))
    scr.addstr(20,26,"TS",curses.color_pair(3))
    scr.addstr(21,26,"TP",curses.color_pair(3))
    scr.addstr(22,26,"TL",curses.color_pair(3))

    scr.addstr(19,38,"St",curses.color_pair(3))
    scr.addstr(20,38,"Sat",curses.color_pair(3))

    scr.addstr(23,3," Press 'q' to quit ",curses.color_pair(1)|curses.A_BOLD)
    scr.refresh()


def loop(scr):
    """Call main window, watch for resize or getch"""
    scr.nodelay(1)
    y,x = scr.getmaxyx()
    window(scr,y,x)
    while 1:
        keypress = scr.getch()
        if keypress == curses.KEY_RESIZE:
            y,x = scr.getmaxyx()
            window(scr,y,x)
            scr.refresh()
        if keypress != -1:
            try:
                key = str(chr(keypress))
            except:
                pass
            else:
                if key.lower() == 'q':
                    break
        write_stats(scr,x)
        sleep(__TIMER__)


def main():
    """Setup curses and start loop()"""
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        curses.start_color()
        curses.use_default_colors()
        for i in range(1,16):
            curses.init_pair(i, i-1, -1)

        loop(stdscr)

        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()


if __name__=='__main__':
    main()

# vim: set ft=python:
