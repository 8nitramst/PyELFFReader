import gzip
import itertools
import os
import shlex

import magic


class ELFFLogreader():
    """
    This Class reads an given file in ELFF format, which has a header line for the used fields in the log.
    The content is crunched to a list of dictionaries, where one dictionary is one log line.


    """

    m_dictLogList = []

    def __init__(self, fname, ft=False):
        if ft == False:
            self.__initParserNFT__(fname)
        if ft == True:
            self.__initParserFTT__(fname)

    def __initParserFTT__(self, fname):
        '''
        Fault Tolerance Parser - This Parser has Fault-Tolerance on board,

        :param fname: (str) Filename

        '''

        # check if the path exists and the file type
        try:
            if os.path.exists(fname):
                mime = magic.Magic(mime=True)
                ftype = mime.from_file(str(fname))
            else:
                raise IOError("No such file " + fname)
        except IOError:
            raise

        try:
            print "Depending on the size this could take a few minutes..."
            # Read the file
            filecontent = []
            if ftype == "text/plain":
                with open(fname, "r") as reader:
                    filecontent = reader.readlines()
            else:
                if ftype == "application/gzip":
                    with gzip.open(fname, "r") as reader:
                        filecontent = reader.readlines()

            dictLogKeys = None
            self.m_dictLogList = []

            # read the header comments and prepare the "#Fields - Header" for parsing to dict-keys
            for i in filecontent:
                # strip comments - and  get the columns titles
                if i.startswith("#"):
                    if i.startswith("#Fields: "):
                        # change column header, if there are multiple files concatenated
                        dictLogKeys = shlex.split(i.replace("#Fields: ", ""))
                else:
                    try:
                        # split the logline
                        dictLogValues = shlex.split(i)
                    except:
                        try:
                            # second method to split if the first fails
                            s = shlex.shlex(i)
                            s.whitespace_split = True
                            s.whitespace = " "
                            dictLogValues = list(s)
                        except:
                            raise

                    # generate dictionary and add it to the list
                    dictLogLine = dict(itertools.izip(dictLogKeys, dictLogValues))
                    self.m_dictLogList.append(dictLogLine)
        except IOError:
            print "No such file: %s" % (fname)

    def __initParserNFT__(self, fname):
        '''
        The ristrictive Parser - This Parser is not Fault-Tolerance

        :param fname: (str) - Filename of the Logfile

        '''

        ftype = ""

        # check the file type
        try:
            if os.path.exists(fname):
                mime = magic.Magic(mime=True)
                ftype = mime.from_file(str(fname))
            else:
                raise IOError("No such file " + fname)
        except IOError:
            raise

        try:

            print "Depending on the size this could take a few minutes..."

            filecontent = []
            # Read the file
            if ftype == "text/plain":
                with open(fname, "r") as reader:
                    filecontent = reader.readlines()
            else:
                if ftype == "application/gzip":
                    with gzip.open(fname, "r") as reader:
                        filecontent = reader.readlines()

            dictLogKeys = None
            keyline = 0
            self.m_dictLogList = []

            # read the file-content
            for i in filecontent:
                # strip comments - and  get the columns titles
                if i.startswith("#"):
                    if i.startswith("#Fields: "):
                        # allow only one header line in the file
                        if keyline == 0:
                            dictLogKeys = shlex.split(i.replace("#Fields: ", ""))
                            keyline = 1
                else:
                    # for each logline
                    if keyline == 1:
                        try:
                            # split the logline
                            dictLogValues = shlex.split(i)
                        except ValueError:
                            # if the logline can not be splitted well - try it a second time with different splitter
                            try:
                                s = shlex.shlex(i)
                                s.whitespace_split = True
                                s.whitespace = " "
                                dictLogValues = list(s)
                            except:
                                raise

                        # check of keys to value parsing - count of keys and values should not change
                        if len(dictLogKeys) == len(dictLogValues):
                            # generate dictonary entry and add it to the  list
                            dictLogLine = dict(itertools.izip(dictLogKeys, dictLogValues))
                            self.m_dictLogList.append(dictLogLine)
                        else:
                            raise StandardError("Logfile might be damaged")
                    else:
                        raise StandardError("Logfile not in ELFF-Format")
        except IOError:
            print "No such file: %s" % (fname)



    def getLogs(self):
        """ Get the content of the logfile as a list of dict


        :return: list(dict[]) List of Dictionary - where key is the ELFF-Header
        """
        return self.m_dictLogList
