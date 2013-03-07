import cPickle as pickle
import sys
import re
import logging

### read in data from an ARFF file and return the following data structures:
### A dict that maps an attribute index to a dictionary mapping attribute names to either:
###    - possible values
###    - the string 'string'
###    - the string 'numeric'
### A list containing all data instances, with each instance stored as a tuple.
def readArff(filehandle) :
    isData = False
    attriDict = {}
    dataList = []
    seq = 1
    for line in filehandle :
        if line.startswith('%') :
            # This is a comment line
            pass
        elif not isData :
            if line.startswith('@attribute') :
                m = re.match(r'@attribute ([^\s]+) \{(.*)\}.*', line)
                items = m.group(2).split(',')
                items = [i.strip() for i in items]
                attriDict[seq] = {m.group(1) : items}
                seq += 1
            elif line.startswith('@data') :
                isData = True
        else :
            items = line.split(',')
            items = [i.strip() for i in items]
            dataList.append(tuple(items))

    result = [attriDict, dataList]
    return result

### Compute ZeroR - that is, the most common data classification without 
### examining any of the attributes. Return the most comon classification.
###   (that is, the most common value of the *last* column of data)
def computeZeroR(attributes, data) :
    items = attributes.values()[-1].values()[0]
    countDict = {item: 0 for item in items}

    logging.debug(countDict)

    for d in data :
        countDict[d[-1]] += 1

    result = None
    for i in countDict.items() :
        if result is None or result[1] < i[1] :
            result = i

    logging.debug(countDict)

    return result[0]

### Usage: readARFF {--pfile=outfile} infile
### If --pfile=outfile, pickle and store the results in outfile. Otherwise, 
### print them to standard out. Your code should also call computeZeroR and 
### print out the results.

if __name__ == '__main__' :
#    logging.basicConfig(level=logging.DEBUG)

    pfile = None

    if len(sys.argv) > 1 :
        for arg in sys.argv[1:-1] :
            if arg.startswith('--pfile=') :
                logging.info('pfile')
                pfile = arg[8:]
            else :
                print('Usage: readARFF {--pfile=outfile} infile')
                exit()
    else :
        print('Usage: readARFF {--pfile=outfile} infile')
        exit()


    f = open(sys.argv[-1], 'rb')
    r = readArff(f)
    f.close()

    if pfile is not None:
        f = open(pfile, 'w')
        pickle.dump(r, f)
        f.close()
    else :
        print 'Attributes: '
        print r[0]
        print
        print 'Datas: '
        print r[1]

    print
    print 'Most common classification: '
    print computeZeroR(r[0], r[1])

