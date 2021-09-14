import random
import numpy as np
import matplotlib.pyplot as plt

#important parameters for the lattice size and iterations 
#networkSize1 is size of network for classic naming game
#networkSize2 is size of network for 2d4n game
iterations = 75000
networkSize1 = 500
networkSize2 = 20

# R determines the random distribution of reputation among agents (in this code, R = 0.75 means there will be 75 % agents in network with a reputation of -5, and the other 25% a reputation of 5)
R = 0.50
#generate a completely random string of all upper-case letters of a random length of 2-6 characters
def generateRandomString(): 
    # a function to generate a random string of 2-6 uppercase alphabetical letters
    string = ""
    size = random.randint(2, 6)
    for _ in range(size):
        randomChar = chr(random.randint(65, 90))
        string += randomChar
    return string


#our agent, containing a unique ID, its reputation, wordBank, and neighbors
class Agent:
    def __init__(self, ID, reputation, wordBank, neighbors = None,):
        self.ID = ID
        self.reputation = reputation
        self.wordBank = wordBank
        if neighbors is None:
            neighbors = []
        self.neighbors = neighbors


def make_classic_network(size):
    #function to make a network of agents for the classic Naming Game
    #size: number of agents in the network
    agents = []
    for i in range(size):
        random_chance = random.uniform(0, 1)
        if random_chance <= R:
            agents.append(Agent(i, -5, [], []))
        else: 
            agents.append(Agent(i, 5, [], []))
    return agents

def make_2d4n(size):
    # a function for making a 2d4n network of agents
    # size: side length of the network (total number of agents is size^2)

    n = int(size)
    agents = []

    ## Construct network connections
    # Initialize all agents
    for i in range(0,n**2):
        random_chance = random.uniform(0, 1)
        if random_chance <= R:
            agents.append(Agent(i, -5, [], [i - n, i - 1, i+1, i + n]))
        else: 
            agents.append(Agent(i, 5, [], [i - n, i - 1, i+1, i + n]))

    # top row, middle
    for i in range(1,size-1):
        agents[i].neighbors = [i-1,i+1,i+n,i+(n-1)*n]
    # bottom row, middle
    for i in range(n*(n-1)+1,n**2-1):
        agents[i].neighbors = [i-1,i+1,i-n,i-(n-1)*n]
    # left column, middle
    for i in range(n,n**2,n):
        agents[i].neighbors = [i-n,i+n,i+1,i+n-1]
    # right column, middle
    for i in range(n-1,n**2,n):
        agents[i].neighbors = [i-n,i+n,i-1,i-n+1]

    # topleft
    agents[0].neighbors = [1,n,n-1,n*(n-1)]
    # topright
    agents[n-1].neighbors = [n-2,0,2*n-1,n**2-1]
    # botleft
    agents[n*(n-1)].neighbors = [n*(n-1)+1,n**2-1,n*(n-2),0]
    # botright
    agents[n**2-1].neighbors = [n**2-2,n**2-n-1,n*(n-1),n-1]

    return agents

def shout1(talker, receiver):
    # a function for agent-agent interaction
    # talker: an agent
    # receiver: a different agent, not the talker agent
    #if the talker has nothing to shout, it creates a random string to shout. then, it picks a random word from its word bank to shout
    if len(talker.wordBank) == 0:
        talker.wordBank.append(generateRandomString())
    word = random.choice(talker.wordBank)
    
    #success: talker and receiver keep word in inventory and remove everything else
    
    if word in receiver.wordBank:
        talker.wordBank.clear()
        receiver.wordBank.clear()
        talker.wordBank.append(word)
        receiver.wordBank.append(word)
        talker.reputation += 1
        #failure: reputations are compared; if talker's reputation is greater, receiver adds word to bank. otherwise, talker adds new word to bank and reputation decrements
    else:
        if talker.reputation > receiver.reputation:
            receiver.wordBank.append(word)
        else: 
            talker.wordBank.append(generateRandomString())
            talker.reputation -= 1

def shout2(talker, receivers):
    # a function for agent-agent interactions in 2d4n network
    # talker: an agent
    # receivers: an array of neighbor indices from agent's neighbors parameter
    if len(talker.wordBank) == 0:
        talker.wordBank.append(generateRandomString())
    word = random.choice(talker.wordBank)
    #success
    for receiverIndex in receivers:
        receiver = network[receiverIndex]
        if word in receiver.wordBank:
            talker.wordBank.clear()
            receiver.wordBank.clear()
            talker.wordBank.append(word)
            receiver.wordBank.append(word)
            talker.reputation += 1
            #failure
        else:
#            if talker.reputation > receiver.reputation:
            receiver.wordBank.append(word)
#            else: 
#                talker.wordBank.append(generateRandomString())
#                talker.reputation -= 1

#average length to show convergence

averageLengths = []


def playRound(network):
    # function: play out an interaction between agent and neighbors
    # network: an array of agents in the form of a 2d4n lattice
    agent1 = random.choice(network)
    shout2(agent1, agent1.neighbors)

#pick 2 random agents as shouter and receiver, but randomize the receiver if the random selects the exact same agent
#find average length of word bank among all agents for each iteration
def playGame1(network):
    for _ in range(iterations):
        avg = 0
        agent1 = random.choice(network)
        agent2 = random.choice(network)
        while agent1 == agent2:
            agent2 = random.choice(network)
        shout1(agent1, agent2)
        
        for i in range(networkSize1):
            avg += len(network[i].wordBank)
        averageLengths.append(avg / (networkSize1))

def playGame2(network):
    for _ in range(iterations):
        avg = 0
        playRound(network)
        for i in range(len(network)):
            avg += len(network[i].wordBank)
        averageLengths.append(avg / (networkSize2**2))


game = int(input("Enter game to play: 1 for classic Naming Game, 2 for 2d4n Naming Game"))
network = []
if game == 1:
    network = make_classic_network(networkSize1)
    playGame1(network)
elif game == 2:
    network = make_2d4n(networkSize2)
    playGame2(network)
    for i in range(networkSize2**2):
        current_agent = network[i]
        current_agent.wordBank.sort()
        print(current_agent.wordBank)
    
#graph showing our convergence
x = np.arange(1, iterations + 1)
y = averageLengths

plt.title("Naming Game Simulation")  
plt.xlabel("Iteration")  
plt.ylabel("Average # of words in word bank across network")  
plt.plot(x, y, color = "blue")  
plt.show() 
