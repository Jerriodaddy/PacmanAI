# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################
mode = -1 # 0=off, 1=def, 2=gohome
holdFood = 0

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveMinimaxAgent', second = 'DefensiveMinimaxAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########
class MinimaxAgent(CaptureAgent):
  """
  A minimax agent that plays at ply basis
  1) our team: Max1 and Max2
  2) their team: Min1 and Min2
  """

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  """
  def min_value(self, gameState, action, currDepth, targetDepth, turn, lastTurn):
      
      returns a utility value of Min
      1) need to use depth limited search - iterative deepening
      2) check for TERMINAL-TEST: if the target depth is reached
          - if so, return the evaluated utility
          - if not, keep going down
      
      if (currDepth == targetDepth):
          return self.evaluate(gameState, action, turn, lastTurn)
          # return -1

      value = float("inf")  # v -> pos infinity
      actions = gameState.getLegalActions(turn)
      for a in actions:
          # succState = self.getSuccessor(gameState, a)
          successor = self.getSuccessor(gameState, a, turn)
          myteam = self.getTeam(successor)
          teammate = None
          if self.red:
              if (currDepth + 1) % 4 == 3:
                  teammate = self.index
              else:
                  for t in myteam:
                      if t != self.index:
                          teammate = t
          else:
              if lastTurn == 0:
                  teammate = myteam[0]
              else:
                  teammate = myteam[1]
          value = min(value, self.max_value(successor, a, currDepth + 1, targetDepth, teammate, turn))
      return value

  def max_value(self, gameState, action, currDepth, targetDepth, turn, lastTurn):
      
      returns a utility value of Min
      1) need to use depth limited search - iterative deepening
      2) check for TERMINAL-TEST: if the target depth is reached
          - if so, return the evaluated utility
          - if not, keep going down
      
      if (currDepth == targetDepth):
          # return self.evaluate(gameState, action, turn)
          # return 1
          return self.evaluate(gameState, action, turn, lastTurn)

      value = float("-inf") # v -> neg infinity
      actions = gameState.getLegalActions(turn)
      for a in actions:
          successor = self.getSuccessor(gameState, a, turn)
          enemy = self.getOpponents(successor)
          if self.red:
              if lastTurn == 0:
                  opponent = enemy[0]
              else:
                  opponent = enemy[1]
          else:
              if lastTurn == 1:
                  opponent = enemy[1]
              else:
                  opponent = enemy[0]
          value = max(value, self.min_value(successor, a, currDepth + 1, targetDepth, opponent, turn))
      return value
  """
  def max_value(self, gameState, action, currDepth, targetDepth, turn):
      value = float("-inf")
      actions = gameState.getLegalActions(turn)
      action = None
      for a in actions:
          successor = self.getSuccessor(gameState, a, turn)
          temp = self.value(successor, action, currDepth + 1, targetDepth, turn)[0]
          if value < temp:
              value = temp
              action = a
      return (value, action)

  def min_value(self, gameState, action, currDepth, targetDepth, turn):
      value = float("inf")
      actions = gameState.getLegalActions(turn)
      returnAction = None
      for a in actions:
          successor = self.getSuccessor(gameState, a, turn)
          temp = self.value(successor, action, currDepth + 1, targetDepth, turn)[0]
          if value > temp:
              value = temp
              returnAction = a
      return (value, returnAction)

  def value(self, gameState, action, currDepth, targetDepth, turn):
      """
      return the best action for the root agent
      :param gameState: current game state
      :param currDepth: current depth for the game tree
      :param targetDepth: target depth for searching
      :return: a tuple: (value, action)
      """
      if currDepth == targetDepth:
          return (self.evaluate(gameState, action, (turn + 1) % 4), )  # TODO: implement it

      myteam = self.getTeam(gameState)
      if (turn + 1) % 4 in myteam:  # next is MAX
          return self.max_value(gameState, action,  currDepth, targetDepth, (turn + 1) % 4)
      else:  # next is MIN
          return self.min_value(gameState, action, currDepth, targetDepth, (turn + 1) % 4)

  def chooseAction(self, gameState):
    """
    choose the action based on the utilities of Max or Min
    """
    global holdFood

    # if holdFood == 1*2 and not gameState.getAgentState(self.index).isPacman:
    #     print "Get home"
    #     holdFood = 0
        
    value = float("-inf")
    actions = gameState.getLegalActions(self.index)
    bestAction = None
    for a in actions:
        successor = self.getSuccessor(gameState, a, self.index)
        temp = self.value(successor, a, 0, 0, self.index)[0]

        # print "action = " + a + " " + "value =  " + str(temp) +"\n"

        if value < temp:# random pick
            value = temp
            bestAction = a
    succPos = gameState.getAgentState(self.index).getPosition()
    self.debugDraw([succPos],[1,0,0], False)

    foodLeft = len(self.getFood(gameState).asList())
    if len(self.observationHistory) != 1:
      foodBefore = len(self.getFood(self.getPreviousObservation()).asList())
      if (foodBefore - foodLeft == 1):
        holdFood = holdFood + 1
        print "holdFood = " + str(holdFood)

    """
    maxUtility = float("-inf")
    bestAction = None
    for a in actions:
        # succState = self.getSuccessor(gameState, a)
        successor = self.getSuccessor(gameState, a, self.index)
        enemies = self.getOpponents(successor)  # opponent indices list
        # enemyIndex = None
        if self.red:
            if self.index + 1 == 1:
                enemyIndex = 0
            else:
                enemyIndex = 1
        else:
            if self.index == 1:
                enemyIndex = 1
            else:
                enemyIndex = 0
        curr = self.min_value(successor, a, 0, 4, enemies[enemyIndex], self.index)  # depth limited - 10
        # print "here"
        if curr > maxUtility:
            maxUtility = curr
            bestAction = a
    """
    return bestAction


  def getSuccessor(self, gameState, action, turn):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(turn, action)
    pos = successor.getAgentState(turn).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(turn, action)
    else:
      return successor

  def getCloestGhosts(self, gameState, action, turn):
    successor = self.getSuccessor(gameState, action, turn)

    myState = successor.getAgentState(turn)
    myPos = myState.getPosition()

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    closest = float("inf")
    for e in enemies:
        if e.isPacman and e.getPosition() != None: continue
        dist = self.getMazeDistance(myPos, e.getPosition())
        if (dist < closest):
            closest = dist
    return closest

  def evaluate(self, gameState, action, turn):
      global holdFood
      features = self.getFeatures(gameState, action)
      weights = self.getWeights(gameState, action)

      # if mode == 2:
      print str(features['goHome'])+" "+str(features*weights)+" "+action+" "+str(holdFood)
      # features = util.Counter()
      # weights = util.Counter()

      # myteam = self.getTeam(gameState)
      # opponents = self.getOpponents(gameState)
      # if turn not in myteam:  # evaluate on the opponents' side
      #     #if not len(self.observationHistory) == 1:  # avoid STOP action
      #     #    if self.getPreviousObservation().getAgentState(self.index).getPosition() == self.getCurrentObservation().getAgentState(self.index).getPosition():
      #     #        features['stop'] = 1
      #     #weights['stop'] = -100
      #
      #     #oppState = gameState.getAgentState(turn)
      #     #oppPos = oppState.getPosition()
      #
      #     myState = gameState.getAgentState(self.index)
      #     myPos = myState.getPosition()
      #
      #     enemies = [gameState.getAgentState(i) for i in myteam]
      #     o = [gameState.getAgentState(i) for i in opponents]
      #
      #     #ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      #     ghosts = [a for a in o if not a.isPacman and a.getPosition() != None]
      #     #pacmans = [a for a in enemies if a.isPacman and a.getPosition() != None]
      #     oppPacmans = [a for a in o if a.isPacman and a.getPosition() != None]  # my opponents as pacmans
      #
      #     # distsToEnemy = [self.getMazeDistance(oppPos, a.getPosition()) for a in enemies]
      #     distsToEnemy = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies]
      #     #distsToGhost = [self.getMazeDistance(oppPos, a.getPosition()) for a in ghosts]
      #     distsToGhost = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      #     distsToOppPacman = [self.getMazeDistance(myPos, a.getPosition()) for a in oppPacmans]
      #
      #     distsToAllEnemy = 0
      #     for d in distsToEnemy:
      #         distsToAllEnemy += d
      #     # features['distsToAllEnemy'] = distsToAllEnemy
      #     # weights['distsToAllEnemy'] = -10  # must be negative
      #
      #     # avoid being eaten by the ghost
      #     distsToAllGhost = 0
      #     for d in distsToGhost:
      #         distsToAllGhost += d
      #     # features['distsToAllGhost'] = distsToAllGhost
      #     # weights['distsToAllGhost'] = -1
      #     # if distsToGhost:
      #     #     features['distsToClosestGhost'] = min(distsToGhost)
      #     #     if min(distsToGhost) > 3: # maintain a fixed distance between enemy
      #     #         weights['distsToClosestGhost'] = -100
      #     #     #        weights['distsToAllGhost'] = -100
      #     #     else:
      #     #         weights['distsToClosestGhost'] = 1000
      #
      #
      #     # defensive feature behavior
      #     features['numOfInvader'] = len(oppPacmans)
      #     weights['numOfInvader'] = -1000
      #     #print "pacnum "+str(len(oppPacmans))
      #     distsToAllPacmans = 0
      #     for d in distsToOppPacman:
      #         distsToAllPacmans += d
      #     features['distsToAllPacmans'] = distsToAllPacmans
      #     weights['distsToAllPacmans'] = -10000
      #
      #     # scared feature: avoid being eaten when scared
      #     # if distsToAllPacmans:
      #         # features['distsToClosestGhost'] = min(distsToGhost)
      #     #    if oppState.scaredTimer != 0 and min(distsToAllPacmans) > 5:  # maintain a fixed distance between power pacman
      #             # weights['distsToClosestGhost'] = -100
      #     #        weights['distsToAllPacmans'] = -100
      #     #    else:
      #             # weights['distsToClosestGhost'] = 1
      #     #        weights['distsToAllPacmans'] = 100
      #
      #
      #     # offensive behavior
      #     foodList = self.getFood(gameState).asList()
      #     features['currentScore'] = -len(foodList)
      #     weights['currentScore'] = 100
      #
      #     # eat the closest food first
      #     if len(foodList) > 0:  # This should always be True,  but better safe than sorry
      #          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      #          features['distanceToFood'] = minDistance
      #          #if minDistance < 5:
      #              #features['eatFood'] = minDistance
      #              #weights['distanceToFood'] = -1000000
      #     #weights['eatFood'] = -100
      #     weights['distanceToFood'] = -1
      #
      #     # go back if have one food
      #     if gameState.getAgentState(self.index).numCarrying == 1:  # check number of food carried
      #         foodDefending = self.getFood(gameState).asList()  # go back if have one food
      #         minDistance = min([self.getMazeDistance(myPos, food) for food in foodDefending])
      #         features['goHome'] = minDistance
          #weights['goHome'] = -1000000

          #features['distsToClosestEnemy'] = min(distsToEnemy)
          #weights['distsToClosestEnemy']= -1

          #if distsToGhost:
          #    features['distsToClosestGhost'] = min(distsToGhost)
          #weights['distsToClosestGhost'] = -1


      # else:
      #     myState = gameState.getAgentState(turn)
      #     myPos = myState.getPosition()
      #
      #     enemies = [gameState.getAgentState(i) for i in opponents]
      #     ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      #     pacmans = [a for a in enemies if a.isPacman and a.getPosition() != None]
      #
      #     distsToGhost = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      #     distsToPacman = [self.getMazeDistance(myPos, a.getPosition()) for a in pacmans]
      #
      #     distsToAllGhost = 0
      #     for d in distsToGhost:
      #         distsToAllGhost += d
      #     # features['distsToAllGhost'] = distsToAllGhost  # avoid being eaten by the ghost
      #     # weights['distsToAllGhost'] = 10
      #
      #     # if distsToGhost:
      #     #     # features['distsToClosestGhost'] = min(distsToGhost)
      #     #     if min(distsToGhost) > 2: # maintain a fixed distance between enemy
      #     #         # weights['distsToClosestGhost'] = -100
      #     #         weights['distsToAllGhost'] = -10
      #     #     else:
      #     #         # weights['distsToClosestGhost'] = 1
      #     #         weights['distsToAllGhost'] = -10
      #
      #     distsToAllPacmans = 0
      #     for d in distsToPacman:
      #         distsToAllPacmans += d
      #     features['distsToAllPacmans'] = distsToAllPacmans
      #     weights['distsToAllPacmans'] = 100
      #
      #     if distsToPacman:
      #       features['distsToClosestPacman'] = min(distsToPacman)  # defensive feature
      #       weights['distsToClosestPacman'] = 100
      #
      #     # eat the closest food first
      #     foodList = self.getFood(gameState).asList()
      #     if len(foodList) > 0:  # This should always be True,  but better safe than sorry
      #        minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      #        if minDistance < 20:
      #           features['eatFood'] = -len(foodList)
      #           features['distanceToFood'] = minDistance
      #     # weights['distanceToFood'] = 100

      return features * weights
  """
  def evaluate(self, gameState, action, turn, lastTurn):
    
    Computes a linear combination of features and feature weights
    
    # features = self.getFeatures(gameState, action, turn)
    # weights = self.getWeights(gameState, action)
    features = util.Counter()
    weights = util.Counter()
    if self.red:
        if turn == 0 or turn == 2:  # Maximizer features
            if turn == 0:  # Offensive agent features
                
                features:
                1) dotEaten
                2) totalScore
                3) closestGhost
                
                # oppSuccessor = self.getSuccessor(gameState, action, lastTurn)
                # dotEaten = -1
                if len(self.observationHistory) == 1:
                    dotEaten = 0
                else:
                    dotEaten = len(self.getFood(self.getPreviousObservation()).asList()) \
                           - len(self.getFood(self.getCurrentObservation()).asList())
                features['dotEaten'] = dotEaten

                totalScore = self.getScore(gameState)
                features['totalScore'] = totalScore

                closestGhost = self.getCloestGhosts(gameState, action, turn)
                features['closestGhost'] = closestGhost

                weights['dotEaten'] = 10
                weights['totalScore'] = 100
                weights['closestGhost'] = -50

            if turn == 2:  # defensive agent features
                successor = self.getSuccessor(gameState, action, turn)

                myState = successor.getAgentState(turn)
                myPos = myState.getPosition()

                features['onDefense'] = 1
                if myState.isPacman: features['onDefense'] = 0

                enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
                invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
                features['numInvaders'] = len(invaders)
                if len(invaders) > 0:
                    dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
                    features['invaderDistance'] = min(dists)

                if action == Directions.STOP: features['stop'] = 1
                rev = Directions.REVERSE[gameState.getAgentState(turn).configuration.direction]
                if action == rev: features['reverse'] = 1

                # {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
                weights['numInvaders'] = -1000
                weights['onDefense'] = 100
                weights['invaderDistance'] = -10
                weights['stop'] = -100
                weights['reverse'] = -2

        else:  # Minimizer Features
            # evaluation of opponents
            
            features: 
                1) distance to both our agents
                2) successor score
                3) distance to closest food
            
            if lastTurn == 0: # if last player is an offensive player, the opponent will defend its territory
                myteam = [gameState.getAgentState(i) for i in self.getTeam(gameState)]
                invaders = [a for a in myteam if a.isPacman and a.getPosition() != None]

                features['numInvaders'] = len(invaders)

                if len(invaders) > 0:
                    dists = [self.getMazeDistance(gameState.getAgentState(turn).getPosition(),
                                                  a.getPosition()) for a in invaders]
                    features['invaderDistance'] = min(dists)
            else:  # if last player is a defensive player, the opponent will try to avoid it
                # distToMyAgents
                distToClosestGhost = float("inf")
                myTeam = self.getTeam(gameState)
                for i in myTeam:
                    # distToMyAgents += self.getMazeDistance(gameState.getAgentState(i).getPosition(),
                    #                              gameState.getAgentState(turn).getPosition())
                    dist = self.getMazeDistance(gameState.getAgentState(turn).getPosition()
                                                  ,gameState.getAgentState(i).getPosition())
                    if dist < distToClosestGhost:
                        distToClosestGhost = dist

                features['distToClosestGhost'] = distToClosestGhost

            # successorScore
            # foodList = self.getFoodYouAreDefending(gameState).asList()
            # features['successorScore'] = -len(foodList)

            #if len(foodList) > 0:  # This should always be True,  but better safe than sorry
            #    oppPos = gameState.getAgentState(turn).getPosition()
            #    minDistance = min([self.getMazeDistance(oppPos, food) for food in foodList])
            #    features['distanceToFood'] = minDistance


            weights['distToMyAgents'] = -10
            weights['successorScore'] = 100
            weights['distanceToFood'] = -1
            weights['numInvaders'] = -1000
            weights['invaderDistance'] = -10
            weights['distToClosestGhost'] = -50
    else:
        distToLast = self.getMazeDistance(gameState.getAgentState(lastTurn).getPosition(),
                                          gameState.getAgentState(turn).getPosition())
        features['distToLast'] = distToLast

        weights['distToLast'] = -50
    return features * weights
  """

  def getFeatures(self, gameState, action): # features need to be redesigned to be fully informed
    # """
    # Returns a counter of features for the state
    # """
    global mode
    global holdFood
    features = util.Counter()

    # Offense
    foodList = self.getFood(gameState).asList()
    features['successorScore'] = -len(foodList)  # self.getScore(successor)

    # Compute distance to the nearest food

    if len(foodList) > 0:  # This should always be True,  but better safe than sorry
        myPos = gameState.getAgentState(self.index).getPosition()
        minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
        features['distanceToFood'] = minDistance

    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
        mode = 1 #defense
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        features['invaderDistance'] = min(dists)
    else:
        mode = 0 #offense

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    if holdFood == 1*2: # hold food * depth
        mode = 2
        features['goHome'] = self.getMazeDistance(self.start, gameState.getAgentState(self.index).getPosition())

    return features

  def getWeights(self, gameState, action):
    # """
    # Normally, weights do not depend on the gamestate.  They can be either
    # a counter or a dictionary.
    # """
    return {'distsToClosestEnemy': 5,
            'distsToClosestGhost': -10,
            'distsToClosestPacman': 1000,
            'distsToAllPacmans': 5000,
            'distsToAllEnemy': 10,
            'distsToAllGhost': -50,
            'currentScore': 100,
            'goHome': 10000,
            'distanceToFood': 1000}


  def offWeight(self, gameState, action):
      return {'successorScore': 100, 'distanceToFood': -1, 'goHome': -1000}
  def gohomeWeight(self, gameState, action):
      return {'goHome': -1}
  def defWeight(self, gameState, action):
      return {'numInvaders': -10000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
class OffensiveMinimaxAgent(MinimaxAgent):
    """
      A Minimax agent that seeks food. This is an agent
    """

    # def getFeatures(self, gameState, action):
    #     # features = util.Counter()
    #     # successor = self.getSuccessor(gameState, action, self.index)
    #     # foodList = self.getFood(successor).asList()
    #     # features['successorScore'] = -len(foodList)  # self.getScore(successor)
    #     #
    #     # # Compute distance to the nearest food
    #     #
    #     # if len(foodList) > 0:  # This should always be True,  but better safe than sorry
    #     #     myPos = successor.getAgentState(self.index).getPosition()
    #     #     minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
    #     #     features['distanceToFood'] = minDistance
    #
    #     features = util.Counter()
    #     foodList = self.getFood(gameState).asList()
    #     features['successorScore'] = -len(foodList)  # self.getScore(successor)
    #
    #     # Compute distance to the nearest food
    #
    #     if len(foodList) > 0:  # This should always be True,  but better safe than sorry
    #         myPos = gameState.getAgentState(self.index).getPosition()
    #         minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
    #         features['distanceToFood'] = minDistance
    #
    #     return features

    def getWeights(self, gameState, action):
        global mode
        if mode == 0:
            return self.offWeight(gameState, action)
        if mode == 2:
            return self.gohomeWeight(gameState, action)
        #default
        return self.offWeight(gameState, action)

class DefensiveMinimaxAgent(MinimaxAgent):
    """
      A Minimax agent that keeps its side Pacman-free.
    """

    # def getFeatures(self, gameState, action):
    #     features = util.Counter()
    #
    #     myState = gameState.getAgentState(self.index)
    #     myPos = myState.getPosition()
    #
    #     # Computes whether we're on defense (1) or offense (0)
    #     features['onDefense'] = 1
    #     if myState.isPacman: features['onDefense'] = 0
    #
    #     # Computes distance to invaders we can see
    #     enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    #     invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    #     features['numInvaders'] = len(invaders)
    #     if len(invaders) > 0:
    #         dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
    #         features['invaderDistance'] = min(dists)
    #     else:
    #         #Offense
    #         foodList = self.getFood(gameState).asList()
    #         features['successorScore'] = -len(foodList)  # self.getScore(successor)
    #
    #         # Compute distance to the nearest food
    #
    #         if len(foodList) > 0:  # This should always be True,  but better safe than sorry
    #             myPos = gameState.getAgentState(self.index).getPosition()
    #             minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
    #             features['distanceToFood'] = minDistance
    #
    #     if action == Directions.STOP: features['stop'] = 1
    #     rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    #     if action == rev: features['reverse'] = 1
    #
    #     return features

    def getWeights(self, gameState, action):
        global mode
        if mode == 0:
            return self.offWeight(gameState, action )
        if mode == 1:
            return self.defWeight(gameState, action)
        #default
        return self.defWeight(gameState, action)


class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)

