import search

def checkMove(initial, moves, width):
    for move in moves:
        zeroIndex = initial.index(0)
        pieceIndex = initial.index(move)
        xDelta = abs((zeroIndex / width) - (pieceIndex / width))
        yDelta = abs((zeroIndex % width) - (pieceIndex % width))
        if (xDelta == 1 and yDelta == 0) or (xDelta == 0 and yDelta == 1):
            initial[zeroIndex] = move
            initial[pieceIndex] = 0
        else:
            return False

    return initial == range(len(initial))


bigCases = [((4,4,[7,6,5,4,3,2,1,0,8,9,10,11,12,13,14,15]), 28),
              ((3,2,[5,4,3,2,1,0]), 15)]

smallCases = [((3,3,[1,3,2,5,4,6,7,8,0]), 20),
               ((3,3,[1,2,5,4,0,8,3,6,7]), 8)]

slowSearches = [("ucs",search.ucs),("ids",search.ids)]
fastSearches = [("astar", search.astar), ("idastar", search.idastar)]


if __name__ == '__main__':

    success = True
    for (name,search) in slowSearches:
        print "Testing ", name
        for ((w,h,initial),solLen) in smallCases:
            (unused, size, sol) = search(w,h,initial[:])
            if (size > solLen):
                success = False
                print "Search ", name, " Path to long"
            print sol
            if (not checkMove(initial[:], sol, w)):
                sucess = False
                print "Search ", name, " solution incorrect"
    for (name,search) in fastSearches:
        print "Testing ", name
        for ((w,h,initial),solLen) in smallCases + bigCases:
            (unused, size, sol) = search(w,h,initial[:])
            print sol
            if (size > solLen):
                success = False
                print "Search ", name, " Path to long"
            if (not checkMove(initial[:], sol, w)):
                sucess = False
                print "Search ", name, " solution incorrect"
    if success:
        print "OK"
    else:
        print "Errors found"


