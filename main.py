import heapq

def input_circles():
    """Collect input for circles, intersections, and routing."""
    circles = {}
    intersections = []
    
    # Input circles
    num_circles = int(input("Enter the number of bus circles: "))
    for _ in range(num_circles):
        circle_name = input(f"Enter name for circle {_ + 1}: ").strip()
        stops = [stop.strip() for stop in input(f"Enter stops for {circle_name} circle (comma-separated): ").split(',')]
        circles[circle_name] = stops
    
    # Input intersections
    num_intersections = int(input("Enter number of intersections between circles: "))
    for _ in range(num_intersections):
        first_circle = input("Enter first circle name: ").strip()
        second_circle = input("Enter second circle name: ").strip()
        
        common_stops = [stop.strip() for stop in 
            input(f"Enter common stops between {first_circle} and {second_circle} (comma-separated): ").split(',')]
        
        intersections.append((first_circle, second_circle, common_stops))
    
    # Start and destination
    start_stop = input("Enter start stop: ").strip()
    end_stop = input("Enter end stop: ").strip()
    
    return circles, intersections, start_stop, end_stop

def build_graph(circles, intersections):
    """Create a comprehensive graph of bus routes."""
    graph = {}
    
    # Add connections within circles
    for circle_name, stops in circles.items():
        for i in range(len(stops)):
            current_stop = stops[i]
            next_stop = stops[(i + 1) % len(stops)]  # Circular route
            
            # Initialize graph entries if not present
            if current_stop not in graph:
                graph[current_stop] = {}
            if next_stop not in graph:
                graph[next_stop] = {}
            
            # Add bidirectional edges
            graph[current_stop][next_stop] = 5
            graph[next_stop][current_stop] = 5
    
    # Add zero-cost intersections between circles
    for first_circle, second_circle, common_stops in intersections:
        for stop in common_stops:
            # Initialize graph entries if not present
            if stop not in graph:
                graph[stop] = {}
            
            # Add zero-cost connections for intersections
            for other_stop in common_stops:
                if stop != other_stop:
                    graph[stop][other_stop] = 0
    
    return graph


def a_star_search(graph, start, goal):
    """A* search algorithm to find the optimal route."""
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    while open_set:
        _, current, path = heapq.heappop(open_set)
        
        if current == goal:
            return path, g_score[current]
        
        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score, neighbor, path + [neighbor]))
    
    return None, float('inf')

def solve_routing():
    """Main routing solution function."""
    circles, intersections, start_stop, end_stop = input_circles()
    graph = build_graph(circles, intersections)
    
    path, time = a_star_search(graph, start_stop, end_stop)
    
    if path:
        print("\nRouting Solution:")
        print(f"Start: {start_stop}")
        print(f"Destination: {end_stop}")
        print(f"Path: {' -> '.join(path)}")
        print(f"Total Travel Time: {time} minutes")
    else:
        print("No valid route found.")

def main():
    solve_routing()

if __name__ == "__main__":
    main()
