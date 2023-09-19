osm-to-gps-map
==============

Tools to download osm tiles and merge to a garmin image. Some hacking is required to download any particular area.

* download.py downloads a set of tiles for an area.
* retile.py creates a mkgmap script of downloaded tiles. This depends on the mkgmap splitter tool: http://www.mkgmap.org.uk/doc/splitter.html
* garmin map created with: java -jar mkgmap-r2638/mkgmap.jar --gmapsupp -c template.args
* mergeTiles.py merges many tiles into a single large osm file 

Tools for OsmAndMapCreator
--------------------------

* regions.py convert regions to WKT format
* multiextract.py extract areas from pycrocosm/pgmap
* prepextract.py renumber extracted areas to 32-bit IDs and convert to pbf format
* pbftoosmand convert a folder of pbfs to osmand files using OsmAndMapCreator

License
=======

Copyright (c) 2013-2014, Tim Sheerman-Chase
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

