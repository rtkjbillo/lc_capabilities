# Copyright 2017 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from beach.actor import Actor
import re
_x_ = Actor.importLib( 'utils/hcp_helpers', '_x_' )

class AclTampering ( object ):
    def __init__( self, fromActor ):
        self.icacls = re.compile( r'.*icacls\.exe', re.IGNORECASE )
        self.icaclsCommands = re.compile( r'.*(grant)', re.IGNORECASE )

    def analyze( self, event, sensor, *args ):
        filePath = _x_( event.data, '?/base.FILE_PATH' )
        cmdLine = _x_( event.data, '?/base.COMMAND_LINE' )
        if filePath is not None and cmdLine is not None:
            if self.icacls.match( filePath ) and self.icaclsCommands.match( cmdLine ):
                return True
        return False
