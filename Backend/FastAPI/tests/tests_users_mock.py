import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
try:
    from main import app
except ModuleNotFoundError:
    from Backend.FastAPI.main import app

"""
🧠 Qué estamos logrando
        Antes                   -   Ahora
        Usa Mongo real	        -   Simulado
        Depende de datos reales -   100% aislado
        Puede fallar por DB	    -   Solo prueba lógica
        Es integración	        -   Es unit test real
"""

class TestUsersMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    """
    @patch: reemplazá temporalmente esos objetos reales por mocks durante este test.
        1- Busca ese objeto en esa ruta exacta
        2- Lo reemplaza por un MagicMock
        3- Ejecuta el test
        4- Al terminar, lo devuelve a su estado original
    Es temporal y solo vive dentro del test.
    """
    @patch("Backend.FastAPI.routers.dataBase.users_db.db_client")
    @patch("Backend.FastAPI.routers.dataBase.users_db.search_user")
    def test_create_user(self, mock_search_user, mock_db_client):
        #mock_search_user y mock_db_client: son instancias de MagicMock
        #Python hace esto detrás de escena:
        #    -Crea un MagicMock para search_user
        #    -Crea un MagicMock para db_client
        #    -Reemplaza los objetos reales por esos mocks
        #    -Te los pasa como parámetros a la función
        #    -Ejecuta el test
        #    -Restaura los originales al terminar
    
        # Simular que no existe usuario
        mock_search_user.return_value = None

        #Simular insert_one
        mock_insert = MagicMock()
        mock_insert.inserted_id = "mock_id"
        mock_db_client.users.insert_one.return_value = mock_insert

        # Simular find_one luego del insert
        mock_db_client.users.find_one.return_value = {
            "_id": "mock_id",
            "uuid": "1234",
            "dni": 30998221,
            "username": "haas1234",
            "saldo": 20000.0
        }

        response = self.client.post("/user/new-user", json={
            "dni": 30998221,
            "username": "haas1234"
        })

        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIn("uuid", data)
        self.assertEqual(data["dni"], 30998221)
        self.assertEqual(data["saldo"], 20000.0)

        """
        Verifican que esas funciones hayan sido llamadas exactamente una vez durante el test.
            assert_called_once(): este mock debe haber sido ejecutado una sola vez. Si no se cumple, el test falla.
            Entonces el flujo correcto es:
                1- Se llama a search_user
                2- Se llama a insert_one
                3- Se llama a find_one
            Con esas asserts estás diciendo:
                ✔ Se verificó si el usuario existe
                ✔ Se insertó en la DB
                ✔ Se buscó el usuario recién creado
        
        👉 Testing de comportamiento: tests unitarios no solo prueban resultado, también prueba comportamiento.
                -Que se ejecutó la lógica esperada
                -Que no se saltearon pasos
                -Que no hubo llamadas duplicadas
                -Que no hubo llamadas innecesarias
        """
        mock_search_user.assert_called_once()
        mock_db_client.users.insert_one.assert_called_once()
        mock_db_client.users.find_one.assert_called_once()

    @patch("Backend.FastAPI.routers.dataBase.users_db.search_user")
    def test_user_exist(self, mock_search_user):
        mock_search_user.return_value = {
            "dni": 28773990
        }

        response = self.client.post("/user/new-user", json={
            "dni": 28773990,
            "username": "cadillac1234",
            "saldo": 20000.0
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Usuario ya existe")
        
        mock_search_user.assert_called_once()
        
    @patch("Backend.FastAPI.routers.dataBase.users_db.search_user")
    def test_get_user_success(self, mock_search_user):
        mock_search_user.return_value = {
            "uuid": "q1234",
            "dni": 25665009,
            "username": "williams1234",
            "saldo": 20000.0
        }

        response = self.client.get("/user/info-user?dni=25665009")

        self.assertEqual(response.status_code, 200)
        
        data = response.json()

        self.assertEqual(data["dni"], 25665009)
        self.assertEqual(data["saldo"], 20000.0)

        #Valida La función fue llamada exactamente una vez con esos parámetros
        mock_search_user.assert_called_once_with("dni", 25665009)
        
    @patch("Backend.FastAPI.routers.dataBase.users_db.search_user")
    def test_get_user_not_found(self, mock_search_user):
        mock_search_user.return_value = None

        response = self.client.get("/user/info-user?dni=32554992")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Usuario no encontrado")

        mock_search_user.assert_called_once_with("dni", 32554992)


class TestBlackjackV2Mock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas
        partidas.clear()

    @patch("Backend.FastAPI.routers.blackjack.blackjack_v2.search_uuid")
    @patch("Backend.FastAPI.routers.blackjack.blackjack_v2.search_user")
    def test_new_game_success(self, mock_search_user, mock_search_uuid):
        mock_search_user.return_value = {"dni": 34556332, "username": "testuser"}
        mock_search_uuid.return_value = "user123"

        response = self.client.post("/v2/blackjack/new-game?dni=34556332")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user_id"], "user123")
        self.assertEqual(data["mensaje"], "Partida creada")

        mock_search_user.assert_called_once_with("dni", 34556332)
        mock_search_uuid.assert_called_once_with(34556332)

    @patch("Backend.FastAPI.routers.blackjack.blackjack_v2.search_user")
    def test_new_game_user_not_found(self, mock_search_user):
        mock_search_user.return_value = None

        response = self.client.post("/v2/blackjack/new-game?dni=99999999")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Usuario no existe")

        mock_search_user.assert_called_once_with("dni", 99999999)

    def test_hit_success(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user1"] = {
            "jugador": [{"valor": "4", "palo": "Picas", "puntos": 4}, {"valor": "K", "palo": "Diamantes", "puntos": 10}],
            "mazo": [{"valor": "5", "palo": "Tréboles", "puntos": 5}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["puntos"], 19)
        self.assertEqual(len(data["carta"]), 3)
        self.assertEqual(len(data["mazo"]), 0)

    def test_hit_game_not_found(self):
        response = self.client.post("/v2/blackjack/hit/usuario_inexistente")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Partida no encontrada")

    def test_hit_at_21(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user2"] = {
            "jugador": [{"valor": "A", "palo": "Corazones", "puntos": 11}, {"valor": "K", "palo": "Diamantes", "puntos": 10}],
            "mazo": [{"valor": "5", "palo": "Tréboles", "puntos": 5}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user2")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["mensaje"], "No se puede solicitar más cartas")

    def test_hit_bust(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user3"] = {
            "jugador": [{"valor": "6", "palo": "Corazones", "puntos": 6}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "mazo": [{"valor": "8", "palo": "Tréboles", "puntos": 8}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/hit/user3")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["mensaje"], "Jugador se pasó")
        self.assertTrue(data["puntos"] > 21)

    def test_stand_success(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user4"] = {
            "jugador": [{"valor": "9", "palo": "Corazones", "puntos": 9}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "crupier": [{"valor": "2", "palo": "Diamantes", "puntos": 2}, {"valor": "5", "palo": "Picas", "puntos": 5}],
            "mazo": [{"valor": "J", "palo": "Tréboles", "puntos": 10}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user4")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Jugador gana")
        self.assertIn("jugador", data)
        self.assertIn("crupier", data)

    def test_stand_game_not_found(self):
        response = self.client.post("/v2/blackjack/stand/usuario_inexistente")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Partida no encontrada")

    def test_stand_already_bust(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user5"] = {
            "jugador": [{"valor": "6", "palo": "Corazones", "puntos": 6}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "mazo": [{"valor": "8", "palo": "Tréboles", "puntos": 8}],
            "estado": "bust"
        }

        response = self.client.post("/v2/blackjack/stand/user5")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["mensaje"], "Jugador se pasó")

    def test_stand_dealer_wins(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user6"] = {
            "jugador": [{"valor": "5", "palo": "Corazones", "puntos": 5}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "crupier": [{"valor": "5", "palo": "Diamantes", "puntos": 5}, {"valor": "8", "palo": "Picas", "puntos": 8}],
            "mazo": [{"valor": "7", "palo": "Tréboles", "puntos": 7}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user6")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Crupier gana")

    def test_stand_tie(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user7"] = {
            "jugador": [{"valor": "9", "palo": "Corazones", "puntos": 9}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "crupier": [{"valor": "9", "palo": "Diamantes", "puntos": 9}, {"valor": "Q", "palo": "Picas", "puntos": 10}],
            "mazo": [],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user7")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Empate")

    def test_stand_dealer_busts(self):
        try:
            from Backend.FastAPI.routers.blackjack.blackjack_v2 import partidas
        except ModuleNotFoundError:
            from routers.blackjack.blackjack_v2 import partidas

        partidas["user8"] = {
            "jugador": [{"valor": "9", "palo": "Corazones", "puntos": 9}, {"valor": "Q", "palo": "Diamantes", "puntos": 10}],
            "crupier": [{"valor": "Q", "palo": "Diamantes", "puntos": 10}, {"valor": "6", "palo": "Picas", "puntos": 6}],
            "mazo": [{"valor": "8", "palo": "Tréboles", "puntos": 8}],
            "estado": "jugando"
        }

        response = self.client.post("/v2/blackjack/stand/user8")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["resultado"], "Jugador gana")