from Team import *

class TeamStats:

    def __init__(self):
        self.points_for = 0
        self.points_against = 0
        self.fouls = 0
        self.minutes_played = 0
        self.rebounds = 0

    def __str__(self):
        return "Team Stats:" + \
               "\n\tPoints For: " + str(self.points_for) + \
               "\n\tPoints Against: " + str(self.points_against)