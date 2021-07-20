def main():
    # Parameters:
    P1S = 0.6
    P2S = 0.7
    Q = 1 - P2S 
    [A, B] = Matrices()

    # Compute the match probability distribution:
    MatchDist3 = Match3(P1S, Q, A, B)
    print(MatchDist3)

def Game(P):
    # Single Service Game:
    Game = pow(P,4) * (15 - 4*P - ((10 * pow(P,2)) / (1 - 2 * P * (1 - P))))
    return Game

def TB(P, Q):
    # Import A Matrix:
    [A, B] = Matrices()
    # Tie-Breaker: (7 Pointer)
    TB = 0
    for i in range(28):
        TB += A[i][0] * pow(P,A[i][1]) * pow((1-P),A[i][2]) * pow(Q,A[i][3]) * pow((1-Q),A[i][4]) * pow(D(P, Q),A[i][5])
    return TB

def Set(P, Q, A, B):
    # Set:
    Set = 0
    for i in range(21):
        Set += B[i][0] * pow(Game(P),B[i][1]) * pow((1-Game(P)),B[i][2]) * pow(Game(Q),B[i][3]) * pow((1-Game(Q)),B[i][4])\
        * pow((Game(P)*Game(Q) + (Game(P)*(1-Game(Q)) + (1-Game(P))*Game(Q)) * TB(P,Q,A)),B[i][5])
    return Set

def Match3(P, Q, A, B):
    Match = pow(Set(P,Q,A,B),2) * (1 + 2 * (1 - Set(P,Q,A,B)))
    return Match

def Match5(P, Q, A, B):
    Match = pow(Set(P,Q,A,B),3) * (1 + 3 * (1 - Set(P,Q,A,B)) + 6 * pow((1 - Set(P,Q,A,B)),2))
    return Match

def D(P, Q):
    D = P * Q * pow((1 - (P * (1-Q) + (1-P) * Q)), -1)
    return D

def Matrices():
    A = [[1,3,0,4,0,0],[3,3,1,4,0,0],[4,4,0,3,1,0],[6,3,2,4,0,0],[16,4,1,3,1,0],[6,5,0,2,2,0],[10,2,3,5,0,0],[40,3,2,4,1,0],
    [30,4,1,3,2,0],[4,5,0,2,3,0],[5,1,4,6,0,0],[50,2,3,5,1,0],[100,3,2,4,2,0],[50,4,1,3,3,0],[5,5,0,2,4,0],[1,1,5,6,0,0],
    [30,2,4,5,1,0],[150,3,3,4,2,0],[200,4,2,3,3,0],[75,5,1,2,4,0],[6,6,0,1,5,0],[1,0,6,6,0,1],[36,1,5,5,1,1],[225,2,4,4,2,1],
    [400,3,3,3,3,1],[225,4,2,2,4,1],[36,5,1,1,5,1],[1,6,0,0,6,1]]
    B = [[1,3,0,3,0,0],[3,3,1,3,0,0],[3,4,0,2,1,0],[6,2,2,4,0,0],[12,3,1,3,1,0],[3,4,0,2,2,0],[4,2,3,4,0,0],[24,3,2,3,1,0],
    [24,4,1,2,2,0],[4,5,0,1,3,0],[5,1,4,5,0,0],[40,2,3,4,1,0],[60,3,2,3,2,0],[20,4,1,2,3,0],[1,5,0,1,4,0],[1,0,5,5,0,1],
    [25,1,4,4,1,1],[100,2,3,3,2,1],[100,3,2,2,3,1],[25,4,1,1,4,1],[1,5,0,0,5,1]]
    return A, B
    
if __name__ == "__main__":
    main()