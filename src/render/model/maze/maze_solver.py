#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

moves = ('UP', 'DOWN', 'EAST', 'WEST', 'SOUTH', 'NORTH')


def solve_maze_general(maze, algorithm):
	# select the right queue for each algorithm
	if algorithm == "BFS":
		fr = Fringe("FIFO")
		BFS(maze, fr)
	elif algorithm == "DFS":
		fr = Fringe("STACK")
		DFS(maze, fr)
	elif algorithm == "UCS":	
		fr = Fringe("PRIO")
		UCS(maze, fr)
	elif algorithm == "GREEDY":	
		fr = Fringe("PRIO")
		GREEDY(maze, fr)
	elif algorithm == "ASTAR":	
		fr = Fringe("PRIO")
		ASTAR(maze, fr)
	elif algorithm == "IDS":	
		fr = Fringe("PRIO")
		IDS(maze, fr)
	else:
		print("algorithm not found/implemented, exit")
		return


def BFS(maze, fringe):
	"""
	Can solve
		-default.maze
		-sequence.maze
		-greedy_astar.maze
	"""
	# Variables
	fr = fringe
	room = maze.getRoom(*maze.getStart())	# to find the node
	state = State(room, None)	# a node
	
	# Creates variables for searching
	fr.push(state)	
	explored = set()	# Create empty Explored list
	
	# Loop
	while not fr.isEmpty():	
		state = fr.pop()	
		explored.add(state)	# Add state to the explored list
		room = state.getRoom()
		
		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return		# Stops the program when the goal is found.

		for d in room.getConnections():
			newRoom, cost = room.makeMove(d, state.getCost())
			newState = State(newRoom, state, cost)
			if newState not in explored:
				fr.push(newState) 	
	print("not solved")
	fr.printStats()


def DFS(maze, fringe):
	"""
	TODO: Finish its still broken, wont solve anything.
	Can solve
		-
	"""
	fr = fringe
	room = maze.getRoom(*maze.getStart())  # to find the node
	state = State(room, None)  # a node

	# Creates variables for searching
	fr.push(state)
	explored = set()  # Create empty Explored list

	# Loop
	while not fr.isEmpty():
		state = fr.pop()
		explored.add(state)  # Add state to the explored list
		room = state.getRoom()

		if state.getCost() == evaluation:
			for move in moves:
				room.makeMove(room, move, 0)    # UP, DOWN, EAST, WEST, SOUTH, NORTH

		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return  # Stops the program when the goal is found.

		for d in room.getConnections():
			newRoom, cost = room.makeMove(d, state.getCost())
			newState = State(newRoom, state, cost)
			if newState not in explored:
				fr.push(newState)
				evaluation = newState.getCost

	print("not solved")
	fr.printStats()

	# # Variables
	# fr = fringe
	# room = maze.getRoom(*maze.getStart())	# to find the node
	# state = State(room, None)	## a node
	# fr.push(state)
	# explored = set()	# Create empty Explored list
	#
	# while not fr.isEmpty():
	# 	node = fr.pop()
	# 	room = node.getRoom()
	# 	explored.add(node)
	#
	# 	for d in room.getConnections():
	# 		newRoom, cost = room.makeMove(d, node.getCost())
	# 		newNode = State(newRoom, node, cost)
	# 		if newRoom.isGoal():
	# 			print("solved")
	# 			fr.printStats()
	# 			state.printPath()
	# 			maze.printMazeWithPath(state)
	# 			return		## Stops the program when the goal is found.
	#
	# 		if newNode not in explored:
	# 			fr.push(newNode)
	#
	# print("not solved")
	# fr.printStats()


def UCS(maze, fringe):
	"""
	Can solve
		-default.maze
		-sequence.maze 
	"""
	room = maze.getRoom(*maze.getStart())    # to find the node
	state = State(room, None)    # a node
	return bestFirstSearch(maze, fringe, lambda state: state.getCost())


def GREEDY(maze, fringe):
	"""
	Can solve
		-default.maze
		-sequence.maze 
		-greedy_astar.maze (most impornatly)
		-
	"""
	room = maze.getRoom(*maze.getStart())	# to find the node
	bestFirstSearch(maze, fringe, room.getHeuristicValue())


def ASTAR(maze, fringe):
	"""
	Can solve
		-default.maze
		-sequence.maze 
		-greedy_astar.maze (most impornatly)
	"""
	# Variables
	room = maze.getRoom(*maze.getStart())    # to find the node
	state = State(room, None)    # a node
	bestFirstSearch(maze, fringe, room.getHeuristicValue() + state.getCost())


def IDS(maze, fringe):
	return


def bestFirstSearch(maze, fringe, f):
	"""
	Base algorithm for the GREEDY, ASTAR, and UCS algorithms.
	"""
	
	# Variables
	fr = fringe
	room = maze.getRoom(*maze.getStart())    # to find the node
	state = State(room, None)    # a node
	
	# Creates variables for searching
	fr.push((f, state))	
	explored = set()    # Create empty Explored list
	
	# Loop
	while not fr.isEmpty():	
		state = fr.pop()
		statePriorityNumber = state[1].getCost()		
		room = state[1].getRoom()
		explored.add(state[1])    # Add state to the explored lsit
		for d in room.getConnections():
			newRoom, cost = room.makeMove(d, state[1].getCost())
			newState = State(newRoom, state[1], cost)
			newStatePrioirtyNumber = newState.getCost()
			if newState not in explored and newStatePrioirtyNumber > statePriorityNumber:
				if newRoom.isGoal():
					print("solved")
					fr.printStats()
					state[1].printPath()
					maze.printMazeWithPath(state[1])
					return    # Stops the program when the goal is found.
				fr.push((newStatePrioirtyNumber, newState))
	print("not solved")
	fr.printStats()