# -*- coding: utf-8 -*-
#
# hl_api_parallel_computing.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

"""
Functions for parallel computing
"""

from .. import ll_api
from .hl_api_helper import *

__all__ = [
    'Rank',
    'NumProcesses',
    'SetAcceptableLatency',
    'SetMaxBuffered',
]


@check_stack
def Rank():
    """Return the MPI rank of the local process.

    Returns
    -------
    int:
        MPI rank of the local process

    Note
    ----
    DO NOT USE Rank() TO EXECUTE ANY FUNCTION IMPORTED FROM THE nest
    MODULE ON A SUBSET OF RANKS IN AN MPI-PARALLEL SIMULATION.

    This will lead to unpredictable behavior. Symptoms may be an
    error message about non-synchronous global random number generators
    or deadlocks during simulation. In the worst case, the simulation
    may complete but generate nonsensical results.
    """

    ll_api.sr("Rank")
    return ll_api.spp()


@check_stack
def NumProcesses():
    """Return the overall number of MPI processes.

    Returns
    -------
    int:
        Number of overall MPI processes
    """

    ll_api.sr("NumProcesses")
    return ll_api.spp()


@check_stack
def SetAcceptableLatency(port_name, latency):
    """Set the acceptable latency (in ms) for a MUSIC port.

    Parameters
    ----------
    port_name : str
        MUSIC port to set latency for
    latency : float
        Latency in ms
    """

    ll_api.sps(ll_api.kernel.SLILiteral(port_name))
    ll_api.sps(latency)
    ll_api.sr("SetAcceptableLatency")


@check_stack
def SetMaxBuffered(port_name, size):
    """Set the maximum buffer size for a MUSIC port.

    Parameters
    ----------
    port_name : str
        MUSIC port to set buffer size for
    size : int
        Buffer size
    """

    ll_api.sps(ll_api.kernel.SLILiteral(port_name))
    ll_api.sps(size)
    ll_api.sr("SetMaxBuffered")
