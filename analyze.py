#!/usr/bin/env python
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

TASK_NAME = 'tau'
rex_switch = re.compile ('^.*\[(\d+)\] [^\s]+\s+([^\s]+): sched_switch: prev_comm=([^\s]+) prev_pid=([^\s]+) prev_prio=([^\s]+) prev_state=([^\s]+) ==> next_comm=([^\s]+) next_pid=([^\s]+) next_prio=([^\s]+)$')

def populate_task (match, index):
    task = {}
    task ['name'] = match.group (index)
    task ['pid'] = int (match.group (index + 1))
    task ['prio'] = int (match.group (index + 2))
    try:
        task ['state'] = match.group (index + 3)
    except:
        pass

    return task

def get_switch_params (match):
    params = {}
    timestamp = float (match.group (2)) * 1000
    params ['cpu'] = int (match.group (1))
    params ['prev'] = populate_task (match, 3)
    params ['next'] = populate_task (match, 7)

    return timestamp, params

def parse (filename):
    data = {}

    with open (filename, 'r') as fdi:
        for line in fdi:
            match_switch = rex_switch.match (line)

            if match_switch:
                ts, params = get_switch_params (match_switch)

                if TASK_NAME in params ['prev']['name'] or \
                    TASK_NAME in params ['next']['name']:
                    data [ts] = params

    return data

def get_cpu_timelines (data):
    cpu_events = {}

    for ts in data.keys ():
        cpu = data [ts]['cpu']
        if (cpu not in cpu_events.keys ()):
            cpu_events [cpu] = {}
        cpu_events [cpu][ts] = data [ts]

    return cpu_events

def get_task_timelines (data):
    task_events = {}

    for ts in data.keys ():
        prev_task = data [ts]['prev']['name']
        next_task = data [ts]['next']['name']

        for task in [prev_task, next_task]:
            if (task not in task_events.keys ()):
                task_events [task] = {}

            task_events [task][ts] = data [ts]

    return task_events

colors = {'tau_1': 'r', 'tau_2': 'g', 'tau_3': 'b'}
def plot_cpu_timelines (cpus, filter_cpus):
    fig, ax = plt.subplots (1)

    startTime = 10**10
    endTime = 0

    prev_cpu = 1
    ylabels = []
    yticks = []
    for cpu in cpus.keys ():
        if cpu in filter_cpus:
            pass
        tss = sorted (cpus [cpu].keys ())
        events = cpus [cpu]

        startTime = tss [0] if tss [0] < startTime else startTime
        endTime = tss [-1] if tss [-1] > endTime else endTime

        for idx in xrange (len (tss) - 1):
            nextTask = events [tss [idx]]['next']

            if TASK_NAME in nextTask ['name']:
                duration = tss [idx + 1] - tss [idx]
                rect = patches.Rectangle ((tss [idx], prev_cpu), duration, 0.5, linewidth = 0, edgecolor = 'k', facecolor = colors [nextTask ['name']])
                ax.add_patch (rect)
                rect = patches.Rectangle ((tss [idx], 4), duration, (1 - 0.05 * prev_cpu), linewidth = 0, edgecolor = 'k', facecolor = colors [nextTask ['name']])
                ax.add_patch (rect)

        yticks.append (prev_cpu + 0.25)
        ylabels.append ('CPU-%d' % cpu)
        prev_cpu += 1

    yticks.append (yticks [-1] + 1.25)
    ylabels.append ('Cumulative')
    plt.yticks (yticks)
    ax.set_yticklabels (ylabels, rotation = 90, fontweight = 'bold')
    plt.xlim (startTime, endTime)
    plt.ylim (0.5, 6.5)
    plt.grid (True)
    plt.show ()

    return

def plot_task_timelines (tasks, select_tasks):
    fig, ax = plt.subplots (1)

    startTime = 10**10
    endTime = 0

    prev = 1
    ylabels = []
    yticks = []
    for task in tasks.keys ():
        if task not in select_tasks:
            continue

        tss = sorted (tasks [task].keys ())
        events = tasks [task]

        startTime = tss [0] if tss [0] < startTime else startTime
        endTime = tss [-1] if tss [-1] > endTime else endTime

        for idx in xrange (len (tss) - 1):
            nextTask = events [tss [idx]]['next']

            if task in nextTask ['name']:
                duration = tss [idx + 1] - tss [idx]
                rect = patches.Rectangle ((tss [idx], prev), duration, 0.5, linewidth = 0, edgecolor = 'k', facecolor = colors [nextTask ['name']])
                ax.add_patch (rect)
                rect = patches.Rectangle ((tss [idx], 4), duration, (1 - 0.05 * prev), linewidth = 0, edgecolor = 'k', facecolor = colors [nextTask ['name']])
                ax.add_patch (rect)

        yticks.append (prev + 0.25)
        ylabels.append (task.upper ())
        prev += 1

    yticks.append (yticks [-1] + 1.25)
    ylabels.append ('Cumulative')
    plt.yticks (yticks)
    ax.set_yticklabels (ylabels, rotation = 90, fontweight = 'bold')
    plt.xlim (startTime, endTime)
    plt.ylim (0.5, 6.5)
    plt.grid (True)
    plt.show ()

    return

def main ():
    filename = 'profile.dat'
    data = parse (filename)

    # cpus = get_cpu_timelines (data)
    # filter_cpus = [0,1,2]
    # plot_cpu_timelines (cpus, filter_cpus)

    tasks = get_task_timelines (data)
    select_tasks = ['tau_%d' % x for x in [1,2,3]]
    plot_task_timelines (tasks, select_tasks)

    return

if __name__ == '__main__':
    main ()
