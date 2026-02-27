import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

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
    @patch("routers.dataBase.users_db.db_client")
    @patch("routers.dataBase.users_db.search_user")
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

    @patch("routers.dataBase.users_db.search_user")
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
        
    @patch("routers.dataBase.users_db.search_user")
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
        
    @patch("routers.dataBase.users_db.search_user")
    def test_get_user_not_found(self, mock_search_user):
        mock_search_user.return_value = None

        response = self.client.get("/user/info-user?dni=32554992")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Usuario no encontrado")

        mock_search_user.assert_called_once_with("dni", 32554992)
                