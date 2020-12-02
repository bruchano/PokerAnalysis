import random


CARD = "23456789TJQKA"

POKER = {
    0: {0: "D2", 1: "D3", 2: "D4", 3: "D5", 4: "D6", 5: "D7", 6: "D8", 7: "D9", 8: "DT", 9: "DJ", 10: "DQ", 11: "DK", 12: "DA"},
    1: {0: "C2", 1: "C3", 2: "C4", 3: "C5", 4: "C6", 5: "C7", 6: "C8", 7: "C9", 8: "CT", 9: "CJ", 10: "CQ", 11: "CK", 12: "CA"},
    2: {0: "H2", 1: "H3", 2: "H4", 3: "H5", 4: "H6", 5: "H7", 6: "H8", 7: "H9", 8: "HT", 9: "HJ", 10: "HQ", 11: "HK", 12: "HA"},
    3: {0: "S2", 1: "S3", 2: "S4", 3: "S5", 4: "S6", 5: "S7", 6: "S8", 7: "S9", 8: "ST", 9: "SJ", 10: "SQ", 11: "SK", 12: "SA"}
}

VALUE = {
    0: {"High Card"},
    1: {"Pair"},
    2: {"Two Pairs"},
    3: {"Three of a Kind"},
    4: {"Straight"},
    5: {"Flush"},
    6: {"Full House"},
    7: {"Four of a Kind"},
    8: {"Straight Flush"}
}

RESULT = {
    1: "Win",
    0: "Split",
    -1: "Lose"
}


class Player:
    def __init__(self, num, *args: int):
        self.name = f"Player {num}"
        self.word = []
        self.draw = []
        self.card = [0 for i in range(13)]
        self.suit = [[0 for i in range(13)] for j in range(4)]

        self.value = 0
        self.highest = None

        self.high = 0
        self.high_num = []
        self.pair = 0
        self.pair_num = []
        self.triple = 0
        self.triple_num = []
        self.four = 0
        self.four_num = None

        self.straight = False
        self.straight_num = None

        self.flush = False
        self.flush_count = [0 for i in range(4)]
        self.flush_list = [[] for i in range(4)]

        self.straight_flush = False

        if args:
            for x in args:
                self.draw.append(x)
                self.draw.sort()
                self.card[x % 13] += 1
                self.suit[x // 13][x % 13] = 1
                self.word.append(POKER[x // 13][x % 13])

    def __str__(self):
        return self.name


class Game:
    def __init__(self, args):
        self.players = args
        self.pool = [i for i in range(52)]
        self.word = []
        self.draw = []
        self.winner = None

        for player in self.players:
            if player.draw != []:
                for x in player.draw:
                    self.pool.remove(x)

        for player in self.players:
            if player.draw == []:
                for i in range(2):
                    card = random.choice(self.pool)
                    player.draw.append(card)
                    self.pool.remove(card)

                player.draw.sort()
                for x in player.draw:
                    player.card[x % 13] += 1
                    player.suit[x // 13][x % 13] = 1
                    player.word.append(POKER[x // 13][x % 13])

        for i in range(5):
            card = random.choice(self.pool)
            self.draw.append(card)
            self.word.append(POKER[card // 13][card % 13])
            self.pool.remove(card)

        for x in self.draw:
            for player in self.players:
                player.card[x % 13] += 1
                player.suit[x // 13][x % 13] = 1

        print(f"Flop: {self.word}")
        for player in self.players:
            print(f"{player} card: {player.word}")
            # print(f"Player {i+1} suit: {player.suit}")

    def GetCardValue(self):
        for player in self.players:
            for i in range(13):

                if player.card[i] == 4:
                    player.four += 1
                    player.four_num = i
                elif player.card[i] == 3:
                    player.triple += 1
                    player.triple_num.append(i)
                elif player.card[i] == 2:
                    player.pair += 1
                    player.pair_num.append(i)
                elif player.card[i] == 1:
                    player.high = i
                    player.high_num.append(i)

                for j in range(4):
                    if player.suit[j][i] == 1:
                        player.flush_count[j] += 1
                        player.flush_list[j].append(i)

            for x, i in enumerate(player.flush_count):
                if i >= 5:
                    player.flush = True
                    player.flush_list = player.flush_list[x]
                    break

            if [player.card[i] >= 1 for i in range(-1, 4)] == [True, True, True, True, True]:
                player.straight = True
                player.straight_num = 3
            for i in range(9):
                if [player.card[i+j] >= 1 for j in range(5)] == [True, True, True, True, True]:
                    player.straight = True
                    player.straight_num = i + 4
            if player.straight and player.flush:
                for i in range(len(player.flush_list) - 4):
                    if player.flush_list[i:i+5] == [player.flush_list[i], player.flush_list[i]+1, player.flush_list[i]+2, player.flush_list[i]+3, player.flush_list[i]+4]:
                        player.straight_flush = True
                        player.highest = player.flush_list[i] + 4

            if player.straight_flush:
                player.value = 8
                player.highest = player.straight_num
            elif player.four:
                player.value = 7
                player.highest = player.four_num
            elif player.triple and player.pair:
                player.value = 6
                player.highest = player.triple_num[-1]
            elif player.flush:
                player.value = 5
                player.highest = player.flush_list[-1]
            elif player.straight:
                player.value = 4
                player.highest = player.straight_num
            elif player.triple:
                player.value = 3
                player.highest = player.triple_num[-1]
            elif player.pair >= 2:
                player.value = 2
                player.highest = player.pair_num[-1]
            elif player.pair == 1:
                player.value = 1
                player.highest = player.pair_num[-1]
            else:
                player.highest = player.high

    def GetWinner(self):
        highest_value = 0
        competitor = []
        competitor_highest = []
        for i, player in enumerate(self.players):
            if player.value > highest_value:
                highest_value = player.value
                competitor = [self.players[i]]
                competitor_highest = [player.highest]
            elif player.value == highest_value:
                competitor.append(self.players[i])
                competitor_highest.append(player.highest)
        print(f"Highest Value: {VALUE[highest_value]}")

        if len(competitor) == 1:
            self.winner = [competitor[0]]
        else:
            leader = 0
            lead_value = 0
            for i in range(len(competitor_highest)):
                if competitor_highest[i] > lead_value:
                    lead_value = competitor_highest[i]
                    leader = i
            if competitor_highest.count(lead_value) == 1:
                self.winner = [competitor[leader]]
            else:
                if highest_value == 8:
                    self.winner = [player for player in competitor if player.highest == lead_value]
                if highest_value == 7:
                    x = [player.high for player in competitor]
                    leader = 0
                    lead_value = 0
                    for i in range(len(competitor_highest)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        self.winner = [player for player in competitor if player.high == lead_value]
                elif highest_value == 6:
                    x = [player.pair_num[-1] for player in competitor]
                    leader = 0
                    lead_value = 0
                    for i in range(len(competitor_highest)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        self.winner = [player for player in competitor if player.pair_num[-1] == lead_value]
                elif highest_value == 5:
                    x = [player.flush_list[-2] for player in competitor]
                    count = 0
                    leader = 0
                    lead_value = 0
                    for i in range(len(x)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                            count = 1
                        elif x[i] == lead_value:
                            count += 1
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        competitor = [player for player in competitor if player.flush_list[-2] == lead_value]
                        x = [player.flush_list[-3] for player in competitor]
                        count = 0
                        leader = 0
                        lead_value = 0
                        for i in range(len(x)):
                            if x[i] > lead_value:
                                lead_value = x[i]
                                leader = i
                                count = 1
                            elif x[i] == lead_value:
                                count += 1
                        if x.count(lead_value) == 1:
                            self.winner = [competitor[leader]]
                        else:
                            competitor = [player for player in competitor if player.flush_list[-3] == lead_value]
                            x = [player.flush_list[-4] for player in competitor]
                            count = 0
                            leader = 0
                            lead_value = 0
                            for i in range(len(x)):
                                if x[i] > lead_value:
                                    lead_value = x[i]
                                    leader = i
                                    count = 1
                                elif x[i] == lead_value:
                                    count += 1
                            if x.count(lead_value) == 1:
                                self.winner = [competitor[leader]]
                            else:
                                competitor = [player for player in competitor if player.flush_list[-4] == lead_value]
                                x = [player.flush_list[-5] for player in competitor]
                                count = 0
                                leader = 0
                                lead_value = 0
                                for i in range(len(x)):
                                    if x[i] > lead_value:
                                        lead_value = x[i]
                                        leader = i
                                        count = 1
                                    elif x[i] == lead_value:
                                        count += 1
                                if x.count(lead_value) == 1:
                                    self.winner = [competitor[leader]]
                                else:
                                    self.winner = [player for player in competitor if player.flush_list[-5] == lead_value]
                elif highest_value == 4:
                    self.winner = [player for player in competitor if player.highest == lead_value]
                elif highest_value == 3:
                    x = [player.high for player in competitor]
                    lead_value = 0
                    leader = 0
                    count = 0
                    for i in range(len(x)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                            count = 1
                        elif x[i] == lead_value:
                            count += 1
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        competitor = [player for player in competitor if player.high == lead_value]
                        x = [player.high_num[-2] if len(player.high_num) >= 2 else player.triple_num[-2] for player in competitor]
                        lead_value = 0
                        leader = 0
                        count = 0
                        for i in range(len(x)):
                            if x[i] > lead_value:
                                lead_value = x[i]
                                leader = i
                                count = 1
                            elif x[i] == lead_value:
                                count += 1
                        if x.count(lead_value) == 1:
                            self.winner = [competitor[leader]]
                        else:
                            self.winner = []
                            for i, j in enumerate(x):
                                if j == lead_value:
                                    self.winner.append(competitor[i])
                elif highest_value == 2:
                    x = [player.pair_num[-2] for player in competitor]
                    count = 0
                    lead_value = 0
                    leader = 0
                    for i in range(len(x)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                            count = 1
                        elif x[i] == lead_value:
                            count += 1
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        competitor = [player for player in competitor if player.pair_num[-2] == lead_value]
                        x = [player.high for player in competitor]
                        count = 0
                        lead_value = 0
                        leader = 0
                        for i in range(len(x)):
                            if x[i] > lead_value:
                                lead_value = x[i]
                                leader = i
                                count = 1
                            elif x[i] == lead_value:
                                count += 1
                        if x.count(lead_value) == 1:
                            self.winner = [competitor[leader]]
                        else:
                            self.winner = [player for player in competitor if player.high == lead_value]
                elif highest_value == 1:
                    x = [player.high for player in competitor]
                    count = 0
                    lead_value = 0
                    leader = 0
                    for i in range(len(x)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                            count = 1
                        elif x[i] == lead_value:
                            count += 1
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        competitor = [player for player in competitor if player.high == lead_value]
                        x = [player.high_num[-2] for player in competitor]
                        count = 0
                        lead_value = 0
                        leader = 0
                        for i in range(len(x)):
                            if x[i] > lead_value:
                                lead_value = x[i]
                                leader = i
                                count = 1
                            elif x[i] == lead_value:
                                count += 1
                        if x.count(lead_value) == 1:
                            self.winner = [competitor[leader]]
                        else:
                            competitor = [player for player in competitor if player.high_num[-2] == lead_value]
                            x = [player.high_num[-3] for player in competitor]
                            count = 0
                            lead_value = 0
                            leader = 0
                            for i in range(len(x)):
                                if x[i] > lead_value:
                                    lead_value = x[i]
                                    leader = i
                                    count = 1
                                elif x[i] == lead_value:
                                    count += 1
                            if x.count(lead_value) == 1:
                                self.winner = [competitor[leader]]
                            else:
                                self.winner = [player for player in competitor if player.high_num[-3] == lead_value]
                elif highest_value == 0:
                    x = [player.high_num[-2] for player in competitor]
                    count = 0
                    lead_value = 0
                    leader = 0
                    for i in range(len(x)):
                        if x[i] > lead_value:
                            lead_value = x[i]
                            leader = i
                            count = 1
                        elif x[i] == lead_value:
                            count += 1
                    if x.count(lead_value) == 1:
                        self.winner = [competitor[leader]]
                    else:
                        competitor = [player for player in competitor if player.high_num[-2] == lead_value]
                        x = [player.high_num[-3] for player in competitor]
                        count = 0
                        lead_value = 0
                        leader = 0
                        for i in range(len(x)):
                            if x[i] > lead_value:
                                lead_value = x[i]
                                leader = i
                                count = 1
                            elif x[i] == lead_value:
                                count += 1
                        if x.count(lead_value) == 1:
                            self.winner = [competitor[leader]]
                        else:
                            competitor = [player for player in competitor if player.high_num[-3] == lead_value]
                            x = [player.high_num[-4] for player in competitor]
                            count = 0
                            lead_value = 0
                            leader = 0
                            for i in range(len(x)):
                                if x[i] > lead_value:
                                    lead_value = x[i]
                                    leader = i
                                    count = 1
                                elif x[i] == lead_value:
                                    count += 1
                            if x.count(lead_value) == 1:
                                self.winner = [competitor[leader]]
                            else:
                                competitor = [player for player in competitor if player.high_num[-4] == lead_value]
                                x = [player.high_num[-5] for player in competitor]
                                count = 0
                                lead_value = 0
                                leader = 0
                                for i in range(len(x)):
                                    if x[i] > lead_value:
                                        lead_value = x[i]
                                        leader = i
                                        count = 1
                                    elif x[i] == lead_value:
                                        count += 1
                                if x.count(lead_value) == 1:
                                    self.winner = [competitor[leader]]
                                else:
                                    self.winner = [player for player in competitor if player.high_num[-5] == lead_value]

        winner = []
        for i, player in enumerate(self.players):
            if player == self.winner or player in self.winner:
                winner.append(i+1)
        print(f"Winner: Player {winner}")
        if self.players[0] in self.winner:
            if len(self.winner) == 1:
                return RESULT[1]
            else:
                return RESULT[0]
        else:
            return RESULT[-1]













