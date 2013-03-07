import cPickle as pickle
import logging
import re
import sys

### word frequencies:

### function that takes as input a string and, optionally, 
### a dictionary, and returns the dictionary populated with word frequencies.
### provide options to strip punctuation and convert to lowercase.
## 

### instr is the input string
### wf is an optional dictionary. This can be used to count over
### multiple files. If it is present, add counts to this.
### stripPunc and toLower indicate whether to strip punctuation and
### convert to lower case.
def wordfreq(instr, wf=None, stripPunc=True, toLower=True) :
    if stripPunc:
        instr = re.sub(r'[^\s\w0-9]', ' ', instr)
    if toLower:
        instr = instr.lower()
        logging.debug(instr)
        logging.debug('\n')

    wordList = instr.split()
    logging.debug(wordList)
    logging.debug('\n')

    if wf is None :
        wf = {}
    for w in wordList :
        if w in wf.iterkeys() :
            wf[w] += 1
        else :
            wf[w] = 1

    logging.debug(wf)
    logging.debug('\n')

    return wf

### Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file
### if --nostrip, don't strip punctuation
### if --noConvert, don't convert everything to lower case
### if --pfile=outfile, pickle the resulting dictionary and store it in outfile.
### otherwise, print it to standard out.

if __name__ == '__main__' :
#    logging.basicConfig(level=logging.DEBUG)

    logging.debug(sys.argv)

    strip = True
    convert = True
    pfile = None

    if len(sys.argv) > 1 :
        for arg in sys.argv[1:-1] :
            if arg == '--nostrip' :
                logging.debug('nostrip')
                strip = False
            elif arg == '--noConvert' :
                logging.debug('noConvert')
                convert = False
            elif arg.startswith('--pfile=') :
                logging.debug('pfile')
                pfile = arg[8:]
            else :
                print('Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file')
                exit()
    else :
        print('Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file')
        exit()

    f = open(sys.argv[-1], 'r')
    fstr = f.read()
    wf = wordfreq(fstr, None, strip, convert)
    f.close()

    if pfile is not None :
        f = open(pfile, 'w')
        pickle.dump(wf, f)
        f.close()
    else :
        print wf
