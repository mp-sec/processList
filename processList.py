#!usr/bin/python3

# Filename: m4p2.py
# Author: Mandeep Parihar
# Course: ITSC-204
# Details: A program that collects a list of all running processes and then prompts the user which process they wish to see in detail.
# Resources: Maybe one day I will stop closing all of the things I look up before realizing I can't add them here.

import os
import psutil


class LinuxProcList:
    def __init__(self, name, pid, ppid):
        self.name = name
        self.pid = pid
        self.ppid = ppid

    def get_attr(self, name, pid, ppid):
        return name, pid, ppid,

    def set_attr(self, name, pid, ppid):
        self.name = name
        self.pid = pid
        self.ppid = ppid

    def proc_list(self, curr_proc_list):
        return curr_proc_list

    def command_line(self, pid):
        with open("/proc/" + pid + "/cmdline", "r") as reader:
            cmdline_string = reader.read()

        # https://stackoverflow.com/a/9573259
        # Empty strings are falsy, so the below line simply checks if the variable returns false
        if not cmdline_string:
            return "None"
        else:
            return cmdline_string

    def children(self, pid):
        proc_children = psutil.Process(pid)
        children = proc_children.children()
        children_list = []

        for child in children:
            # Self is used to call a method in the same class
            child_cmdline = self.command_line(str(child.pid))
            child_name = child.name()
            print("\t", child_name, ":\t", child.pid, ",", child_cmdline, sep="")
            children_list.append(child_name)

        print("\nRaw list of child processes:")
        return children_list


quit_flag = 0

while quit_flag == 0:
    proc_ids = [proc_id for proc_id in os.listdir("/proc") if proc_id.isdigit()]
    print("This is a list of all currently running processes on the system:\n\t", proc_ids)
    proc_select = input("Select a process you wish to view more information for: ")

    # Checks if the user entry is a numerical string value
    if proc_select.isnumeric():
        print("")
        pass
    else:
        print("Invalid process selection made. Exiting program.")
        quit()

    with open("/proc/" + proc_select + "/stat", "r") as stat_reader:
        stat_collector = stat_reader.read()
        stat_reader_list = stat_collector.split(" ")

        proc_name = stat_reader_list[1].strip("(").strip(")")
        proc_pid = stat_reader_list[0]
        proc_ppid = stat_reader_list[3]

        proc = LinuxProcList(proc_name, proc_pid, proc_ppid)
        proc.proc_list(proc_ids)

        print("PID:", proc_pid)
        print("PPID:", proc_ppid)
        print("Process Name:", proc_name)
        cmdline_call = proc.command_line(proc_select)
        print("Process cmdline:", cmdline_call)
        print("Process children:")
        children_call = proc.children(int(proc_select))
        print(children_call)

        continue_prompt = input("\nDo you wish to see the details of another process? [Y/N] ")

        if continue_prompt == "N" or continue_prompt == "n":
            quit_flag = 1
        elif continue_prompt == "Y" or continue_prompt == "y":
            print("")
            pass
        else:
            print("Invalid entry made. Exiting program.")
            quit()
