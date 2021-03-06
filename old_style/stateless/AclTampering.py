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

###############################################################################
# Metadata
'''
LC_DETECTION_MTD_START
{
    "type" : "stateless",
    "description" : "Detects someone tampering ACLs on disk.",
    "requirements" : "",
    "feeds" : [ "notification.NEW_PROCESS" ],
    "platform" : "windows",
    "author" : "maximelb@google.com",
    "version" : "1.0",
    "scaling_factor" : 1000,
    "n_concurrent" : 5,
    "usage" : {}
}
LC_DETECTION_MTD_END
'''
###############################################################################

from beach.actor import Actor
import re
ObjectTypes = Actor.importLib( 'utils/ObjectsDb', 'ObjectTypes' )
StatelessActor = Actor.importLib( 'Detects', 'StatelessActor' )
_x_ = Actor.importLib( 'utils/hcp_helpers', '_x_' )

class AclTampering ( StatelessActor ):
    def init( self, parameters, resources ):
        super( AclTampering, self ).init( parameters, resources )
        self.icacls = re.compile( r'.*icacls\.exe', re.IGNORECASE )
        self.icaclsCommands = re.compile( r'.*(grant)', re.IGNORECASE )

    def process( self, detects, msg ):
        routing, event, mtd = msg.data
        
        filePath = _x_( event, '?/base.FILE_PATH' )
        cmdLine = _x_( event, '?/base.COMMAND_LINE' )
        if filePath is not None and cmdLine is not None:
            if self.icacls.match( filePath ) and self.icaclsCommands.match( cmdLine ):
                    detects.add( 90,
                                 'tampering of ACLs',
                                 event )
