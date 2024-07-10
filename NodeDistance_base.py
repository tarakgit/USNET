import heapq
import random
import matplotlib.pyplot as plt

# Sample graph with adjacent node list in diagram
graph = {
    1: [2, 6],
    2: [1, 3, 6],
    3: [2, 4, 7],
    4: [3, 5, 7],
    5: [4, 8],
    6: [1, 2, 7, 11],
    7: [3, 4, 6, 8, 9],
    8: [5, 7, 9, 10],
    9: [7, 8, 11, 12],
    10: [8, 13, 14],
    11: [6, 9, 15],
    12: [9, 13, 16],
    13: [10, 12, 14, 17],
    14: [10, 13, 18],
    15: [11, 16, 19],
    16: [12, 15, 17, 21],
    17: [13, 16, 18, 22],
    18: [14, 17, 24],
    19: [15, 20],
    20: [19, 21],
    21: [16, 20, 22],
    22: [17, 21, 23],
    23: [22, 24],
    24: [18, 23]
}

# Initial resources at each node
initial_resources = {i: {'cpu': 100, 'bandwidth': 100} for i in range(1, 25)}

def reset_resources():
    return {i: {'cpu': 100, 'bandwidth': 100} for i in range(1, 25)}

# Function for find shortest path with CPU and bandwidth limits of cpu of 2 and network bandwith of 5 min
def find_shortest_path(graph, start, end, resources):
    # Do not initiate any action if start and destination nodes are the same
    if start == end:
        return "No action initiated"
    
    queue = [(0, start, [])]
    visited = set()
    
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node in visited:
            continue
        
        visited.add(node)
        path = path + [node]
        
        # If we've reached the destination
        if node == end:
            return path
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                # Calculate remaining CPU and bandwidth after visiting this node
                remaining_cpu = resources[node]['cpu'] - 2
                remaining_bandwidth = resources[node]['bandwidth'] - 5
                
                # Check if constraints are met
                if remaining_cpu >= 2 and remaining_bandwidth >= 5:
                    resources[node]['cpu'] = remaining_cpu
                    resources[node]['bandwidth'] = remaining_bandwidth
                    heapq.heappush(queue, (cost + 1, neighbor, path))
                else:
                    return "Cancelled"
    
    return "Cancelled"

# Function to generate random requests
def generate_random_request(nodes):
    while True:
        start_node = random.choice(nodes)
        end_node = random.choice(nodes)
        if start_node != end_node:
            return start_node, end_node

# Simulate multiple random requests to our graph
def simulate_requests(graph, num_requests):
    nodes = list(graph.keys())
    resources = reset_resources()
    requests = []
    cancelled_requests = 0
    
    successful_requests = []
    
    for i in range(num_requests):
        start_node, end_node = generate_random_request(nodes)
        path = find_shortest_path(graph, start_node, end_node, resources)
        result = "Success" if path != "Cancelled" else "Cancelled"
        
        if result == "Cancelled":
            cancelled_requests += 1
        
        requests.append((start_node, end_node, result))
        
        successful_requests.append(i + 1 - cancelled_requests)
        
    threshold = len(successful_requests) - 1 if cancelled_requests > 0 else num_requests
    
    return requests, successful_requests, threshold

# Example: Simulate 100 random requests
num_requests = 200
requests, successful_requests, threshold = simulate_requests(graph, num_requests)

# Print the results
print(f"Threshold: {threshold} requests")
for i, (start, end, result) in enumerate(requests):
    print(f"Request {i+1}: from node {start} to node {end} - {result}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(range(1, num_requests + 1), successful_requests, label="Successful Requests")
plt.axvline(x=threshold, color='r', linestyle='--', label="Threshold")
plt.xlabel("Total Number of Requests")
plt.ylabel("Successful Requests")
plt.title("Total Requests vs Successful Requests with Threshold")
plt.legend()
plt.show()
