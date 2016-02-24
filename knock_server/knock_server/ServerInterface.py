# Copyright (C) 2015-2016 Daniel Sel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import logging
import os

from lib import daemonize

from modules import Configuration
from modules.Configuration import config

from modules.CertUtil import CertUtil
from modules.Firewall.Firewall import Firewall
from modules.Listener.KnockProcessor import KnockProcessor
from modules.Platform.LinuxUtils import dropPrivileges


LOG = logging.getLogger(__name__)

class ServerInterface:

    def __init__(self,
                 configFilePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'config.ini')):

        Configuration.initialize(configFilePath)
        self.cryptoEngine = CertUtil(config).initializeCryptoEngine()

    def runKnockDaemon(self):
        with Firewall(config) as firewallHandler:
            knockProcessor = KnockProcessor(config, self.cryptoEngine, firewallHandler)
            daemonize.createDaemon()
            dropPrivileges()
            knockProcessor.processPossibleKnockPackets()