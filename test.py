import unittest
import main
from main import Fireflies, Params




class test_vectormath(unittest.TestCase):


    def setUp(self) -> None:
        self.fireflies = Fireflies(Params)

    def test_timechange(self):
        
        phase1 = self.fireflies.phases.copy()
        # self.fireflies.step()
        self.fireflies.simulate(num_steps=2000)
        phase2 = self.fireflies.phases
        self.assertIsNot(phase1, phase2)

    def test_phase_reset(self):

        self.fireflies.simulate(num_steps=2000)
        self.assertTrue(max(self.fireflies.phases) < 2)

unittest.main()