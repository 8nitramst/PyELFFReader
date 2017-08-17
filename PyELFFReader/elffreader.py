import shlex, itertools

class ELFFLogreader:
    m_file=""
    m_dictLogList = []

    m_dictLogValues=[]


    def __init__(self,fname):
        self.m_file=fname

        with open(self.m_file,"r") as reader:
            filecontent = reader.readlines()

        comments=[]

        for i in filecontent:
            if i.startswith("#"):
                if i.startswith("#Fields: "):
                    dictLogKeys = shlex.split(i.replace("#Fields: ", ""))
                    comments.append(i)
                    break
                else:
                    comments.append(i)

        for i in comments:
            filecontent.remove(i)

        self.m_dictLogList = []

        # Standard-header
        # BC header
        # #Version: 1.0
        # #Date: 2005-04-27 20:57:09
        # #Fields: date time time-taken c-ip sc-status s-action sc-bytes cs-bytes cs-method cs-uri-scheme cs-host cs-uri-path cs-uri-query cs-username s-hierarchy s-supplier-name rs(Content-Type) cs(User-Agent) sc-filter-result sc-filter-category x-virus-id s-ip s-sitename x-virus-details x-icap-error-code x-icap-error-details

        for logline in filecontent:
            dictLogValues = shlex.split(logline)
            dictLogLine = dict(itertools.izip(dictLogKeys, dictLogValues))
            self.m_dictLogList.append(dictLogLine)

    def getLogs(self):
        return self.m_dictLogList
