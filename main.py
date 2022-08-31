import numpy as np
import plotly.express as px
from connectivity import build_graph


class Params:
    """
    parameters for simulation
    """
    algorithm = ["ermentraut"][0]  # firefly algorithm. Choose: index
    time_delta = 0.002
    num_agents = 200  # 800 works well
    omega_high = 3  # upper bound frequency
    omega_low = 0.8  # lower bound frequency
    omega_common = 2  # common omega
    num_neighbors = 30  # how many neighbors for each agent # 30 often converges
    epsilon = 0.01  # tendency for the agent to move to natural frequecy
    iterations = 100


class Fireflies():

    def __init__(self, params) -> None:
        self.p = params
        self.phases = np.random.rand(self.p.num_agents)
        self.omegas = np.random.uniform(
            low=self.p.omega_low, high=self.p.omega_high, size=self.p.num_agents)
        self.timedeltas = self.p.time_delta / self.omegas
        self.stepcount = 0
        self.flashcount = 0
        self.history = {"firefly": [], "timestep": []}
        self.cm = build_graph(Params)
    # def _scale_timedeltas

    def step(self):
        """
        One simulation step
        """

        # first advance phase
        self.phases += self.timedeltas
        # check for flashes
        self.flashed = self.phases > 1

        self.save_history()

        self.integrate_flash()

    def save_history(self):
        """
        saves each timestep which fireflies flashed
        """

        flashed_fireflies = np.where(self.flashed == True)[0].tolist()

        for firefly in flashed_fireflies:
            self.history['firefly'].append(firefly)
            self.history['timestep'].append(self.stepcount)

    def integrate_flash(self):
        """
        adjusts omega_current if flash occurs. Also sets self.flashed back to 0
        """

        # check if neighbors fired
        flashed = np.sum(self.flashed) >= 1
        if flashed:
            self.flashcount += 1

            flashed_neighbors = np.matmul(self.cm, self.flashed*1)
            flashed_neighbors[flashed_neighbors > 1] = 1

            if np.sum(flashed_neighbors) > 0:

                # adjust omegacurrent
                gPlus = np.sin(2 * np.pi * self.phases) / (2 * np.pi)
                gPlus[gPlus < 0] = 0
                
                gMin = np.sin(2 * np.pi * self.phases) / (2 * np.pi)
                gMin[gMin > 0] = 0
                gMin = -gMin
                omega_change = self.p.epsilon * (self.p.omega_common - self.omegas) \
                    + gPlus * self.phases * (self.p.omega_low - self.omegas) \
                    + gMin * self.phases * (self.p.omega_low - self.omegas) # TODO: change to omega High!
                # omega_change[flashed_neighbors] = 0 # TODO: we should take the oposite of this!
                self.omegas = self.omegas + omega_change

            # reset phase on flash
            self.phases[self.flashed] = 0
            self.timedeltas = self.p.time_delta / self.omegas

    def simulate(self, num_steps=None):

        if num_steps == None:
            num_steps = self.p.iterations

        for i in range(num_steps):
            self.step()

            if i % 100 == 0:
                print(
                    f"flashcount = {self.flashcount}, on step {self.stepcount}")

            self.stepcount += 1

        print('done')

    def plot_graph(self):
        # b=1
        fig = px.scatter(x=self.history['timestep'], y=self.history['firefly'])

        fig.update_traces(marker=dict(size=3,
                                      line=dict(width=0,
                                                color='DarkSlateGrey')),
                          selector=dict(mode='markers'))
        fig.show()
        print('done')


f = Fireflies(Params)
f.simulate(20000)
f.plot_graph()
