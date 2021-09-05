import util

"""
Data sturctures we will use are stack, queue and priority queue.

Stack: first in last out
Queue: first in first out
    collection.push(element): insert element
    element = collection.pop() get and remove element from collection

Priority queue:
    pq.update('eat', 2)
    pq.update('study', 1)
    pq.update('sleep', 3)
pq.pop() will return 'study' because it has highest priority 1.

"""

"""
problem is a object has 3 methods related to search state:

problem.getStartState()
Returns the start state for the search problem.

problem.isGoalState(state)
Returns True if and only if the state is a valid goal state.

problem.getChildren(state)
For a given state, this should return a list of tuples, (next_state,
step_cost), where 'next_state' is a child to the current state, 
and 'step_cost' is the incremental cost of expanding to that child.

"""
def myDepthFirstSearch(problem):
    visited = {}
    frontier = util.Stack()

    frontier.push((problem.getStartState(), None))

    while not frontier.isEmpty():
        state, prev_state = frontier.pop()

        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]                
        
        if state not in visited:
            visited[state] = prev_state

            for next_state, step_cost in problem.getChildren(state):
                frontier.push((next_state, state))

    return []

def myBreadthFirstSearch(problem):
    visited = {}
    frontier = util.Queue() #申请一个队列

    frontier.push((problem.getStartState(), None))

    while not frontier.isEmpty():
        state, prev_state = frontier.pop()

        if problem.isGoalState(state):
            action = [state]
            while prev_state != None:
                action.append(prev_state)
                prev_state = visited[prev_state]
            return action[::-1]                
        
        if state not in visited:
            visited[state] = prev_state

            for next_state, step_cost in problem.getChildren(state):
                frontier.push((next_state, state))

    return []

def myAStarSearch(problem, heuristic):
    # YOUR CODE HERE
    start=problem.getStartState()
    visited = {}
    cost = {} #存储已走过的cost
    frontier = util.PriorityQueue()

    frontier.push((start, None),0)
    mincost=0 #负责取前面走过的路径耗费值
    ncost=0
    cost[start]=0
    while not frontier.isEmpty():
        state, prev_state= frontier.pop()
        mincost=cost[state]
        
        
        if problem.isGoalState(state): 
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]
        
        if state not in visited:
            visited[state] = prev_state
            next_states=problem.getChildren(state)
            
            for next_state,step_cost in next_states:
                if next_state not in visited:
                    cost[next_state]=step_cost+mincost #保存权值
                    nextcost=cost[next_state]+heuristic(next_state)
                    frontier.update((next_state, state),nextcost)         
    return []

"""
Game state has 4 methods we can use.

state.isTerminated()
Return True if the state is terminated. We should not continue to search if the state is terminated.

state.isMe()
Return True if it's time for the desired agent to take action. We should check this function to determine whether an agent should maximum or minimum the score.

state.getChildren()
Returns a list of legal state after an agent takes an action.

state.evaluateScore()
Return the score of the state. We should maximum the score for the desired agent.

"""
class MyMinimaxAgent():

    def __init__(self, depth):
        self.depth = depth

    def minimax(self, state, depth):
        if state.isTerminated():
            return None, state.evaluateScore()        

        best_state, best_score = None, -float('inf') if state.isMe() else float('inf')

        for child in state.getChildren():
            # YOUR CODE HERE
            value=self.min_value(child)
            if value is not None and value >best_score:
                best_score=value
                best_state=child
            #util.raiseNotDefined()
        
        return best_state, best_score
    
    def max_value(self,state,depth=0):
        #判断如果到达了完结状态
        if state.isTerminated() or depth == self.depth:
            return state.evaluateScore()
        v=-float('inf')
        #此处由于只有一个吃豆人，因此吃豆人的后继结点始终是min结点
        for child in state.getChildren():
            value=self.min_value(child,depth)
            if value is not None and value>v:
                v=value
        return v
        
    def min_value(self,state,depth=0):
        #判断如果到达了完结状态
        if state.isTerminated() or depth == self.depth:
            return state.evaluateScore()
        v=float('inf')
        #此处其实要注意的是Min的孩子结点不一定是max结点，因为不止有一个和吃豆人对立的Agent，因此要对孩子结点进行判断
        for child in state.getChildren():
            if child.isMe() == True:
                value=self.max_value(child,depth+1)
            else:
                value=self.min_value(child,depth)
            if value is not None and value<v:
                v=value
        return v
            
    def getNextState(self, state):
        best_state, _ = self.minimax(state, self.depth)
        return best_state

class MyAlphaBetaAgent():

    def __init__(self, depth):
        self.depth = depth

    def getNextState(self, state):
        # YOUR CODE HERE
        return self.max_value(state)[1]
        #util.raiseNotDefined()
    
    def max_value(self,state,depth=0,alpha=-float('inf'),beta=float('inf')):
        if depth == self.depth or state.isTerminated():
            return state.evaluateScore(),None
        
        #先判断是否为终止的条件，否则遍历
        
        maxvalue=-float('inf')
        best_state=None
        #此处由于只有一个吃豆人，因此吃豆人的后继结点始终是min结点
        for child in state.getChildren():
            value=self.min_value(child,depth,alpha,beta)[0]
            if value is not None and (maxvalue == None or value > maxvalue):
                maxvalue=value
                best_state=child
            #如果v>β，则直接返回v
            if value is not None and value>beta:
                return value,child
            #更新α的值
            if value is not None and value>alpha:
                alpha=value
        return maxvalue,best_state
    
    
    def min_value(self,state,depth=0,alpha=-float('inf'),beta=float('inf')):
        if depth == self.depth or state.isTerminated():
            return state.evaluateScore(),None
        
        minvalue=float('inf')
        best_state=None
        
        for child in state.getChildren():
            #此处其实要注意的是Min的孩子结点不一定是max结点，因为不止有一个和吃豆人对立的Agent，因此要对孩子结点进行判断
            if child.isMe() == True:
                value=self.max_value(child,depth+1,alpha,beta)[0]
            else:
                value=self.min_value(child,depth,alpha,beta)[0]
                
            if value is not None and (minvalue == None or value < minvalue):
                minvalue=value
                best_state=child
            #如果v<α，则直接返回v
            if value is not None and value<alpha:
                return value,child
            #更新β的值
            if value is not None and value<beta:
                beta=value
        return minvalue,best_state
    

