# -*- coding: utf-8 -*-
"""Read-only update check from an HTTPS JSON manifest in the project repository."""
import json
import re
from urllib.request import Request, urlopen
from . import VERSION

MANIFEST_URL = 'https://raw.githubusercontent.com/OliOli2013/OpenCamView-Plugin/main/version.json'
_MAX_BYTES = 8192
_VERSION_RE = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')

def version_tuple(value):
    if not isinstance(value, str) or not _VERSION_RE.fullmatch(value):
        raise ValueError('Invalid version in update manifest')
    return tuple(int(item) for item in value.split('.'))

def check_update(opener=None):
    """Fetch bounded metadata only; never download or execute a package."""
    req = Request(MANIFEST_URL, headers={'User-Agent': 'OpenCamView/%s'%VERSION, 'Accept': 'application/json'})
    if opener is None:
        opener = urlopen
    with opener(req, timeout=8) as response:
        raw = response.read(_MAX_BYTES+1)
    if len(raw) > _MAX_BYTES:
        raise ValueError('Update metadata is too large')
    data = json.loads(raw.decode('utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Invalid update metadata')
    remote = data.get('version')
    latest = version_tuple(remote)
    installed = version_tuple(VERSION)
    notes = data.get('notes', {})
    if not isinstance(notes, dict):
        notes = {}
    notes = {x:str(notes.get(x,'')).replace('\r',' ').replace('\n',' ')[:200] for x in ('pl','en')}
    date = data.get('date', '')
    if not isinstance(date, str) or len(date)>16:
        date = ''
    return {'installed':VERSION,'latest':remote,'newer':latest>installed,'date':date,'notes':notes}
