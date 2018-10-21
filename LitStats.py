#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, re
import traceback
import curses

#from datetime import datetime
from time import sleep
from math import floor
from collections import deque
from textwrap import wrap

INTERVAL = 1
LOG_STATS = '~/.config/EgoSoft/X3AP/log09004.txt'
LOG_ALERT = '~/.config/EgoSoft/X3AP/log06689.txt'

DEBUG = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--debug':
        DEBUG = True

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


def get_elapsed(dtime):
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

def set_color_pair(n,nmax):
    """Return color_pair number based on percentage"""
    if n == 0: n = 1
    perc = 100 * float(n)/float(nmax)
    if perc >= 75: color = 7 # cyan
    elif perc < 75 and perc >= 50: color = 3 # green
    elif perc < 50 and perc >= 25: color = 4 # yellow
    else: color = 8 # white
    return color

def get_alert(file):
    """Return message as list of lines"""
    alert = []
    file = os.path.expanduser(file)
    with open(file) as fp:
        dq = deque(fp, 24)
        for i in dq:
            alert.append(i.strip('\n'))
    return alert[1:-2]

def wrap_alert(data,max_x):
    """Check line length, split into two lines if too wide"""
    new_data = []
    for line in data:
        if len(line) > max_x:
            for clip in wrap(line,max_x-2):
                new_data.append(clip)
        else:
            new_data.append(line)
    return new_data

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

def stat_win(win,max_y,max_x,show_alert=None):
    """Draw stat window with fields"""
    win.erase()
    stat = win.subpad(0,0)
#    stat.box()

    stat.hline(0,1,curses.ACS_HLINE,max_x-2)
    stat.addstr(0,3," Litcube's Universe ",curses.color_pair(7)|curses.A_BOLD)
    if show_alert:
        stat.addstr(0,max_x-10," ALERT ",curses.color_pair(2)|curses.A_BOLD)

    stat.addstr(1,2,"Credits",curses.color_pair(8)|curses.A_BOLD)
    stat.addstr(2,2,"Trade Rank",curses.color_pair(8)|curses.A_BOLD)
    stat.addstr(3,2,"Combat Rank",curses.color_pair(8)|curses.A_BOLD)
    stat.addstr(4,2,"Loot Chance",curses.color_pair(8)|curses.A_BOLD)
    stat.addstr(5,2,"Play Time",curses.color_pair(8)|curses.A_BOLD)
    stat.addstr(6,2,"Real Time",curses.color_pair(8)|curses.A_BOLD)

    stat.hline(7,1,curses.ACS_HLINE,max_x-2)
    stat.addstr(7,3," Factions ",curses.color_pair(8)|curses.A_BOLD)

    stat.addstr(8,2,"Argon",curses.color_pair(5)|curses.A_BOLD)
    stat.addstr(9,2,"Boron",curses.color_pair(3)|curses.A_BOLD)
    stat.addstr(10,2,"Paranid",curses.color_pair(2)|curses.A_BOLD)
    stat.addstr(11,2,"Split",curses.color_pair(6)|curses.A_BOLD)
    stat.addstr(12,2,"Teldai",curses.color_pair(4)|curses.A_BOLD)
    stat.addstr(13,2,"Terran",curses.color_pair(7)|curses.A_BOLD)
    stat.addstr(14,2,"ATF",curses.color_pair(7)|curses.A_BOLD)
    stat.addstr(15,2,"Goner",curses.color_pair(5)|curses.A_BOLD)
    stat.addstr(16,2,"Yaki",curses.color_pair(6)|curses.A_BOLD)
    stat.addstr(17,2,"Pirates",curses.color_pair(2)|curses.A_BOLD)

    stat.hline(18,1,curses.ACS_HLINE,max_x-2)
    stat.addstr(18,3," Properties ",curses.color_pair(8)|curses.A_BOLD)

    stat.addstr(19,2,"M5",curses.color_pair(3))
    stat.addstr(20,2,"M4",curses.color_pair(3))
    stat.addstr(21,2,"M3",curses.color_pair(3))
    stat.addstr(22,2,"M6",curses.color_pair(3))

    stat.addstr(19,14,"M8",curses.color_pair(3))
    stat.addstr(20,14,"M7",curses.color_pair(3))
    stat.addstr(21,14,"M1",curses.color_pair(3))
    stat.addstr(22,14,"M2",curses.color_pair(3))

    stat.addstr(19,26,"TM",curses.color_pair(3))
    stat.addstr(20,26,"TS",curses.color_pair(3))
    stat.addstr(21,26,"TP",curses.color_pair(3))
    stat.addstr(22,26,"TL",curses.color_pair(3))

    stat.addstr(19,38,"St",curses.color_pair(3))
    stat.addstr(20,38,"Sat",curses.color_pair(3))

    stat.refresh(0,0,0,0,max_y+1,max_x+1)

    return stat

def write_stats(win,max_y,max_x):
    """Format and write out stats"""
    data = get_stats(LOG_STATS)

    if data:
        credits = add_commas(data['credits'])
        win.addstr(1,16,credits,curses.color_pair(4)|curses.A_BOLD)

        trade_rank, trade_title = get_rank_title(data['trade_title'])
        trade_perc = data['trade_perc']
        rank = set_color_pair(trade_rank,30)
        perc = set_color_pair(trade_perc,100)
        win.addnstr(2,16,trade_rank,2,curses.color_pair(rank))
        win.addnstr(2,20,trade_perc+'%',4,curses.color_pair(perc))
        win.addnstr(2,25,trade_title,max_x-5)

        combat_rank, combat_title = get_rank_title(data['combat_title'])
        combat_perc = data['combat_perc']
        rank = set_color_pair(combat_rank,30)
        perc = set_color_pair(combat_perc,100)
        win.addnstr(3,16,combat_rank,2,curses.color_pair(rank))
        win.addnstr(3,20,combat_perc+'%',4,curses.color_pair(perc))
        win.addnstr(3,25,combat_title,max_x-5)

        flc_perc = get_flc_perc(int(data['flc_rank']))
        flc_perc = str(flc_perc) 
        perc = set_color_pair(flc_perc,100)
        win.addnstr(4,16,flc_perc+'%',max_x-21,curses.color_pair(perc))

        time_played = get_elapsed(int(data['time_played']))
        win.addnstr(5,16,time_played,max_x-21)

        time_real = get_elapsed(int(data['time_real']))
        win.addnstr(6,16,time_real,max_x-21)

        argon_rank, argon_title = get_rank_title(data['argon_title'])
        argon_perc = data['argon_perc']
        rank = set_color_pair(argon_rank,10)
        perc = set_color_pair(argon_perc,100)
        win.addnstr(8,16,argon_rank,2,curses.color_pair(rank))
        win.addnstr(8,20,argon_perc+'%',4,curses.color_pair(perc))
        win.addnstr(8,25,argon_title,max_x-26)

        boron_rank, boron_title = get_rank_title(data['boron_title'])
        boron_perc = data['boron_perc']
        rank = set_color_pair(boron_rank,10)
        perc = set_color_pair(boron_perc,100)
        win.addnstr(9,16,boron_rank,2,curses.color_pair(rank))
        win.addnstr(9,20,boron_perc+'%',4,curses.color_pair(perc))
        win.addnstr(9,25,boron_title,max_x-26)

        paranid_rank, paranid_title = get_rank_title(data['paranid_title'])
        paranid_perc = data['paranid_perc']
        rank = set_color_pair(paranid_rank,10)
        perc = set_color_pair(paranid_perc,100)
        win.addnstr(10,16,paranid_rank,2,curses.color_pair(rank))
        win.addnstr(10,20,paranid_perc+'%',4,curses.color_pair(perc))
        win.addnstr(10,25,paranid_title,max_x-26)

        split_rank, split_title = get_rank_title(data['split_title'])
        split_perc = data['split_perc']
        rank = set_color_pair(split_rank,10)
        perc = set_color_pair(split_perc,100)
        win.addnstr(11,16,split_rank,2,curses.color_pair(rank))
        win.addnstr(11,20,split_perc+'%',4,curses.color_pair(perc))
        win.addnstr(11,25,split_title,max_x-26)

        teladi_rank, teladi_title = get_rank_title(data['teladi_title'])
        teladi_perc = data['teladi_perc']
        rank = set_color_pair(teladi_rank,10)
        perc = set_color_pair(teladi_perc,100)
        win.addnstr(12,16,teladi_rank,2,curses.color_pair(rank))
        win.addnstr(12,20,teladi_perc+'%',4,curses.color_pair(perc))
        win.addnstr(12,25,teladi_title,max_x-26)

        terran_rank, terran_title = get_rank_title(data['terran_title'])
        terran_perc = data['terran_perc']
        rank = set_color_pair(terran_rank,10)
        perc = set_color_pair(terran_perc,100)
        win.addnstr(13,16,terran_rank,2,curses.color_pair(rank))
        win.addnstr(13,20,terran_perc+'%',4,curses.color_pair(perc))
        win.addnstr(13,25,terran_title,max_x-26)

        atf_rank, atf_title = get_rank_title(data['atf_title'])
        atf_perc = data['atf_perc']
        rank = set_color_pair(atf_rank,10)
        perc = set_color_pair(atf_perc,100)
        win.addnstr(14,16,atf_rank,2,curses.color_pair(rank))
        win.addnstr(14,20,atf_perc+'%',4,curses.color_pair(perc))
        win.addnstr(14,25,atf_title,max_x-26)

        goner_rank, goner_title = get_rank_title(data['goner_title'])
        goner_perc = data['goner_perc']
        rank = set_color_pair(goner_rank,10)
        perc = set_color_pair(goner_perc,100)
        win.addnstr(15,16,goner_rank,2,curses.color_pair(rank))
        win.addnstr(15,20,goner_perc+'%',4,curses.color_pair(perc))
        win.addnstr(15,25,goner_title,max_x-26)

        yaki_rank, yaki_title = get_rank_title(data['yaki_title'])
        yaki_perc = data['yaki_perc']
        rank = set_color_pair(yaki_rank,10)
        perc = set_color_pair(yaki_perc,100)
        win.addnstr(16,16,yaki_rank,2,curses.color_pair(rank))
        win.addnstr(16,20,yaki_perc+'%',4,curses.color_pair(perc))
        win.addnstr(16,25,yaki_title,max_x-26)

        pirates_rank, pirates_title = get_rank_title(data['pirates_title'])
        pirates_perc = data['pirates_perc']
        rank = set_color_pair(pirates_rank,10)
        perc = set_color_pair(pirates_perc,100)
        win.addnstr(17,16,pirates_rank,2,curses.color_pair(rank))
        win.addnstr(17,20,pirates_perc+'%',4,curses.color_pair(perc))
        win.addnstr(17,25,pirates_title,max_x-26)

        count_m5 = add_commas(data['count_m5'])
        win.addnstr(19,6,count_m5,6)
        count_m4 = add_commas(data['count_m4'])
        win.addnstr(20,6,count_m4,6)
        count_m3 = add_commas(data['count_m3'])
        win.addnstr(21,6,count_m3,6)
        count_m6 = add_commas(data['count_m6'])
        win.addnstr(22,6,count_m6,6)

        count_m8 = add_commas(data['count_m8'])
        win.addnstr(19,18,count_m8,6)
        count_m7 = add_commas(data['count_m7'])
        win.addnstr(20,18,count_m7,6)
        count_m1 = add_commas(data['count_m1'])
        win.addnstr(21,18,count_m1,6)
        count_m2 = add_commas(data['count_m2'])
        win.addnstr(22,18,count_m2,6)

        count_tm = add_commas(data['count_tm'])
        win.addnstr(19,30,count_tm,6)
        count_ts = add_commas(data['count_ts'])
        win.addnstr(20,30,count_ts,6)
        count_tp = add_commas(data['count_tp'])
        win.addnstr(21,30,count_tp,6)
        count_tl = add_commas(data['count_tl'])
        win.addnstr(22,30,count_tl,6)

        count_station = add_commas(data['count_station'])
        win.addnstr(19,42,count_station,6)
        count_sat = add_commas(data['count_sat'])
        win.addnstr(20,42,count_sat,6)

        win.refresh(0,0,0,0,max_y+1,max_x+1)

def alert_title(text):
    words = text.split(']')
    author = words[2].replace("[/green","")
    timestamp = words[4].replace("  "," ",2)

    if author and timestamp:
    #if author:
        #return " {} {} ".format(author.group(1),timestamp.group(1))
        #return " {} ".format(author.group(1))
#        return " {} {} ".format(author,timestamp)
        return author, timestamp
    return False

#def extract(line):
#    for asshole in line:
#    mo = re.search(r'\](.*)\[', s)
#    mo = re.search(r'\](.*)\[', mo)
#    if mo:
#        return mo.group(1)
#    return ''

def alert_win(win,max_y,max_x):
    """Draw message window"""
    alert = get_alert(LOG_ALERT)
    new_list = []
    if alert:
        row = 0
        win.erase()
        win = win.subpad(0,0)
        win.hline(0,1,curses.ACS_HLINE,max_x-1)
#        win.box()
        for line in wrap_alert(alert,max_x-1):
            if row == 0:
                author,timestamp = alert_title(line)
                alen = len(author)
                tlen = len(timestamp)
                win.addnstr(row,3," {} ".format(author),max_x-2,curses.color_pair(3))
                win.addnstr(row,alen+6," {} ".format(timestamp),max_x-2,curses.color_pair(2))
            else:
            	win.addnstr(row,1,line,max_x-2)
            row += 1
        win.refresh(0,0,0,0,max_y,max_x)


def main(win):
    """Setup curses and start loop"""
    win.nodelay(True)
    curses.start_color()
    curses.curs_set(False)

    curses.start_color()
    curses.use_default_colors()
    for i in range(1,16):
        curses.init_pair(i, i-1, -1)
    curses.init_pair(17,curses.COLOR_BLACK,curses.COLOR_RED)

    max_y,max_x = win.getmaxyx()
    cur_win = 1
    last_alert = None
    show_alert = False

    swin = curses.newpad(max_y,max_x)

    while True:

        max_y,max_x = win.getmaxyx()
        try:
            alert = get_alert(LOG_ALERT)
            if not alert == last_alert:
                last_alert = alert
                show_alert = True
        except:
            pass


        pressed = win.getch()
        curses.flushinp()

        if pressed == curses.KEY_RESIZE:
            win.erase()
            swin = curses.newpad(max_y,max_x)
            swin.refresh(0,0,0,0,max_y,max_x)

        if pressed != -1:
            try:
                key = str(chr(pressed))
            except:
                pass
            else:
                if key == ' ':
                    if cur_win == 1:
                        cur_win = 2
                    elif cur_win == 2:
                        cur_win = 1
                    pass
                if key == 'Q':
                    break

        if cur_win == 1:
            xwin = stat_win(swin,max_y,max_x,show_alert)
            write_stats(xwin,max_y,max_x)
        if cur_win == 2:
            xwin = alert_win(swin,max_y,max_x)
            show_alert = False
        swin.refresh(0,0,0,0,max_y,max_x)
        sleep(INTERVAL)

if __name__ == '__main__':
    curses.wrapper(main)
    #stdscr = curses.initscr()
    #main(stdscr)
