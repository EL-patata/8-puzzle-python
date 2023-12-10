from treeds import Tree
import time


class Search(Tree):
    def __init__(self, goal_test, next_states, state=None):
        if state is not None:
            super().__init__(root_nodes=[state], auto_correct=True)
            self.state = state
        self.algorithms = {
            'bfs': self.bfs,
            'dfs': self.dfs,
        }
        self.goal_test = goal_test
        self.next_states = next_states
        self.quit = False

    def set_state(self, state):

        self.state = state
        super().__init__(root_nodes=[state], auto_correct=True)

    def non_visited_states(self, state) -> list:

        self.add_children(state, self.next_states(state))
        return self.get_children(state)

    def search(self, algorithm: str, verbose=True) -> list:

        if type(algorithm) != str:
            raise Exception("type(algorithm) must be string.")
        try:
            start_time = time.time()
            solution = self.algorithms[algorithm](verbose=verbose)
            time_taken = str(time.time() - start_time).split('.')
            fmt_time = time_taken[0] + '.' + time_taken[1][:2]
            if verbose:
                print("Time taken:", fmt_time)
            return solution
        except KeyError:
            raise Exception(f"No algorithm named {algorithm} found.")

    # Search Methods
    def bfs(self, verbose: bool = True) -> list:

        if verbose:
            print("**************Solving(BFS)*****************")
        depth_count = 0
        states = 1
        queue = [self.state]
        while len(queue) != 0:
            if verbose:
                print(f"\rDepth: {depth_count} | States: {states}", end='')
            new_open = []
            for state in queue:
                if self.quit:
                    quit()
                if self.goal_test(state):
                    if verbose:
                        print()
                    return self.get_path(state)
                new_open += self.non_visited_states(state)
            queue = new_open
            depth_count += 1
            states += len(queue)
        print(self.tree)
        raise Exception("Can't find Solution.")

    def dfs(self, verbose: bool = True) -> list:

        if verbose:
            print("**************Solving(DFS)*****************")
        depth_count = 0
        states = 1
        stack = [self.state]
        while len(stack) != 0:
            if verbose:
                print(f"\rDepth: {depth_count} | States: {states}", end='')
            if self.quit:
                quit()
            state = stack.pop()
            if self.goal_test(state):
                if verbose:
                    print()
                return self.get_path(state)
            nvs = self.non_visited_states(state)
            if len(nvs) == 0:
                self.delete(state)
                depth_count -= 1
            stack += nvs
            self.add_children(state, nvs)
            depth_count += 1
            states += len(nvs)
        raise Exception("Can't find Solution.")
