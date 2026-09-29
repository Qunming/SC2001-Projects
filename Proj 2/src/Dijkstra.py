#Used for part b of the assignment. Dijkstra's algorithm using adjacency list representation of the graph.
#Heapq is used to implement the priority queue for efficient retrieval of the next vertex with the smallest distance.
import heapq

INF = float('inf')
# sample graph represented as an adjacency matrix
# Index 0 = A, Index 1 = B, Index 2 = C, Index 3 = D
adjMatrix = [
    [0, 1, 4, INF],
    [4, 0, INF, 1],
    [2, INF, 0, 3],
    [INF, 1, 2, 0]
]

#Part B
#Adj List for part b. We need not store edges that does not exist. So we can store only the edges that exist in the graph.
#How to read: If we do adjList[0], we will get [(1, 4), (2, 2)], which means A is connected to B with weight 4 and A is connected to C with weight 2.
adjList = [
    [(1, 4), (2, 2), (4, 7)],          # A = 0
    [(0, 4), (3, 1), (5, 6)],          # B = 1
    [(0, 2), (3, 3), (4, 5)],          # C = 2
    [(1, 1), (2, 3), (5, 4), (6, 8)],  # D = 3
    [(0, 7), (2, 5), (6, 2), (7, 9)],  # E = 4
    [(1, 6), (3, 4), (6, 3), (7, 5)],  # F = 5
    [(3, 8), (4, 2), (5, 3), (7, 1)],  # G = 6
    [(4, 9), (5, 5), (6, 1)]           # H = 7
]

def dijkstra_list(adjList, source):
    #Get the number of vertices in the graph
    n = len(adjList)

    #Set distance of all vertices as infinite
    dist = [INF] * n 

    #Set distance of source vertex as 0
    dist[source] = 0

    #Make a MinHeap priority queue to store vertices that are being preprocessed
    # (distance, vertex)
    pq = [(0, source)]  # (distance, vertex) <- We use a tuple to store the distance and vertex, so that the priority queue can sort by distance.

    while pq:

        #Get vertex with the smallest distance
        current_distance, current_vertex = heapq.heappop(pq)

        #If the distance is greater than the recorded distance, skip processing
        if current_distance > dist[current_vertex]:
            continue

        #Examine all neighbors of the current vertex
        for neighbour, weight in adjList[current_vertex]:

            new_dist = current_distance + weight

            #Relaxation step: If the new distance is smaller, update the distance and add to the priority queue
            if new_dist < dist[neighbour]:
                dist[neighbour] = new_dist
                heapq.heappush(pq, (new_dist, neighbour))

    return dist

#Run the list and get the distances from source
distances = dijkstra_list(adjList, 3)

print(distances)








