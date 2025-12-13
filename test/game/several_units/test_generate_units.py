import unittest

from logic.game.several_units_game.generate_units.generate_units import generate_units
from logic.game.chasing_game.chasing_game import ChasingGame
from logic.game.comp_chasing_game.comp_chasing_game import CompChasingGame
from logic.game.several_units_game.generate_units.unit_generation_data import UnitGenerationData
from logic.game.share.unit_type import UnitType


class TestGenerateUnits(unittest.TestCase):

    def test_generate_units(self):
        game = ChasingGame(None)

        blue_generation_data = UnitGenerationData(units_number=3)
        red_generation_data = UnitGenerationData(units_number=3)

        result = generate_units(game, blue_generation_data=blue_generation_data, red_generation_data=red_generation_data)

    def test_generate_units1(self):
        game = CompChasingGame(None, 7, 7, 0., 0., 0.)
        blue_generation_data = UnitGenerationData(units_number=3)
        red_generation_data = UnitGenerationData(units_number=3)
        result = generate_units(game, blue_generation_data=blue_generation_data, red_generation_data=red_generation_data)

    def test_generate_units2(self):
        game = ChasingGame(None)

        unit_probs = [0.4] + [0.6 / (len(UnitType) - 1)] * (len(UnitType) - 1)
        unit_type_probs = {unit_type: prob for unit_type, prob in zip(UnitType, unit_probs)}

        blue_generation_data = UnitGenerationData(units_number=15,
            unit_type_probs=unit_type_probs)
        red_generation_data = UnitGenerationData(units_number=3)

        result = generate_units(game, blue_generation_data=blue_generation_data, red_generation_data=red_generation_data)
