import itertools
import shlex


class ELFFLogreader():
    """
    This Class reads an given file in ELFF format, which has a header line for the used fields in the log.
    The content is crunched to a list of dictionaries, where one dictionary is one log line.


    """
    m_file = ""
    m_dictLogList = []

    def __init__(self, fname):
        self.m_file = fname

        try:
            with open(self.m_file, "r") as reader:
                filecontent = reader.readlines()

            comments = []
            dictLogKeys = None

            # read the header comments and prepare the "#Fields - Header" for parsing to dict-keys
            for i in filecontent:
                if i.startswith("#"):
                    if i.startswith("#Fields: "):
                        dictLogKeys = shlex.split(i.replace("#Fields: ", ""))
                        comments.append(i)
                        break
                    else:
                        comments.append(i)

            try:
                if dictLogKeys is not None:
                    # remove the comment lines
                    for i in comments:
                        filecontent.remove(i)

                    self.m_dictLogList = []

                    # Standard-header
                    # #BC header
                    # #Version: 1.0
                    # #Date: 2005-04-27 20:57:09
                    # #Fields: date time time-taken c-ip sc-status s-action sc-bytes cs-bytes cs-method cs-uri-scheme cs-host cs-uri-path cs-uri-query cs-username s-hierarchy s-supplier-name rs(Content-Type) cs(User-Agent) sc-filter-result sc-filter-category x-virus-id s-ip s-sitename x-virus-details x-icap-error-code x-icap-error-details

                    # crunch the log lines to a dictionary
                    for logline in filecontent:
                        dictLogValues = shlex.split(logline)
                        dictLogLine = dict(itertools.izip(dictLogKeys, dictLogValues))
                        self.m_dictLogList.append(dictLogLine)
                else:
                    raise StandardError("Logfile not in ELFF-Format")
            except StandardError as e:
                print "Error: %s" % e.message
        except IOError:
            print "No such file: %s" % (self.m_file)



    def getLogs(self):
        """ Get the content of the logfile as a list of dict


        :return: list(dict[]) List of Dictionary - where key is the ELFF-Header
        """
        return self.m_dictLogList
