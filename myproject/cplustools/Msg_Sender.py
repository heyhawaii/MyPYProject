#!/usr/bin/env python
# -*- coding: cp936 -*-
import string
import struct
import socket,time
import random
import xlrd
import os


class Byte:
    length=0
    byte=''
    byte1=''
    def reset(self):
        self.length=0
        self.byte=''
    def get_byte(self):
        return self.byte
    def get_length(self):
        return self.length
    def write_char(self,string,len1=None):
        slen=len(string)
        self.length+=slen
        Ascii_list=map(ord,string)
        #print Ascii_list
        for i in Ascii_list:
            #print i
            self.byte+=struct.pack('b',i)
        if type(len1)==int and len1>slen:
            temp_len=len1-slen
            for i in range(0,temp_len):
                self.byte+=struct.pack('b',0)
                self.length+=1
        self.byte+=struct.pack('b',0)
        self.length+=1
        
    def write_int32(self,integer):
        self.length+=4
        self.byte+=struct.pack('I',integer)
    def write_int16(self,integer):
        self.length+=2
        self.byte+=struct.pack('H',integer)
    def write_int8(self,integer):
        self.length+=1
        self.byte+=struct.pack('L',integer)



class Msg_rpc(Byte):
    def __init__(self):
        self._socket = 0
        self._port = 11010
        self._host = '192.168.0.10'
        self._session_id = 0 #登录后的会话ID
        self._uid=random.randrange(100000000,1000000000)
        self._code = 0
        self.cmd=()
        self._header_len = 8
        self._last_action=''
        self.CODE_LOGIN = 901  #登录请求码
        self.CODE_LOGIN_REPLY = 951 #登录请求返回码
        self.CODE_MESSAGE = 912 #发送数据消息请求
        self.CODE_RPC_SEND = 913 #R
        self.CODE_RPC_REPLY = 914 #RPC协议回复
        #self.Setip('192.168.0.10',11010)
        #self.Setip('192.168.5.4',11001)
        #self.Mysocket()
        self.Login(self._uid,"username"+str(self._uid),"username"+str(self._uid))
        #self.Login(self._uid,"username"+str(self._uid),"username"+str(self._uid))
        #def Setip(self,host,port):
        #self._host=host
        #self._port=port
    def Mysocket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(10)
        socket.setdefaulttimeout(20)
        result=self._socket.connect((self._host, self._port))
    def Close(self):
            self._socket.close()
    def Send(self,is_reply=False):
        if not self._socket:
            print "socket wei connection\r\n"
        #if self._code != self.CODE_LOGIN and not self._session_id:
        #    print "socket Error\r\n"
        self.write_int16(0)
        result=self._socket.send(self.get_header()+self.get_byte())
        self.reset()
        if not result:
            print "发送信息失败\r\n"
        if is_reply==True:
            return self.Read()
        else:
            return True
    def Read(self):
        #if not self._socket:
        #    print "socket连接中断\r\n"
        if self._socket:
            data=self._socket.recv(4)
            if data:
                ll=struct.unpack('I',data)
                le=ll[0]
                return self.Pack_doing(self._socket.recv(le))
    def Pack_doing(self,data):
        self.cmd=()
        code=struct.unpack('H',data[4:6])
        if code[0]==self.CODE_LOGIN_REPLY:
            temp=struct.unpack('Q',data[8:])
            self._session_id=temp[0]
        #print "session_id:"+str(self._session_id)
        if code[0]==self.CODE_RPC_REPLY:
            fmt='%ds' %(len(data[8:])-struct.calcsize('3I'))
            #self.cmd=struct.unpack('3I',data[8:20])
            temp=struct.unpack(fmt,data[20:])
            #print "\r\n cmd:"+str(self.cmd)+"\r\n"
            #print "\r\n temp:"+temp[0]+"\r\n"

            return self.decode(temp[0])
    def code(self,code):
            self._code=int(code)
    def get_login(self):
            return self._session_id
    def get_header(self):
        self.length+=8
        self.byte1=struct.pack('I',self.length)+struct.pack('I',self.length)+struct.pack('H',self._code)+struct.pack('H',0)
        return self.byte1
    def Login(self,uid, username,password):
        self.code(self.CODE_LOGIN)
        self.write_int32(uid)
        self.write_char(username,32)
        self.write_char(username,32)
        self.Mysocket()
        self.Send(True)
        return self._session_id
    def Rpc(self,func_name,data,server_id=0):
        tag=random.randrange(100000,1000000000)
        self.code(self.CODE_RPC_SEND)
        self.write_int32(self._uid)
        self.write_int32(tag)
        self.write_int32(server_id)
        self.write_char(func_name,127)
        if data:
            #print "\r\ndata"+self.encode(data)
            self.write_char(self.encode(data))
        self._last_action=func_name
        return self.Send(True)
    def encode(self,dic,type=2):
        if type==1:
            return self._encode1(dic)
        else:
            return self._encode2(dic)
    def _encode1(self,dic):
        st=''
        comm=''
        for v in dic.values():
            if type(v)==dict:
                v['value']='/'.join(v.values())
            st+=comm
            st+=(self.filter1(v['key'])+'@=') if v['key']!=None else ''
            st+=self.filter1(v['value'])
    def _encode2(self,dic):
        st=''
        comm=''
        for (k,v) in dic.items():
            if type(v)==dict:
                v='/'.join(v.values())
            st+=comm
            st+= (self.filter1(k)+'@=') if k!=None else ''
            st+=self.filter1(v)
            comm='/'
        return st
    def filter1(self,strr,encode=True):
        strr=strr.strip()
        if strr=='':
            return strr
        if encode==True:
            strr1=strr.replace('@','@A')
            strr2=strr1.replace('/','@S')
            return strr2
        else:
            strr1=strr.replace('@S','/')
            strr2=strr1.replace('@A','@')
            return strr2
    def decode(self,strr,type=1):
        strr=strr.strip()
        if strr=='':
            return strr
        st_list=strr.split('/')
        result={}
        for v in st_list:
            if v.count('@=')!=0:
                st_list2=v.split('@=')
                key=self.filter1(st_list2[0],False)
                value=self.filter1(st_list2[1],False)
                result[key]=value
            else:
                key=None
            i=0
            for vv in self.cmd:
                result[i]=vv
                i+=1
        return result
    def send_phone_msg(self, phone, msg):
        if not phone and not msg:
            return False
        data=self.Rpc('send_phone_message',{'phone':phone,'msg':msg},48001)
        #print "\r\ndonate_room data:"+str(data)
        return data

# print Msg_rpc().send_phone_msg('180866698030','1')