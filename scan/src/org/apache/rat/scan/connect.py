#########################################################################################
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################################

'''
NB: THIS SCRIPT IS PRE-ALPHA QUALITY

Connect module executes command line ssh 
to connect to apache. Once connected,
it pipes the scanner script to python.

This script is designed to be run within a ssh-agent session 
with 'apache' as a local alias for people.apache.org.
'''

import subprocess
import datetime
import diff
import sys
import os.path

def addPreamble(xml):
    return """<?xml version='1.0'?>
<!-- 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

-->\n""" + xml

def save(file, document):

    f = open(file, 'w')
    try:
        f.write(document)
    finally:
        f.close()
    return file

build_dir = sys.argv[1]
base_file_name = sys.argv[2]
diff_file_name = sys.argv[3]
ssh_host = sys.argv[4]
src_dir = sys.argv[5]

base_file = os.path.join(build_dir, base_file_name)
diff_file = os.path.join(build_dir, diff_file_name)

print 'Apache RAT Scan - Distribution Scanner'
print '---------------------------------------'
print 'ssh-agent MUST loaded with an appropriate'
print 'key for people.apache.org.'
print 'Alias host apache to people.apache.org'
print 'in the ssh client configuration.'
print ''
print 'Reading scanning script from local disc...'
file = open(os.path.join(src_dir,'scanner.py'), 'r')
script = file.read()
file.close()
print 'Ok'
print ''
print 'Opening connection to people.apache.org...'
process = subprocess.Popen('ssh -T -t ' + ssh_host, shell=True, 
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print 'Ok'
print ''
print 'About to run scanning script:'
print 'Time for tea...'
stdout_value, stderr_value = process.communicate("python <<TillEndOfScript234875823947592345988223\n" 
                                                 + script + "\nTillEndOfScript234875823947592345988223\n")
if not stderr_value == '':
    print 'ERROR: ' + stderr_value
print 'Ok'

xml = ''
for document in stdout_value.split("<?xml version='1.0'?>"):
    if document.lstrip().startswith("<documents basedir='/www/www.apache.org/dist/incubator'"):
        xml = xml + document
    elif document.lstrip().startswith("<documents basedir='/www/archive.apache.org/dist/incubator'"):
        xml = xml + document
    else:
        print "OUTPUT (probably nothing to worry about):"
        print document
        
if xml == "":
    print "No results returned"
else:
    xml = addPreamble("<audit on='" + datetime.datetime.utcnow().date().isoformat() + "'>" + xml + "</audit>")
    path = save(base_file, xml)
    subprocess.Popen('gpg --armor --detach-sig ' + path, shell=True).wait()
    
    
    prefix = base_file_name[0:-14]
    auditor = diff.Auditor(build_dir, prefix)
    auditor.printSignatureChecks()
    latestDiffs = auditor.latestDiffs()
    if latestDiffs == None:
        print "First run so skipping comparison "
    else:
        save(diff_file, addPreamble(latestDiffs))
    