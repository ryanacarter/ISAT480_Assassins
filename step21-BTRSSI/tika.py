## If you put the jar in a non-standard location, you need to
## prepare the CLASSPATH **before** importing jnius
import os
os.environ['CLASSPATH'] = "/home/checkout/Downloads/tika-app-1.5.jar"

from jnius import autoclass

## Import the Java classes we are going to need
Tika = autoclass('org.apache.tika.Tika')
Metadata = autoclass('org.apache.tika.metadata.Metadata')
FileInputStream = autoclass('java.io.FileInputStream')

tika = Tika()
meta = Metadata()
text = tika.parseToString(FileInputStream(filename), meta)
