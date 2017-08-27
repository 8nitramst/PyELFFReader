# PyELFFReader
Reader for W3C ELFF files (extended log file format)

Introduction
-------------
Some proxy server using the W3C ELFF logging format for their log files. To make them also available for python and for automated processing, this package is a general log reader, that translates the log lines to a better useable format.

Who uses ELFF format?
---------------------
* Symantec SGProxy (aka BlueCoat)
* MS IIS 6.0

Dependencies:
-------------
* python-magic: Thanks to https://github.com/ahupp/python-magic and  https://pypi.python.org/pypi/python-magic
  * How-To: 
`pip install python-magic`
  * copyright by Adam Hupp under MIT License


Links:
------
* https://en.wikipedia.org/wiki/Extended_Log_Format
* https://www.microsoft.com/technet/prodtechnol/WindowsServer2003/Library/IIS/676400bc-8969-4aa7-851a-9319490a9bbb.mspx?mfr=true
* https://www.w3.org/TR/WD-logfile.html
