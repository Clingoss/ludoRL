import numpy as np
import random

#SARSA is on-policy
#Q-learning is off-policy

class RL:

    actions = [1,2,3,4,5,6]
    world = [0,1,2,2,2,2,3,2,2,4,2,2,3,2,5,2,2,2,2,3,2,2,4,2,2,3,2,5,2,2,2,2,3,2,2,4,2,2,3,2,5,2,2,2,2,3,2,2,4,2,2,3,6,6,6,6,6,7]
    # [OtC,startPos,blank,star,globe,enemyGlobe,homeStrech,home]
    rewards = [-2.0,1.0,-0.1,0.0,1.0,-1.0,1.0,2.0]
    
    KILL = 1.0
    PROTECT = 1.0
    GOAL_POSITION = 57

    action2 = ['kill','safe','unsafe','OtC','home']
    world2 = ['OtC','safe','unsafe','home']
    reward2 = [[2.0,1.0,-5.0,-5.0,-5.0],[1.0,0.0,-0.5,-2.0,2.0],[1.0,2.0,-0.1,-2.0,2.0],[-5.0,-5.0,-5.0,-5.0,-5.0]]

    def __init__(self,alpha=0.1,gamma=0.1,epsilon=0.1,eps=20):
        # Our step size / learing rate 
        self.alpha = alpha 
        # Discount factor
        self.gamma = gamma
        # exploration factor
        self.epsilon = epsilon
        # Episodes to run 
        self.eps = eps

        self.Q = np.full((4,len(self.actions),len(self.world)), 0.0)
        self.Qsq = np.full((4,len(self.action2),len(self.world2)),0.0)

        self.roll = 0
        self.lastState = ['OtC','OtC','OtC','OtC']
        self.lastAction = ['OtC','OtC','OtC','OtC']

    def runSpecial(self,playerPos,offset,enemyPos,roll):
        decisions = np.zeros(len(playerPos))
        self.roll = roll
        for i,pos in enumerate(playerPos):
            decisions[i]=self.specialQlearning(i,pos,offset,playerPos,enemyPos)
        
        p = random.randint(0,100)
        if p <= self.epsilon*100:
            p = random.randint(0,4)
            return p
        else :
            return np.argmax(decisions)
    
    def getState(self,pos):
        typePos = self.world[pos]
        if typePos == 0:
            return self.world2[0]
        elif typePos == 1 or typePos == 4 or typePos == 6:
            return self.world2[1]
        elif typePos == 2 or typePos == 3 or typePos == 5:
            return self.world2[2]
        else :
            return self.world2[3]

    def getProtect(self,player,pos,playerPos):
        for i in range(len(playerPos)):
            if i != player:
                if playerPos[i] == pos+self.roll:
                    return 1        
        return 0

    def getActions(self,player,pos,offset,playerPos,enemyPos):
        actualState = -1
        subReward=0.0

        # Get the next state from the world
        if pos == 0 and self.roll==6:
            return self.action2[1]
        elif pos == 0:
            return self.action2[3]
        elif pos+self.roll > self.GOAL_POSITION:
            return self.action2[1]
        else:
            if self.world[pos+self.roll]==3:
                if self.world[pos+self.roll+1]==6:
                    self.roll += 0
                elif self.world[pos+self.roll+6]==3:
                    self.roll += 6
                elif self.world[pos+self.roll+7]==3:
                    self.roll +=7
                if self.getProtect(player,pos,playerPos):
                    return self.action2[1]
                return self.action2[2]
        
            actualState = pos + self.roll + offset
            if actualState > 51:
                # to account for the first grid being 0
                actualState -= 52

            if enemyPos[actualState] and self.world[pos + self.roll]==4:
                return self.action2[3]
            elif enemyPos[actualState] and self.world[pos + self.roll]==5:
                return self.action2[3]
            elif enemyPos[actualState]>1:
                return self.action2[3]
            elif enemyPos[actualState]:
                return self.action2[0]
            elif self.getProtect(player,pos,playerPos):
                return self.action2[1]
            elif self.world[pos+self.roll]==4 or self.world[pos+self.roll]==6:
                return self.action2[1]
            elif self.world[pos+self.roll]==2 or self.world[pos+self.roll]==5:
                return self.action2[2]
            else:
                return self.action2[4]
   

    def specialQlearning(self,player,startState,offset,playerPos,enemyPos):
        state = self.getState(startState)
        if state == 'OtC' and self.lastState[player] != 'OtC':
            self.Qsq[player][self.action2.index(self.lastAction[player])][self.world2.index(self.lastState[player])]-=1.0

        self.lastState[player]=state

        action = self.getActions(player,startState,offset,playerPos,enemyPos)
        self.lastAction[player]=action

        maxAction = -5.0
        for a in range(len(self.action2)):
                try:
                    if not(action == 'kill'):
                        if maxAction <= self.Qsq[player][a][self.world2.index(action)]:
                            maxAction = self.Qsq[player][a][self.world2.index(action)]
                    elif state == 'OtC': 
                        if maxAction <= self.Qsq[player][a][self.world2.index('safe')]:
                            maxAction = self.Qsq[player][a][self.world2.index('safe')]
                    else:
                        if maxAction <= self.Qsq[player][a][self.world2.index('unsafe')]:
                            maxAction = self.Qsq[player][a][self.world2.index('unsafe')]
                except:
                    break
        
        self.Qsq[player][self.action2.index(action)][self.world2.index(state)] = self.Qsq[player][self.action2.index(action)][self.world2.index(state)] + self.alpha * (self.reward2[self.world2.index(state)][self.action2.index(action)] + self.gamma*maxAction-self.Qsq[player][self.action2.index(action)][self.world2.index(state)])
        return self.Qsq[player][self.action2.index(action)][self.world2.index(state)]

    def runQ(self,playerPos,offset,enemyPos,roll):
        decisions = np.zeros(len(playerPos))
        for i,pos in enumerate(playerPos):
            for _ in range(self.eps):
                self.Qlearning(i,pos,offset,playerPos,enemyPos)
            decisions[i]=self.Q[i][roll-1][pos]
        return np.argmax(decisions)
    
    def runSARSA(self,playerPos,offset,enemyPos,roll):
        decisions = np.zeros(len(playerPos))
        for i,pos in enumerate(playerPos):
            for _ in range(self.eps):
                self.Sarsa(i,pos,offset,playerPos,enemyPos)
            decisions[i]=self.Q[i][roll-1][pos]
        return np.argmax(decisions)
            
    def epsilonPolicy(self,player,pos,Q):
        possibleActions = { k:1/len(self.actions) for k in self.actions }
        p = random.randint(0,100)
        for action in self.actions:
            possibleActions[action] = Q[player][self.actions.index(action)][pos]
        if p <= self.epsilon*100 or all(value == 0.0 for value in possibleActions.values()):
            actionRun = random.randint(0,len(self.actions)-1)
            return self.actions[actionRun]
        else :
            actionRun = max(possibleActions, key=possibleActions.get)
            return actionRun
    
    def getNextState(self,currentState,action,offset,enemyPos,playerPos,player):
        actualState = -1
        subReward=0.0

        # Get the next state from the world
        if currentState == 0 and action==6:
            nextState = currentState+1
        elif currentState == 0:
            nextState = currentState
        elif currentState+action > self.GOAL_POSITION:
            nextState = currentState + action
            overshot = nextState - self.GOAL_POSITION
            nextState = self.GOAL_POSITION - overshot-1
            subReward=-2.0
        else:
            if self.world[currentState+action]==3:
                if self.world[currentState+action+1]==6:
                    action += 0
                elif self.world[currentState+action+6]==3:
                    action += 6
                elif self.world[currentState+action+7]==3:
                    action +=7
        
            actualState = currentState + action + offset
            if actualState > 51:
                # to account for the first grid being 0
                actualState -= 52

            if enemyPos[actualState] and self.world[currentState+action]==4:
                nextState = 0
            elif enemyPos[actualState] and self.world[currentState+action]==5:
                nextState = 0
            elif enemyPos[actualState]>1:
                nextState = 0
            else:
                nextState = currentState+action
        
        protect = 0
        if nextState > 0:
            for i in range(len(playerPos)):
                if i != player:
                    if playerPos[i] == nextState:
                        protect = 1
        
        return subReward,protect,nextState,actualState

    def Qlearning(self,player,startState,offset,playerPos,enemyPos):

        # set start state as current state
        currentState = startState
        
        while self.world[currentState]!=len(self.rewards)-1:
            
            # Get the possible actions and their probabilities that our policy says 
            # that the agent should perform in the current state: 
            action = self.epsilonPolicy(player,currentState,self.Q)
            
            # Pick a weighted random action: 
            actionNum = self.actions.index(action)

            subReward,protect,nextState,actualState=self.getNextState(currentState,action,offset,enemyPos,playerPos,player)

            # Get the reward for performing the action
            if enemyPos[actualState]:
                reward = self.rewards[self.world[nextState]]+self.KILL
            elif protect:
                reward = self.rewards[self.world[nextState]]+self.PROTECT
            else:
                reward = self.rewards[self.world[nextState]]+subReward
            
            # calculate the optimal action value for next state
            maxAction = 0.0
            for a in range(len(self.actions)):
                try:
                    if maxAction <= self.Q[player][a][nextState]:
                        maxAction = self.Q[player][a][nextState]
                except:
                    break
            
            # Calculate the action-value
            self.Q[player][actionNum][currentState] = self.Q[player][actionNum][currentState] + self.alpha * (reward + self.gamma*maxAction-self.Q[player][actionNum][currentState])

            # Move the agent to the new state
            currentState = nextState

    def Sarsa(self,player,startState,offset,playerPos,enemyPos):
        # set start state to be the current state
        currentState = startState
        
        # Get the possible actions and their probabilities that our policy says 
        # that the agent should perform in the current state: 
        action = self.epsilonPolicy(player,currentState,self.Q)
        
        while self.world[currentState]!=len(self.rewards)-1:
            
            # Pick a weighted random action: 
            actionNum = self.actions.index(action)

            subReward,protect,nextState,actualState=self.getNextState(currentState,action,offset,enemyPos,playerPos,player)

            # Get the reward for performing the action
            if enemyPos[actualState]:
                reward = self.rewards[self.world[nextState]]+self.KILL
            elif protect:
                reward = self.rewards[self.world[nextState]]+self.PROTECT
            else:
                reward = self.rewards[self.world[nextState]]+subReward
            
            # Get the next action using policy and next state
            nextAction = self.epsilonPolicy(player,currentState,self.Q)
            nextActionNum = self.actions.index(nextAction)
            
            # calculate the action value
            self.Q[player][actionNum][currentState] = self.Q[player][actionNum][currentState] + self.alpha * (reward + self.gamma*self.Q[player][nextActionNum][nextState]-self.Q[player][actionNum][currentState])

            # Move the agent to the new state
            currentState = nextState
            
            # Set the next action to be the new action to be used
            action = nextAction