# -*- coding: utf-8 -*-
#! /usr/bin/env python
import sys

if sys.platform == 'win32':
    from stallion.common.deamon.windows import run
elif sys.platform == 'linux2':
    from stallion.common.deamon.unix import run

if __name__ == '__main__':
    run()
