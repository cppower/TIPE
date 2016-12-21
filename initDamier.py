def init(damier):
    pionsNoirs=[   [0,1],[0,3],[0,5],[0,7],[0,9],
                    [1,0],[1,2],[1,4],[1,6],[1,8],
                    [2,1],[2,3],[2,5],[2,7],[2,9],
                    [3,0],[3,2],[3,4],[3,6],[3,8]]
    pionsBlancs=[  [6,1],[6,3],[6,5],[6,7],[6,9],
                    [7,0],[7,2],[7,4],[7,6],[7,8],
                    [8,1],[8,3],[8,5],[8,7],[8,9],
                    [9,0],[9,2],[9,4],[9,6],[9,8]]
    casesNoires=[  [0,1],[0,3],[0,5],[0,7],[0,9],
                    [1,0],[1,2],[1,4],[1,6],[1,8],
                    [2,1],[2,3],[2,5],[2,7],[2,9],
                    [3,0],[3,2],[3,4],[3,6],[3,8],
                    [4,1],[4,3],[4,5],[4,7],[4,9],
                    [5,0],[5,2],[5,4],[5,6],[5,8],
                    [6,1],[6,3],[6,5],[6,7],[6,9],
                    [7,0],[7,2],[7,4],[7,6],[7,8],
                    [8,1],[8,3],[8,5],[8,7],[8,9],
                    [9,0],[9,2],[9,4],[9,6],[9,8]]
    for i in range (0,len(pionsNoirs)):
        damier[pionsNoirs[i][0],pionsNoirs[i][1]]=1
        damier[pionsBlancs[i][0],pionsBlancs[i][1]]=-1
    return (damier, pionsBlancs, casesNoires)