"""
Got from https://stackoverflow.com/a/38488544
"""
__all__ = ['timer_resolution']

import contextlib
import ctypes
from ctypes import wintypes

winmm = ctypes.WinDLL('winmm')


class TIMECAPS(ctypes.Structure):
    _fields_ = (('wPeriodMin', wintypes.UINT),
                ('wPeriodMax', wintypes.UINT))


def _check_time_err(err, func, args):
    if err:
        raise WindowsError('%s error %d' % (func.__name__, err))
    return args


winmm.timeGetDevCaps.errcheck = _check_time_err
winmm.timeBeginPeriod.errcheck = _check_time_err
winmm.timeEndPeriod.errcheck = _check_time_err


@contextlib.contextmanager
def timer_resolution(resolution=0):
    caps = TIMECAPS()
    winmm.timeGetDevCaps(ctypes.byref(caps), ctypes.sizeof(caps))
    resolution = min(max(resolution, caps.wPeriodMin), caps.wPeriodMax)
    winmm.timeBeginPeriod(resolution)
    yield
    winmm.timeEndPeriod(resolution)
