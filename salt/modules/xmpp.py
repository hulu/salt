# -*- coding: utf-8 -*-
'''
Module for Sending Messages via XMPP (a.k.a. Jabber)

.. versionadded:: 2014.1.0 (Hydrogen)

:depends:   - sleekxmpp python module
:configuration: This module can be used by either passing a jid and password
    directly to send_message, or by specifying the name of a configuration
    profile in the minion config, minion pillar, or master config.

    For example:

    .. code-block:: yaml

        my-xmpp-login:
            xmpp.jid: myuser@jabber.example.org/resourcename
            xmpp.password: verybadpass

    The resourcename refers to the resource that is using this account. It is
    user-definable, and optional. The following configurations are both valid:

    .. code-block:: yaml

        my-xmpp-login:
            xmpp.jid: myuser@jabber.example.org/salt
            xmpp.password: verybadpass

        my-xmpp-login:
            xmpp.jid: myuser@jabber.example.org
            xmpp.password: verybadpass

'''

HAS_LIBS = False
try:
    from sleekxmpp import ClientXMPP as _ClientXMPP
    HAS_LIBS = True
except ImportError:
    class _ClientXMPP(object):
        '''
        Fake class in order not to raise errors
        '''


__virtualname__ = 'xmpp'


def __virtual__():
    '''
    Only load this module if sleekxmpp is installed on this minion.
    '''
    if HAS_LIBS:
        return __virtualname__
    return False


class SendMsgBot(_ClientXMPP):

    def __init__(self, jid, password, recipient, msg):  # pylint: disable=E1002
        # PyLint wrongly reports an error when calling super, hence the above
        # disable call
        super(SendMsgBot, self).__init__(jid, password)

        self.recipient = recipient
        self.msg = msg

        self.add_event_handler('session_start', self.start)  # pylint: disable=E1101

    def start(self, event):  # pylint: disable=W0613
        self.send_presence()  # pylint: disable=E1101

        self.send_message(mto=self.recipient,  # pylint: disable=E1101
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect(wait=True)  # pylint: disable=E1101


def send_msg(recipient, message, jid=None, password=None, profile=None):
    '''
    Send a message to an XMPP recipient. Designed for use in states.

    CLI Examples::

        xmpp.send_msg 'admins@xmpp.example.com' 'This is a salt module test' \
            profile='my-xmpp-account'
        xmpp.send_msg 'admins@xmpp.example.com' 'This is a salt module test' \
            jid='myuser@xmpp.example.com/salt' password='verybadpass'
    '''
    if profile:
        creds = __salt__['config.option'](profile)
        jid = creds.get('xmpp.jid')
        password = creds.get('xmpp.password')

    xmpp = SendMsgBot(jid, password, recipient, message)
    xmpp.register_plugin('xep_0030')  # pylint: disable=E1101
    xmpp.register_plugin('xep_0199')  # pylint: disable=E1101

    if xmpp.connect():  # pylint: disable=E1101
        xmpp.process(block=True)  # pylint: disable=E1101
        return True
    return False
