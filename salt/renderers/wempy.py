# -*- coding: utf-8 -*-

from __future__ import absolute_import

# Import python libs
from StringIO import StringIO

# Import salt libs
from salt.exceptions import SaltRenderError
import salt.utils.templates


def render(template_file,
           saltenv='base',
           sls='',
           argline='',  # pylint: disable=W0613
           context=None,
           **kws):
    '''
    Render the data passing the functions and grains into the rendering system

    :rtype: string
    '''
    tmp_data = salt.utils.templates.WEMPY(template_file, to_str=True,
            salt=__salt__,
            grains=__grains__,
            opts=__opts__,
            pillar=__pillar__,
            saltenv=saltenv,
            sls=sls,
            context=context,
            **kws)
    if not tmp_data.get('result', False):
        raise SaltRenderError(tmp_data.get('data',
            'Unknown render error in the wempy renderer'))
    return StringIO(tmp_data['data'])
