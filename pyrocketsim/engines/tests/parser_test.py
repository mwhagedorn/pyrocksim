from unittest import TestCase
from pyrocketsim.engines.engine_parser import EngineParser
import os

ENGINE_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/engines'))

class ParserTest(TestCase):


    def test_returns_correct_strategy_for_rse_file(self):
        parser = EngineParser("blah.rse")
        self.assertEqual(parser.strategy().__class__.__name__,"RSEParser")

    def test_returns_correct_strategy_for_eng_file(self):
        parser = EngineParser("blah.eng")
        self.assertEqual(parser.strategy().__class__.__name__,"ENGParser")

    def test_parser_returns_error_for_nonexistant_file(self):
        parser = EngineParser("blah.rse")
        self.assertFalse(parser.parse())

    def test_returns_object_from_rse_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.rse")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.code,"A8")
        self.assertEquals(engine.mfg,"Estes")
        self.assertEquals(str(engine.len),"70.0")
        self.assertEquals(str(engine.dia),"18.0")

    def test_interpolates_force_data(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.rse")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(getattr(engine,"burn_time"),0.73)
        self.assertAlmostEqual(9.000, engine.force_at(0.2),2)

    def test_returns_comment_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertIsNotNone(engine.comment)

    def test_returns_code_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.code,"A8")

    def test_returns_length_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.len,70.0)

    def test_returns_dia_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.dia,18.0)

    def test_returns_prop_weight_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.prop_weight,3.3)

    def test_returns_engine_weight_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.initial_weight,16.35)

    def test_returns_mfg_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(engine.mfg,'Estes')

    def test_returns_thrustdata_from_eng_file(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertEquals(len(engine.data_points),23)

    def test_interpolates_eng_force_data(self):
        path = os.path.join(ENGINE_DATA, "Estes_A8.eng")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertAlmostEqual(9.000, engine.force_at(0.2),2)


    def test_interpolates_large_engine_data(self):
        path = os.path.join(ENGINE_DATA, "AeroTech_J275.rse")
        parser = EngineParser(path)
        engine = parser.parse()
        self.assertAlmostEqual(9.000, engine.force_at(0.2),2)









