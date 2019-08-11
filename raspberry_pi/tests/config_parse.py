# -*- coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

dmux_a = int(config['pin_assign']['dmux_a'])
print(dmux_a)
# >> 11
dmux_para = list(map(int, config['dmux_setting']['para_abc'].split(',')))
print(dmux_para)
# >> [1, 0, 0]
