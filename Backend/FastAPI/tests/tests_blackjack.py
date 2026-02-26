import unittest
from fastapi.testclient import TestClient
from main import app
from routers.blackjack.blackjack_v2 import partidas

class TestBlackjackV2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_new_game(self):
        response = self.client.post("/v2/blackjack/new-game?dni=34556332")

        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json())

    def test_new_game_user_not_found(self):
        response = self.client.post("/v2/blackjack/new-game?dni=34556338")

        self.assertEqual(response.status_code, 400)

    def test_hit(self):
        """
        en mazo esta la carta que luego se asigna al jugador.
        mazo → saca una carta → se la da al jugador → recalcula puntos
        """
        partidas["user1"] = {
            "jugador": [{"valor": "4", "palo":"Picas", "puntos": 4}, {"valor": "K", "palo":"Diamantes", "puntos": 10}],
            "mazo": [{"valor": "5", "palo":"Tréboles", "puntos": 5}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["puntos"], 19)
        self.assertEqual(len(data["carta"]), 3)
                
    def test_hit_game_not_found(self):
        response = self.client.post("/hit/usuario_inexistente")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")

    def test_hit_21(self):
        partidas["user2"] = {
            "jugador": [{"valor": "A", "palo":"Corazones", "puntos": 11}, {"valor": "K", "palo":"Diamantes", "puntos": 10}],
            "mazo": [{"valor": "5", "palo":"Tréboles", "puntos": 5}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mensaje"], "No se puede solicitar más cartas")

    def test_hit_bust(self):
        partidas["user3"] = {
            "jugador": [{"valor": "6", "palo":"Corazones", "puntos": 6}, {"valor": "Q", "palo":"Diamantes", "puntos": 10}],
            "mazo": [{"valor": "8", "palo":"Tréboles", "puntos": 8}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user3")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mensaje"], "Jugador se pasó")
        self.assertTrue(response.json()["puntos"] > 21)

    def test_stand_not_found(self):
        response = self.client.post("/v2/blackjack/stand/usuario_inexistente")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Partida no encontrada")

    def test_stand_bust(self):
        partidas["user4"] = {
            "jugador": [{"valor": "6", "palo":"Corazones", "puntos": 6}, {"valor": "Q", "palo":"Diamantes", "puntos": 10}],
            "mazo": [{"valor": "8", "palo":"Tréboles", "puntos": 8}],
            "estado": "bust"
        }

        response = self.client.post("/v2/blackjack/stand/user4")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mensaje"], "Jugador se pasó")

    def test_stand_player_wins(self):
        partidas["user5"] = {
            "jugador": [{"valor": "9", "palo":"Corazones", "puntos": 9}, {"valor": "Q", "palo":"Diamantes", "puntos": 10}],
            "crupier": [{"valor": "2", "palo":"Diamantes", "puntos": 2}, {"valor": "5", "palo":"Picas", "puntos": 5}],
            "mazo": [{"valor": "J", "palo":"Tréboles", "puntos": 10}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resultado"], "Jugador gana")

    def test_stand_tie(self):
        partidas["user6"] = {
            "jugador": [{"valor": "9", "palo":"Corazones", "puntos": 9}, {"valor": "Q", "palo":"Diamantes", "puntos": 10}],
            "crupier": [{"valor": "9", "palo":"Diamantes", "puntos": 9}, {"valor": "Q", "palo":"Picas", "puntos": 10}],
            "mazo": [],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user6")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Empate")

    def test_stand_dealer_wins(self):
        partidas["user7"] = {
            "jugador": [{"valor": "5", "palo":"Corazones", "puntos": 5}, {"valor": "Q", "palo":"Diamantes", "puntos": 10}],
            "crupier": [{"valor": "5", "palo":"Diamantes", "puntos": 5}, {"valor": "8", "palo":"Picas", "puntos": 8}],
            "mazo": [{"valor": "7", "palo":"Tréboles", "puntos": 7}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user7")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Crupier gana")