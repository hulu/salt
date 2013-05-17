'''
Manage SVN repositories
=======================

Manage repositiry checkouts via the svn vcs system:

.. code-block:: yaml

    http://unladen-swallow.googlecode.com/svn/trunk/:
      svn.latest:
        - target: /tmp/swallow
'''

# Import python libs
import logging
import os

# Import salt libs
from salt import exceptions
from salt.states.git import _fail, _neutral_test

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if svn is available
    '''
    if __salt__['cmd.has_exec']('svn'):
        return 'svn'
    return False


def latest(name,
           target=None,
           rev=None,
           user=None,
           username=None,
           force=False,
           externals=True):
    '''
    Checkout or update the working directory to the latest revision from the
    remote repository.

    name
        Address of the name repository as passed to "svn checkout"

    target
        Name of the target directory where the checkout will put the working
        directory

    rev : None
        The name revision number to checkout. Enable "force" if the directory
        already exists.

    user : None
        Name of the user performing repository management operations

    username : None
        The user to access the name repository with. The svn default is the
        current user

    force : False
        Continue if conflicts are encountered

    externals : True
        Change to False to not checkout or update externals
    '''
    ret = {'name': name, 'result': True, 'comment': '', 'changes': {}}
    if not target:
        return _fail(ret, 'Target option is required')

    svn_cmd = 'svn.checkout'
    cwd, basename = os.path.split(target)
    opts = tuple()

    if os.path.exists(target) and not os.path.isdir(target):
        return _fail(ret,
                     'The path "{0}" exists and is not '
                     'a directory.'.format(target)
                     )
    if __opts__['test']:
        if not os.path.exists(target):
            return _neutral_test(
                    ret,
                    ('{0} doesn\'t exist and is set to be checked out.').format(target))
        svn_cmd = 'svn.diff' 
        opts += ('-r',  'HEAD')
        out = __salt__[svn_cmd](cwd, target, user, username, *opts)
        return _neutral_test(
                ret,
                ('{0}').format(out))
    try:
        current_info = __salt__['svn.info'](cwd, target, user=user, fmt='dict')
        svn_cmd = 'svn.update'
    except exceptions.CommandExecutionError:
        pass

    if rev:
        opts += ('-r', str(rev))

    if force:
        opts += ('--force',)

    if externals is False:
        opts += ('--ignore-externals',)

    if svn_cmd == 'svn.update':
        out = __salt__[svn_cmd](cwd, basename, user, *opts)

        current_rev = current_info[0]['Revision']
        new_rev = __salt__['svn.info'](cwd=target,
                                       targets=None,
                                       user=user,
                                       username=username,
                                       fmt='dict')[0]['Revision']
        if current_rev != new_rev:
            ret['changes']['revision'] = "{0} => {1}".format(current_rev, new_rev)
    else:
        out = __salt__[svn_cmd](cwd, name, basename, user, username, *opts)

        ret['changes']['new'] = name
        ret['changes']['revision'] = __salt__['svn.info'](cwd=target,
                                                          targets=None,
                                                          user=user,
                                                          username=username,
                                                          fmt='dict')[0]['Revision']

    ret['comment'] = out
    return ret


def dirty(name,
          target,  # pylint: disable=W0613
          user=None,  # pylint: disable=W0613
          ignore_unversioned=False):  # pylint: disable=W0613
    '''
    Determine if the working directory has been changed.
    '''
    ret = {'name': name, 'result': True, 'comment': '', 'changes': {}}
    return _fail(ret, 'This function is not implemented yet.')
