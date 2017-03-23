for m in xrange(1,6):
    inString = raw_input( "enter input " + str(m) +": ")
    inStringList = inString.split()

    onState = []

    pressedTileList = [] 

    for i in xrange( 1, int(inStringList[0])+1):
        for j in xrange( 1, len(inStringList[i])):
            onState.append((int(inStringList[i][0]), int(inStringList[i][j])))


    for i in xrange(int(inStringList[0])+2, len(inStringList)):
        pressedTileList.append((int(inStringList[i][0]), int(inStringList[i][1])))

    for pressedTile in pressedTileList:


        def flipAroundTile(row, col):
            if (row, col) in onState:
                onState.remove((row, col))
            else:
                onState.append((row, col))

        flipAroundTile(pressedTile[0], pressedTile[1])

        if pressedTile[0]+1 <= 8:
            flipAroundTile(pressedTile[0]+1, pressedTile[1])

        if pressedTile[0]+2 <= 8:
            flipAroundTile(pressedTile[0]+2, pressedTile[1])

        if pressedTile[0]-1 >= 1:
            flipAroundTile(pressedTile[0]-1, pressedTile[1])

        if pressedTile[0]-2 >= 1:
            flipAroundTile(pressedTile[0]-2, pressedTile[1])

        if pressedTile[1]+1 <= 8:
            flipAroundTile(pressedTile[0], pressedTile[1]+1)

        if pressedTile[1]+2 <= 8:
            flipAroundTile(pressedTile[0], pressedTile[1]+2)

        if pressedTile[1]-1 >= 1:
            flipAroundTile(pressedTile[0], pressedTile[1]-1)

        if pressedTile[1]-2 >= 1:
            flipAroundTile(pressedTile[0], pressedTile[1]-2)

        if pressedTile[0]+1 <= 8 and pressedTile[1]+1 <= 8:
            flipAroundTile(pressedTile[0]+1, pressedTile[1]+1)

        if pressedTile[0]+1 <= 8 and pressedTile[1]-1 >= 1:
            flipAroundTile(pressedTile[0]+1, pressedTile[1]-1)

        if pressedTile[0]-1 >= 1 and pressedTile[1]-1 >= 1:
            flipAroundTile(pressedTile[0]-1, pressedTile[1]-1)

        if pressedTile[0]-1 >= 1 and pressedTile[1]+1 <=8:
            flipAroundTile(pressedTile[0]-1, pressedTile[1]+1)


    print len(onState)
