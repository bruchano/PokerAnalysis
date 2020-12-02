from Model import *
import matplotlib.pyplot as plt


LOOP = 1000
NUM_PLAYER = 6
MODE = "Suit"


y = []
x = []
def plot(mode, num_player, loop):
    plt.figure(1)
    plt.title(f"{num_player} Players ({mode})")
    plt.xlabel("Combination")
    plt.ylabel("Win Rate")
    plt.plot(x, y)
    plt.savefig(f"{mode}_{num_player}_players_loop_{loop}.png")
    plt.show()


def Play(num_player=2, loop=1000, mode="Off"):
    if mode == "Off":
        for i in range(13):
            for j in range(13):
                x.append(CARD[i] + CARD[j])
                game_win = 0

                for _ in range(loop):
                    P = [0 for i in range(num_player)]
                    P[0] = Player(1, i, j + 13)
                    for k in range(1, num_player):
                        P[k] = Player(k+1)
                    G = Game(P)
                    G.GetCardValue()
                    result = G.GetWinner()
                    print(f"Result: {result}" + "\n")
                    if result == "Win" or result == "Split":
                        game_win += 1

                game_win /= loop
                y.append(game_win)
                print(f"Win Rate: {game_win}")

    elif mode == "Suit":
        for i in range(12):
            for j in range(i+1, 13):
                x.append(CARD[i] + CARD[j])
                game_win = 0

                for _ in range(loop):
                    P = [0 for i in range(num_player)]
                    P[0] = Player(1, i, j)
                    for k in range(1, num_player):
                        P[k] = Player(k+1)
                    G = Game(P)
                    G.GetCardValue()
                    result = G.GetWinner()
                    print(f"Result: {result}" + "\n")
                    if result == "Win" or result == "Split":
                        game_win += 1

                game_win /= loop
                y.append(game_win)
                print(f"Win Rate: {game_win}")

    plot(mode, num_player, loop)


if __name__ == "__main__":
    print("--Simulation Started--\n")
    Play(num_player=NUM_PLAYER, loop=LOOP, mode=MODE)
    print("--Done--")
