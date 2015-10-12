#coding: utf-8
import json
import os

base_dir = '/home/room/server'

add_server_info=[
    {
        "MsgServerIP" : '192.168.0.32',
        "MsgServerPort" : 11038
    },
    {
        "MsgServerIP" : '192.168.0.16',
        "MsgServerPort" : 11039
    },
    {
        "MsgServerIP" : '192.168.0.18',
        "MsgServerPort" : 11040
    },
    {
        "MsgServerIP" : '192.168.0.19',
        "MsgServerPort" : 11041
    },
    {
        "MsgServerIP" : '192.168.0.31',
        "MsgServerPort" : 11042
    },
]


def get_msg_config(base_dir):
    configs = []
    for name in os.listdir(base_dir):
        if 'MsgServer' in name and os.path.isdir(os.path.join(base_dir,name)):
            config_path = os.path.join(base_dir,name,'config.json')
            configs.append(config_path)
    return configs

def modify_config(configs,add_server_info):
    for config_file in configs:
        jsonloads = json.load(open(config_file,'r+'))
        for single_server in add_server_info:
            if single_server not in jsonloads["server_list"]:
                jsonloads["server_list"].append(single_server)
        json.dump(jsonloads,open(config_file,'w'),indent=4)
        print '%s was modified success!' % config_file


if __name__ == '__main__':
    configs = get_msg_config(base_dir)
    modify_config(configs,add_server_info)
