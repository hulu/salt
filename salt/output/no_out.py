# -*- coding: utf-8 -*-
'''
Display no output.
'''

def __virtual__():
    return 'quiet'

def output(ret):  # pylint: disable=W0613
    '''
    Don't display data. Used when you only are interested in the
    return.
    '''
    return ''
