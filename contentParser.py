import argparse
import re
import os

from bs4 import BeautifulSoup
import slate

HTML_REGEX = r'\((.*)\)'
PDF_REGEX = ['\n\nMeter Number: ([0-9]{8})\n\n',
    "\n\nTotal Taxes & Fees on Electric Charges[^a-zA-Z]*(\$[\d.]*)\n\n"]


def docparser(readerObj, html=False, pdf=False):
    '''
    @readerObj: File object output from reader library.
    @readerObj type: obj
    @html: Flag for html document.
    @html type: boolean
    @pdf: Flag for pdf document.
    @pdf type: boolean
    '''
    if html:
        htmlparser(readerObj)
    if pdf:
        pdfparser(readerObj)


def pdfparser(rObj):
    '''
    @rObj: File object output from reader library.
    @rObj type: obj
    '''
    for d in rObj:
        regex=r'\n\nMeter Number: ([0-9]{8})\n\n'
        m = re.search(regex, d)
        if m:
            print "Electric meter number (%s)" % str(m.group(1))

        tregex=r"\n\nTotal Taxes & Fees on Electric Charges[^a-zA-Z]*(\$[\d.]*)\n\n"
        mt = re.search(tregex, d)
        if mt:
            print "Electric Tax total amount (%s)" % str(mt.group(1))


def htmlparser(rObj):
    '''
    @rObj: File object output from reader library.
    @rObj type: obj
    '''
    result = rObj.find_all('a', onclick=re.compile("openGasPopup.*"))
    for r in result:
        addrString = r.attrs.get('onclick')
        if addrString:
            HTML_REGEX=r'\((.*)\)'
            m = re.search(HTML_REGEX, addrString)
            if m:
                print "Address is %s" % str(m.group(1))
            else:
                print "Address not found"

    rate = rObj.find_all('h3')
    for item in rate:
        if 'E-1' in item.string.strip():
            print "Rate name is %s" % str(item.string.strip())


def pdf_reader(path):
    '''
    @path: File path.
    @path type: str
    '''
    # https://github.com/timClicks/slate
    with open(path) as f:
        doc = slate.PDF(f)
    return doc


def html_reader(path):
    '''
    @path: File path.
    @path type: str
    '''
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc
    # https://pypi.python.org/pypi/beautifulsoup4https://pypi.python.org/pypi/beautifulsoup4
    with open(path) as f:
       soup = BeautifulSoup(f)
    return soup


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to parse HTML and\
        PDF content for specific purpose.")
    parser.add_argument("--html", help="html doc path", type=str)
    parser.add_argument("--pdf", help="pdf doc path", type=str)
    args = parser.parse_args()
    if args.html and len(args.html) != 0 and os.path.exists(args.html):
        docparser(html_reader(args.html), html=True)
    elif args.pdf and len(args.pdf) != 0 and os.path.exists(args.pdf):
        docparser(pdf_reader(args.pdf), pdf=True)
    else:
        print "Please verify your input file path. %s" % str(args.input)
