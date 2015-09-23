##############################################################################
##
## This file is part of Sardana
##
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################
from sardana import State
from sardana.pool.pooldefs import SynchDomain, SynchParam
from sardana.util.funcgenerator import RectangularFunctionGenerator
from sardana.pool.controller import TriggerGateController

class SoftwareTriggerGateController(TriggerGateController):
    """Basic controller intended for demonstration purposes only.
    """
    gender = "Simulation"
    organization = "ALBA-Cells"
    MaxDevice = 1

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        TriggerGateController.__init__(self, inst, props, *args, **kwargs)
        self.tg = {}

    def add_listener(self, axis, listener):
        '''Backdoor method to attach listeners. It will be removed whenever 
        a proper EventChannel mechanism will be implemented'''
        idx = axis - 1
        tg = self.tg[idx]
        tg.add_listener(listener)

    def remove_listener(self, axis, listener):
        idx = axis - 1
        tg = self.tg[idx]
        tg.add_listener(listener)

    def SetAxisPar(self, axis, name, value):
        pass

    def GetAxisPar(self, axis, name):
        return None

    def SetConfiguration(self, axis, conf):
        idx = axis - 1
        tg = self.tg[idx]
        # TODO: implement nonequidistant triggering
        conf = conf[0]
        delay = conf[SynchParam.Delay][SynchDomain.Time]
        total_time = conf[SynchParam.Total][SynchDomain.Time]
        active_time = conf[SynchParam.Active][SynchDomain.Time]
        passive_time = total_time - active_time
        repeats = conf[SynchParam.Repeats]
        tg.setOffset(delay)
        tg.setActiveInterval(active_time)
        tg.setPassiveInterval(passive_time)
        tg.setRepetitions(repeats)

    def GetConfiguration(self, axis):
        idx = axis - 1
        tg = self.tg[idx]
        # TODO: implement nonequidistant triggering
        # TODO: wrong configuration dict. return the same conf.
        active_time=tg.getActiveInterval(),
        passive_time=tg.getPassiveInterval()
        total_time = active_time + passive_time
        conf = [{SynchParam.Delay: tg.getOffset(),
                 SynchParam.Total: total_time,
                 SynchParam.Active: active_time,
                 SynchParam.Repeats: tg.getRepetitions()}]
        return conf

    def AddDevice(self, axis):
        self._log.debug('AddDevice(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx] = RectangularFunctionGenerator()

    def StateOne(self, axis):
        """Get the dummy trigger/gate state"""
        self._log.debug('StateOne(%d): entering...' % axis)
        sta = State.On
        status = "Stopped"
        idx = axis - 1
        if self.tg[idx].isGenerating():
            sta = State.Moving
            status = "Moving"
        self._log.debug('StateOne(%d): returning (%s, %s)' % (axis, sta, status))
        return sta, status

    def PreStartOne(self, axis, value=None):
        self._log.debug('PreStartOne(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx].prepare()
        return True

    def StartOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('StartOne(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx].start()        

    def AbortOne(self, axis):
        """Start the specified trigger
        """
        self._log.debug('AbortOne(%d): entering...' % axis)
        idx = axis - 1
        self.tg[idx].stop()