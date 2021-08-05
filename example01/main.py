import numpy as np
import matplotlib.pyplot as plt


class Swarm:

    def __init__(self, function, size=50, high=30, low=-30, cognitive=1, social=2, inertia=0.4, linspace=30):
        self._size = size
        self._function = function
        self._upper_bound = high
        self._lower_bound = low
        self._cognitive = cognitive
        self._social = social
        self._inertia = inertia
        self._linspace = linspace
        self.reset()

    def reset(self):
        self._velocity = self.init_random()
        self._population = self.init_random(self._upper_bound, self._lower_bound)

        self._last_evaluation = self._function(self._population[:,0], self._population[:,1])

        self._local_optimal_position = self._population.copy()
        self._local_optimal_value = self._last_evaluation.copy()

        idx = np.argmax(self._local_optimal_value)
        self._global_optimal_value = self._local_optimal_value[idx]
        self._global_optimal_position = self._local_optimal_position[idx]

        # Plotting information
        self._function_image = None
        self._axes = plt.axes(projection="3d")
        self._wait_for_key = True
        self._kill = False

    def init_random(self, high=1, low=0):
        return np.random.sample([self._size, 2]) * (high - low) + low

    def step(self):
        a = self._cognitive * np.random.sample(1) * (self._local_optimal_position - self._population)
        b = self._social * np.random.sample(1) * (self._global_optimal_position - self._population)

        self._velocity = self._inertia * np.random.sample(1) * self._velocity + a + b
        self._population += self._velocity

        self._population[self._population > self._upper_bound] = self._upper_bound
        self._population[self._population < self._lower_bound] = self._lower_bound

        self._last_evaluation = self._function(self._population[:,0], self._population[:,1])

        change = self._last_evaluation > self._local_optimal_value
        self._local_optimal_value = np.where(change, self._last_evaluation, self._local_optimal_value)
        change = np.array([change, change]).T
        self._local_optimal_position = np.where(change, self._population, self._local_optimal_position)

        idx = np.argmax(self._local_optimal_value)
        if self._local_optimal_value[idx] > self._global_optimal_value:
            self._global_optimal_value = self._local_optimal_value[idx]
            self._global_optimal_position = self._local_optimal_position[idx]

    def run(self, max_iterations=50, show=False):
        iteration = 0
        while iteration < max_iterations and not self._kill:
            iteration += 1
            if show:
                self.plot(iteration)
            self.step()
        print(f"Iterations: {iteration}")
        print(f"Best score: Z={self._global_optimal_value}")
        x, y = self._global_optimal_position
        print(f"Position of best score: X={x}, Y={y}")
        if show and not self._kill:
            plt.show()

    def plot_function(self):
        """ Plots function image """
        if self._function_image is None:
            x = np.linspace(self._lower_bound, self._upper_bound, self._linspace)
            y = np.linspace(self._lower_bound, self._upper_bound, self._linspace)
            X, Y = np.meshgrid(x, y)
            Z = self._function(X, Y)
            self._function_image = [X, Y, Z]
        # self._axes.plot_surface(*self._function_image, rstride=1, cstride=1, cmap='viridis', edgecolor="none")
        # self._axes.plot_wireframe(*self._function_image, color="g")
        self._axes.contour3D(*self._function_image, 50, cmap="viridis")

    def plot(self, iteration):
        """ Clears previous data and plots new data """
        plt.cla()
        self.plot_function()
        x = self._population[:,0]
        y = self._population[:,1]
        z = self._last_evaluation
        max_x, max_y = self._global_optimal_position
        max_z = self._global_optimal_value
        self._axes.scatter3D(x, y, z, c="r")
        self._axes.scatter(max_x, max_y, max_z, marker="*", s=500, c="b")

        self._axes.set_xlabel(f"x (best={max_x})")
        self._axes.set_ylabel(f"y (best={max_y})")
        self._axes.set_zlabel(f"z (best={max_z})")
        self._axes.text(self._lower_bound, self._lower_bound, 1.5*max_z, f"#Iteration {iteration}")

        plt.gcf().canvas.mpl_connect("key_press_event", self.key_press_handler)
        if self._wait_for_key:
            while not plt.waitforbuttonpress():
                pass
        else:
            plt.pause(0.5)

    def key_press_handler(self, event):
        if event.key == "c":
            self._wait_for_key = False
        elif event.key == "p":
            self._wait_for_key = True
        elif event.key == "e":
            self._kill = True

def scenario1():
    function = lambda x, y: x * np.exp(-(x**2 + y**2))
    swarm = Swarm(function=function, high=30, low=-30, linspace=300)
    return swarm

def scenario2():
    function = lambda x, y: np.sin(x) * np.cos(y)
    swarm = Swarm(function=function, high=7, low=-7, linspace=30)
    return swarm

def scenario3():
    function = lambda x, y: np.sin(10*(x**2+y**2))/10
    swarm = Swarm(function=function, high=1, low=-1, linspace=40)
    return swarm

if __name__ == "__main__":
    # swarm = scenario1()
    swarm = scenario2()
    # swarm = scenario3()
    swarm.run(show=True)
