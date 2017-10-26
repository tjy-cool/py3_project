#!/usr/bin/env python
# Funtion:
# Filename:

import sys

import time

filename = 'NIVISA1550full.exe'
with open(filename, 'rb') as f:
    bytes = 0
    tol_bytes = 686531176
    send_percent = 0
    last_percent = 0
    for line in f:
        bytes += len(line)
        send_percent = bytes / tol_bytes
        if int(send_percent*100) != int(last_percent*100):
            sys.stdout.write('sending file %s: [' % filename + int(send_percent * 50) * '#' + '->'
                             + (50 - int(send_percent * 50)) * ' ' + ']' + str(int(send_percent * 100)) + '%\r')
            sys.stdout.flush()
            last_percent = send_percent
        if int(send_percent*100) == 100:
            sys.stdout.write('sending file %s: [' % filename + int(send_percent * 50) * '#' + '##'
                             + (50 - int(send_percent * 50)) * ' ' + ']' + str(int(send_percent * 100)) + '%\n')
            sys.stdout.flush()
    # print('\n')
    print(bytes)

#
# import sys
# class progressbar(object):
#     def __init__(self, finalcount, block_char='.'):
#         self.finalcount = finalcount
#         self.blockcount = 0
#         self.block = block_char
#         self.f = sys.stdout
#         if not self.finalcount: return
#         self.f.write('\n------------------ % Progress -------------------1\n')
#         self.f.write('    1    2    3    4    5    6    7    8    9    0\n')
#         self.f.write('----0----0----0----0----0----0----0----0----0----0\n')
#     def progress(self, count):
#         count = min(count, self.finalcount)
#         if self.finalcount:
#             percentcomplete = int(round(100.0*count/self.finalcount))
#             if percentcomplete < 1: percentcomplete = 1
#         else:
#             percentcomplete=100
#         blockcount = int(percentcomplete//2)
#         if blockcount <= self.blockcount:
#             return
#         for i in range(self.blockcount, blockcount):
#             self.f.write(self.block)
#         self.f.flush()
#         self.blockcount = blockcount
#         if percentcomplete == 100:
#             self.f.write("\n")
#
# if __name__ == "__main__":
#     from time import sleep
#     pb = progressbar(8, "*")
#     for count in range(1, 9):
#         pb.progress(count)
#         sleep(0.2)
#     pb = progressbar(100)
#     pb.progress(20)
#     sleep(0.3)
#     pb.progress(47)
#     sleep(0.3)
#     pb.progress(90)
#     sleep(0.3)
#     pb.progress(100)
#     print("testing 1:")
#     pb = progressbar(1)
#     pb.progress(1)