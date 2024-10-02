from espn_api.football import League
import math
WEEK_NUM = 5
QB = 1
RB = 2
WR = 2
TE = 1
FLEX = 2
DEF = 1
K = 0
OP = 0

team_to_user = {
    2 : 282726616449155073, #Tony
    11 : 867523794570969088, # Kevin
    6 : 843940264686911498, # Noah
    10 : 705123997238558730, #Matt
    12 : 823382017131413565, #Shane
    7 : 525136159534481418, # nick pointer
    1 : 216757405780934656, # Nathan
    4 : 759218779649081394, # Nick Wernert
    5 : 253359197029138432, # jerry
    9 : 535180424654225428, # Bryce
    3 : 290383009776009236, # Julian
    8 : 753807398719979555 # Evan
}

team_to_name = {
    1 : "Nathan (Legion of Doom)",
    2 : "Tony (Bradys Luscious Lips)",
    3 : "Julian (Boise Pissboys)",
    4 : "Nick W (Mayfield Bakers)",
    5 : "Jerry (Williamsburg Wombats)",
    6 : "Noah (Bay Ridge Ballers)",
    7 : "Nick P (Alexis Texans)",
    8 : "Evan (BEEG Football)",
    9 : "Bryce (Air Richardson)",
    10 : "Matt (Baltimore Dummies)",
    11 : "Kevin (Village Idiots)",
    12 : "Shane (Franchise Tag Me!)"
}

# CHANGE THIS FOR LEAGUE STATS
#Baller Nation
league = League(1833368525, 2024, espn_s2='AEADsMSFzGzJ2C5QH%2BvPbTC8WwJbVaQigpGc7uZma6rFRCFHRqkJvn6ClIxLCLUDb%2BBuuwWVX75kC1I%2Bj0lwoufbzBG5iMbCKCNAN%2FtGP8US%2BagvwBHKHAUyRHZnwNSd1aW33RsyFFJENK3eRw0tfozMoU0rlb17SgTCJSuOt9R1v29ylci0InXADnbMqUuPJ9YBVHVjCO7ozxO1ZWQLYiUj0fOnbGeR8onPiuPdSfO%2BJ8esCLm%2BPiMsuzRupM9ku4%2B04dPdkgpImwXpXwfT1iQAVDyV46JHWdQpMSY6G7f5tQ%3D%3D', swid='{C1951524-FAD2-4212-B878-73B1F4FE67A9}')


def GetStandings(client):

    result = ''
    result += "**LEAGUE STANDINGS**\n"

    standings = league.standings()

    for i in range(len(standings)):
        result += ("**#" + str(i + 1) + "** " + client.get_user(team_to_user.get(standings[i].team_id)).mention + "\n")

    return result

def GetTeamIdsSorted(): # Sorted by league standings
    result = []

    standings = league.standings()
    for team in standings:
        result.append(team.team_id)
    return result

def GetWinnerIds():
    winners = []
    boxScores = league.box_scores(WEEK_NUM)


    for boxScore in boxScores:
        if (boxScore.home_team == 0 or boxScore.away_team == 0):
            continue

        if (boxScore.home_score > boxScore.away_score):
            winners.append(boxScore.home_team.team_id)
        else:
            winners.append(boxScore.away_team.team_id)

    return winners

def GetLoserIds():
    losers = []
    boxScores = league.box_scores(WEEK_NUM)


    for boxScore in boxScores:
        if (boxScore.home_team == 0 or boxScore.away_team == 0):
            continue

        if (boxScore.home_score > boxScore.away_score):
            losers.append(boxScore.away_team.team_id)
        else:
            losers.append(boxScore.home_team.team_id)

    return losers

def GetMatchupScores(client):
    boxScores = league.box_scores(WEEK_NUM)
    result = ''
    result+=("**Match Summaries for week " + str(WEEK_NUM) + "**\n")
    result+=("----------------------------------------------------------\n")

    for boxScore in boxScores:
        if (boxScore.home_team == 0 or boxScore.away_team == 0):
            continue
        homeUser = client.get_user(team_to_user.get(boxScore.home_team.team_id))
        homeName = client.get_user(team_to_user.get(boxScore.home_team.team_id)).mention + "(" + str(boxScore.home_team.wins) + "-" + str(boxScore.home_team.losses) + ")"
        awayName = client.get_user(team_to_user.get(boxScore.away_team.team_id)).mention + "(" + str(boxScore.away_team.wins) + "-" + str(boxScore.away_team.losses) + ")"
        if (boxScore.home_score > boxScore.away_score):
            result+=("**" + homeName + "** vs. " + awayName + "\n")
        else:
            result+=(homeName + " vs. **" + awayName + "**\n")

        result+=(client.get_user(team_to_user.get(boxScore.home_team.team_id)).mention + " score: " + str(boxScore.home_score) + "\n")
        result+=(client.get_user(team_to_user.get(boxScore.away_team.team_id)).mention + " score: " + str(boxScore.away_score) + "\n")
        result+=("----------------------------------------------------------\n\n")

    return result

def GetTopWeeklyScorers(client):
    result = ("**WEEK'S TOP SCORERS**\n")

    scores = GetSortedHighestWeeklyScores()

    for i in range(3):
        result+=(client.get_user(team_to_user.get(scores[i][0].team_id)).mention + ": " + str(round(scores[i][1], 2)) + "\n")

    return result

def GetBottomWeeklyScorers(client):
    result=("**WEEK'S BOTTOM SCORERS**\n")

    scores = GetSortedHighestWeeklyScores()

    for i in range(3):
        if not isinstance(scores[len(scores) - i - 1][0], int):
            result+=(client.get_user(team_to_user.get(scores[len(scores) - i - 1][0].team_id)).mention + ": " + str(round(scores[len(scores) - i - 1][1], 2)) + "\n")
    return result

def GetTopScorers(client):
    result=("**SEASON'S TOP SCORERS**\n")

    topScorers = league.top_scorer()
    
    for i in range(3):
        result+=(client.get_user(team_to_user.get(topScorers[i].team_id)).mention + ": " + str(round(topScorers[i].points_for, 2)) + "\n")
    return result

def GetBottomScorers(client):
    result=("**SEASON'S BOTTOM SCORERS**\n")

    bottomScorers = league.least_scorer()
    
    for i in range(3):
        result+=(client.get_user(team_to_user.get(bottomScorers[i].team_id)).mention + ": " + str(round(bottomScorers[i].points_for, 2)) + "\n")
    return result

def GetHardestSchedule(client):
    result=("**SEASON'S HARDEST SCHEDULES**\n")

    topScorers = league.most_points_against()
    
    for i in range(3):
        result+=(client.get_user(team_to_user.get(topScorers[i].team_id)).mention + ": " + str(round(topScorers[i].points_for, 2)) + "\n")
    return result

def GetSoftestSchedule(client):
    result=("**SEASON'S SOFTEST SCHEDULES**\n")

    lowestScorers = league.least_points_against()
    
    for i in range(3):
        result+=(client.get_user(team_to_user.get(lowestScorers[i].team_id)).mention + ": " + str(round(lowestScorers[i].points_against, 2)) + "\n")
    return result

def GetMostEfficientManager(client):
    result=("**MANAGER EFFICIENCIES**\n")
    boxScores = league.box_scores(WEEK_NUM)
    effs = []

    for matchup in league.box_scores(WEEK_NUM):
        optimal = GetOptimalScore(matchup.home_lineup)[0]
        actual = matchup.home_score
        eff = round(actual/optimal * 100 , 2)
        effs.append(tuple([client.get_user(team_to_user.get(matchup.home_team.team_id)).mention, actual, optimal, eff]))
        optimal = GetOptimalScore(matchup.away_lineup)[0]
        actual = matchup.away_score
        if optimal == 0:
            continue
        eff = round(actual/optimal * 100, 2)
        effs.append(tuple([client.get_user(team_to_user.get(matchup.away_team.team_id)).mention, actual, optimal, eff]))

    effs.sort(key = lambda x: x[3], reverse = True)

    for i in range(len(effs)):
        result+=(effs[i][0] + ": " + str(effs[i][3]) + "%")
        if effs[i][1] == effs[i][2]:
            result+=(" :star: *PERFECT ROSTER* :star:\n")
        else:
            result+=("\n")
        result+=("\t" + "(actual = " + str(effs[i][1]) + ", max = " + str(effs[i][2]) + ")\n")

    return result

def GetBestStartingPlayers(client):
    result=("**BEST STARTING PLAYERS**\n")
    boxScores = league.box_scores(WEEK_NUM)
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and "QB" in player.eligibleSlots and QB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and "QB" in player.eligibleSlots and QB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("QB: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and "RB" in player.eligibleSlots and RB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and "RB" in player.eligibleSlots and RB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("RB: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and "WR" in player.eligibleSlots and WR > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and "WR" in player.eligibleSlots and WR > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("WR: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and "TE" in player.eligibleSlots and TE > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and "TE" in player.eligibleSlots and TE > 0):
                    if (player.points > score):
                        name = player.name
                        teamName =  client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("TE: "+ name + ": " + str(score) + " on " + teamName)
    return result

def GetBestBenchPlayers(client):
    result=("**BEST BENCHED PLAYERS**\n")
    boxScores = league.box_scores(WEEK_NUM)
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position == "BE" and "QB" in player.eligibleSlots and QB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position == "BE" and "QB" in player.eligibleSlots and QB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("QB: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position == "BE" and "RB" in player.eligibleSlots and RB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position == "BE" and "RB" in player.eligibleSlots and RB > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("RB: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position == "BE" and "WR" in player.eligibleSlots and WR > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position == "BE" and "WR" in player.eligibleSlots and WR > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("WR: "+ name + ": " + str(score) + " on " + teamName + "\n")
    score = -1000
    name = ""
    teamName = ""
    for matchup in boxScores:
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position == "BE" and "TE" in player.eligibleSlots and TE > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                        score = player.points

        if (matchup.away_team != 0):
            for player in matchup.away_lineup:
                if (player.slot_position == "BE" and "TE" in player.eligibleSlots and TE > 0):
                    if (player.points > score):
                        name = player.name
                        teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                        score = player.points

    result+=("TE: "+ name + ": " + str(score) + " on " + teamName + "\n")
    return result

def GetBestBench(client):
    result=("** THE PRESTEGIOUS BEST BENCH AWARD **\n")
    teamName = ""
    benchScore = 0
    boxScores = league.box_scores(WEEK_NUM)
    for matchup in boxScores:
        tempScore = 0
        if (matchup.home_team != 0):
            for player in matchup.home_lineup:
                if (player.slot_position == "BE"):
                    tempScore += player.points
            if tempScore > benchScore:
                teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                benchScore = tempScore
        tempScore = 0
        if matchup.away_team != 0:
            for player in matchup.away_lineup:
                if (player.slot_position == "BE"):
                    tempScore += player.points
            if tempScore > benchScore:
                teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                benchScore = tempScore
    result+=(teamName + ": " + str(round(benchScore, 2)))
    return result

def GetWorstBench(client):
    result=("** THE PITIFUL WORST BENCH AWARD **\n")
    teamName = ""
    benchScore = 9999999
    boxScores = league.box_scores(WEEK_NUM)
    for matchup in boxScores:
        tempScore = 999999
        if matchup.home_team != 0:
            for player in matchup.home_lineup:
                if (player.slot_position == "BE"):
                    tempScore += player.points
            if tempScore < benchScore:
                teamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                benchScore = tempScore
        tempScore = 0
        if matchup.away_team != 0:
            for player in matchup.away_lineup:
                if (player.slot_position == "BE"):
                    tempScore += player.points
            if tempScore < benchScore:
                teamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                benchScore = tempScore
    result+=(teamName + ": " + str(round(benchScore, 2)))
    return result

def GetUpsets(client):
    result=("**UPSETS OF THE WEEK**\n")
    boxScores = league.box_scores(WEEK_NUM)
    for matchup in boxScores:
        if (matchup.home_team == 0 or matchup.away_team == 0):
            continue

        homeProj = 0;
        awayProj = 0;
        for player in matchup.away_lineup:
            if (player.slot_position != "BE" and player.slot_position != "IR"):
                awayProj += player.projected_points
        for player in matchup.home_lineup:
            if (player.slot_position != "BE" and player.slot_position != "IR"):
                homeProj += player.projected_points

        if (homeProj > awayProj and matchup.home_score < matchup.away_score):
            result+=(client.get_user(team_to_user.get(matchup.home_team.team_id)).mention + " was projected to beat " + client.get_user(team_to_user.get(matchup.away_team.team_id)).mention + " by " + 
                       str(round(homeProj-awayProj, 2)) + " points, but lost by " + str(round(matchup.away_score - matchup.home_score, 2)) + " points\n");
        elif (homeProj < awayProj and matchup.home_score > matchup.away_score):
            result+=(client.get_user(team_to_user.get(matchup.away_team.team_id)).mention + " was projected to beat " + client.get_user(team_to_user.get(matchup.home_team.team_id)).mention + " by " + 
                       str(round(awayProj-homeProj, 2)) + " points, but lost by " + str(round(matchup.home_score - matchup.away_score, 2)) + " points\n");
    return result

def CouldHaveWonIf(client):
    result=("** COULD HAVE WON IF... **\n")
    boxScores = league.box_scores(WEEK_NUM)
    for matchup in boxScores:
        if (matchup.home_team == 0 or matchup.away_team == 0):
            continue
        homeLoss = matchup.home_score < matchup.away_score
        if (homeLoss):
            OptimalScoreAndTeam = GetOptimalScore(matchup.home_lineup)
            if (OptimalScoreAndTeam[0] > matchup.away_score):
                result+=(client.get_user(team_to_user.get(matchup.home_team.team_id)).mention + " could have won by " + str(round(OptimalScoreAndTeam[0] - matchup.away_score, 2)) +
                           " if they had started:\n")
                for player in OptimalScoreAndTeam[1]:
                    result+=(player + "\n")
                result+=("\n")
        else:
            OptimalScoreAndTeam = GetOptimalScore(matchup.away_lineup)
            if (OptimalScoreAndTeam[0] > matchup.home_score):
                result+=(client.get_user(team_to_user.get(matchup.away_team.team_id)).mention + " could have won by " + str(round(OptimalScoreAndTeam[0] - matchup.home_score, 2)) +
                           " if they had started:\n")
                for player in OptimalScoreAndTeam[1]:
                    result+=(player + "\n")
                result+=("\n")
    return result

def GetBiggestBlowout(client):
    result=("** THE BIGGEST BLOWOUT **\n")
    boxScores = league.box_scores(WEEK_NUM)
    biggestBlowoutMatch = boxScores[0]

    blowoutMargin = -1
    for matchup in boxScores:
        if (matchup.home_team == 0 or matchup.away_team == 0):
            continue
        if abs(matchup.home_score - matchup.away_score) > blowoutMargin:
            biggestBlowoutMatch = matchup;
            blowoutMargin = abs(matchup.home_score - matchup.away_score)

    if biggestBlowoutMatch.home_score > biggestBlowoutMatch.away_score:
        result+=(client.get_user(team_to_user.get(biggestBlowoutMatch.home_team.team_id)).mention + " blew out " + client.get_user(team_to_user.get(biggestBlowoutMatch.away_team.team_id)).mention
                   + " by " + str(round(blowoutMargin, 2)) + "\n\n")
    else:
        result+=(client.get_user(team_to_user.get(biggestBlowoutMatch.away_team.team_id)).mention + " blew out " + client.get_user(team_to_user.get(biggestBlowoutMatch.home_team.team_id)).mention
                   + " by " + str(round(blowoutMargin, 2)) + "\n\n")
    return result

def GetClosestWin(client):
    result=("** THE CLOSEST WIN **\n")
    boxScores = league.box_scores(WEEK_NUM)
    closestWinMatch = boxScores[0]
    closestWin = 999999
    for matchup in boxScores:
        if (matchup.home_team == 0 or matchup.away_team == 0):
            continue
        if abs(matchup.home_score - matchup.away_score) < closestWin:
            closestWinMatch = matchup;
            closestWin = abs(matchup.home_score - matchup.away_score)

    if closestWinMatch.home_score > closestWinMatch.away_score:
        result+=(client.get_user(team_to_user.get(closestWinMatch.home_team.team_id)).mention + " narrowly beat " + client.get_user(team_to_user.get(closestWinMatch.away_team.team_id)).mention
                   + " by " + str(round(closestWin, 2)) + "\n\n")
    else:
        result+=(client.get_user(team_to_user.get(closestWinMatch.away_team.team_id)).mention + " narrowly beat " + client.get_user(team_to_user.get(closestWinMatch.home_team.team_id)).mention
                   + " by " + str(round(closestWin, 2)) + "\n\n")
    return result

def GetMostPtsInALoss(client):
    result=("** THE MOST POINTS IN A LOSS **\n")
    boxScores = league.box_scores(WEEK_NUM)
    losingTeams = dict()
    topTeam = ""
    topPts = -1

    for matchup in boxScores:
        if matchup.home_score > matchup.away_score:
            losingTeams[client.get_user(team_to_user.get(matchup.away_team.team_id)).mention] = matchup.away_score
        else:
            losingTeams[client.get_user(team_to_user.get(matchup.home_team.team_id)).mention] = matchup.home_score

    for key, value in losingTeams.items():
        if value > topPts:
            topPts = value
            topTeam = key

    result += topTeam + " had the highest points in a loss with " + str(round(topPts, 2)) + "!\n"

    return result

def GetLeastPtsInAWin(client):
    result=("** THE LEAST POINTS IN A WIN **\n")
    boxScores = league.box_scores(WEEK_NUM)
    winningTeams = dict()
    bottomTeam = ""
    leastPts = 9999999

    for matchup in boxScores:
        if matchup.away_score > matchup.home_score:
            winningTeams[client.get_user(team_to_user.get(matchup.away_team.team_id)).mention] = matchup.away_score
        else:
            winningTeams[client.get_user(team_to_user.get(matchup.home_team.team_id)).mention] = matchup.home_score

    for key, value in winningTeams.items():
        if value < leastPts:
            leastPts = value
            bottomTeam = key

    result += bottomTeam + " had the least points in a win with " + str(round(leastPts, 2)) + "!\n"

    return result

def GetBestLuck(client):
    boxScores = league.box_scores(WEEK_NUM)
    bestPercent = -1;
    bestLuckTeamName = ""
    bestLuckTeamProjected = -1
    bestLuckActualScore = -1

    result=("** THE BEST LUCK **\n")
    for matchup in boxScores:
        if matchup.home_team != 0:
            homeProj = 0;
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and player.slot_position != "IR"):
                    homeProj += player.projected_points
            if homeProj > 0 and matchup.home_score / homeProj > bestPercent:
                bestPercent = matchup.home_score / homeProj
                bestLuckTeamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                bestLuckTeamProjected = homeProj
                bestLuckActualScore = matchup.home_score
        if matchup.away_team != 0:
            awayProj = 0;
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and player.slot_position != "IR"):
                    awayProj += player.projected_points
            if awayProj > 0 and matchup.away_score / awayProj > bestPercent:
                bestPercent = matchup.away_score / awayProj
                bestLuckTeamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                bestLuckTeamProjected = awayProj
                bestLuckActualScore = matchup.away_score

    result+=(bestLuckTeamName + " was the luckiest team!\nThey were projected to score " + str(round(bestLuckTeamProjected, 2)) + " but scored "
               + str(round(bestLuckActualScore, 2)) + ". Which is " + str(round(bestPercent * 100, 2)) + "% of their projected!")
    return result

def GetWorstLuck(client):
    boxScores = league.box_scores(WEEK_NUM)
    worstPercent = 99999;
    worstLuckTeamName = ""
    worstLuckTeamProjected = -1
    worstLuckActualScore = 9999999

    result=("** THE WORST LUCK **\n")
    for matchup in boxScores:
        if matchup.home_team != 0:
            homeProj = 0;
            for player in matchup.home_lineup:
                if (player.slot_position != "BE" and player.slot_position != "IR"):
                    homeProj += player.projected_points
            if homeProj > 0 and matchup.home_score / homeProj < worstPercent:
                worstPercent = matchup.home_score / homeProj
                worstLuckTeamName = client.get_user(team_to_user.get(matchup.home_team.team_id)).mention
                worstLuckTeamProjected = homeProj
                worstLuckActualScore = matchup.home_score
        if matchup.away_team != 0:
            awayProj = 0;
            for player in matchup.away_lineup:
                if (player.slot_position != "BE" and player.slot_position != "IR"):
                    awayProj += player.projected_points
            if awayProj > 0 and matchup.away_score / awayProj < worstPercent:
                worstPercent = matchup.away_score / awayProj
                worstLuckTeamName = client.get_user(team_to_user.get(matchup.away_team.team_id)).mention
                worstLuckTeamProjected = awayProj
                worstLuckActualScore = matchup.away_score

    result+=(worstLuckTeamName + " was the unluckiest team :(\nThey were projected to score " + str(round(worstLuckTeamProjected, 2)) + " but scored "
               + str(round(worstLuckActualScore, 2)) + ". Which is " + str(round(worstPercent * 100, 2)) + "% of their projected :(")
    return result


def PerfectRoster(client):
    result=("** PERFECT ROSTERS **\n")
    boxScores = league.box_scores(WEEK_NUM)
    PerfectRosters = []
    for matchup in boxScores:
        if matchup.home_team != 0 and math.isclose(matchup.home_score, GetOptimalScore(matchup.home_lineup)[0], abs_tol=0.003):
            PerfectRosters.append(client.get_user(team_to_user.get(matchup.home_team.team_id)).mention)
        if matchup.away_team != 0 and math.isclose(matchup.away_score, GetOptimalScore(matchup.away_lineup)[0], abs_tol=0.003):
            PerfectRosters.append(client.get_user(team_to_user.get(matchup.away_team.team_id)).mention)
    if (len(PerfectRosters) == 0):
        result+=("There were no perfect rosters this week.\n\n")
    else:
        result+=("These teams had perfect rosters (max points possible):\n")
        for team in PerfectRosters:
            result+=(team + "\n")
    return result

def GetOptimalScore(roster):

    qbCopy = QB
    rbCopy = RB
    wrCopy = WR
    teCopy = TE
    flexCopy = FLEX
    defCopy = DEF
    kCopy = K
    opCopy = OP

    playerList = []
    bestRoster = []
    bestRosterJustNames = []
    bestScore = 0;
    for player in roster:
        playerList.append((player.points, player))
    playerList.sort(reverse=True, key = lambda x: x[0])

    for player in playerList:
        if "QB" in player[1].eligibleSlots and qbCopy > 0:
            qbCopy -= 1
            bestRoster.append(player)
        elif "RB" in player[1].eligibleSlots and rbCopy > 0:
            rbCopy -= 1
            bestRoster.append(player)
        elif "WR" in player[1].eligibleSlots and wrCopy > 0:
            wrCopy -= 1
            bestRoster.append(player)
        elif "TE" in player[1].eligibleSlots and teCopy > 0:
            teCopy -= 1
            bestRoster.append(player)
        elif "RB/WR/TE" in player[1].eligibleSlots and flexCopy > 0:
            flexCopy -= 1
            bestRoster.append(player)
        elif "D/ST" in player[1].eligibleSlots and defCopy > 0:
            defCopy -= 1
            bestRoster.append(player)
        elif "K" in player[1].eligibleSlots and kCopy > 0:
            kCopy -= 1
            bestRoster.append(player)
        elif "OP" in player[1].eligibleSlots and opCopy > 0:
            opCopy -= 1
            bestRoster.append(player)

    for player in bestRoster:
        bestScore += player[0]
        bestRosterJustNames.append(player[1].name)

    return (round(bestScore, 2), bestRosterJustNames)
    
def GetSortedHighestWeeklyScores():
    scores = []
   
    for matchup in league.box_scores(WEEK_NUM):
        scores.append(tuple([matchup.home_team, matchup.home_score]))
        scores.append(tuple([matchup.away_team, matchup.away_score]))
    scores.sort(key = lambda x: x[1], reverse = True)
    return scores
