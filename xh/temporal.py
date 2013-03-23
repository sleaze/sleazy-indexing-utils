# -*- coding: utf-8 -*-

import re
from datetime import timedelta

_ageParserRe = re.compile(
    r'''^
        (?:(?P<years>\d+(?:\.\d+)?)?\s*y[ears]*\s*)?
        (?:(?P<months>\d+(?:\.\d+)?)?\s*mo[nths]*\s*)?
        (?:(?P<weeks>\d+(?:\.\d+)?)?\s*w[eks]*\s*)?
        (?:(?P<days>\d+(?:\.\d+)?)?\s*d[ays]*\s*)?
        (?:(?P<hours>\d+(?:\.\d+)?)?\s*h[ours]*\s*)?
        (?:(?P<minutes>\d+(?:\.\d+)?)?\s*m[inutes]*\s*)?
        (?:(?P<seconds>\d+(?:\.\d+)?)?\s*s[econds]*\s*)?
        (?:ago)?\s*
    $''',
    re.I | re.X
)

def parseInterval(specifier):
    """Produces a timedelta."""
    if specifier is None or not isinstance(specifier, str):
        return specifier

    m = _ageParserRe.match(specifier)
    if not m:
        return specifier

    weeks = 0
    if any([m.group('years'), m.group('months'), m.group('weeks')]):
        weeks += (int(m.group('years') or 0)) * 52
        weeks += (int(m.group('months') or 0)) * 4
        weeks += int(m.group('weeks') or 0)

    return timedelta(
        int(m.group('days') or 0),
        int(m.group('seconds') or 0),
        0, # microseconds
        0, # milliseconds
        int(m.group('minutes') or 0),
        int(m.group('hours') or 0),
        weeks
    )

