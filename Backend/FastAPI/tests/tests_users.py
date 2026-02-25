import unittest
from fastapi.testclient import TestClient
"""
Importa una herramienta de FastAPI.
TestClient simula peticiones HTTP sin levantar un servidor real.
Permite hacer .get(), .post(), .put() como si fuera un cliente real.
"""
from main import app
"""
Importa una herramienta de FastAPI.
TestClient simula peticiones HTTP sin levantar un servidor real.
Permite hacer .get(), .post(), .put() como si fuera un cliente real.
"""

"""
🔹 ¿Qué está pasando internamente?
    1-TestClient crea una app en memoria.
    2-Hace peticiones HTTP simuladas.
    3-Ejecuta tu lógica real.
    4-Verifica que el resultado sea el esperado.
    5-Si algo no coincide → test falla.
"""

"""
✅ Ejecutar Tests
    Todos los tests: python -m unittest discover -s tests -v
    Un archivo específico: python -m unittest tests/tests_users.py -v
    Un método específico: python -m unittest tests.tests_users.TestUsers.test_create_user -v
"""

class TestUsers(unittest.TestCase):

    """
    @classmethod indica que es un método de clase.
    Se ejecuta una sola vez antes de todos los tests.
    cls representa la clase (no una instancia).
    """
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        """
        Crea el cliente de prueba.
        Lo guarda en la clase como atributo.
        Así todos los tests pueden usar self.client.
        Esto evita crear el cliente en cada test.
        """
    
    def test_create_user(self):
        """self: es una referencia al objeto actual."""
        response = self.client.post("/user/new-user", json={
            "dni": 34556332,
            "username": "ferrari1234"
        })

        self.assertEqual(response.status_code, 201)

        data = response.json()
        """Verifica que la clave "uuid" exista en la respuesta."""
        self.assertIn("uuid", data)
        """Verifica que el DNI devuelto sea el correcto."""
        self.assertEqual(data["dni"], 34556332)
        """Verifica que el saldo inicial sea 20000."""
        self.assertEqual(data["saldo"], 20000.0)

    def test_user_exist(self):
        self.client.post("/user/new-user", json={
            "dni": 28773990,
            "username": "redbull1234"
        })

        response = self.client.post("/user/new-user", json={
            "dni": 28773990,
            "username": "audi1234"
        })

        self.assertEqual(response.status_code, 400)
        
    def test_get_user_success(self):
        response = self.client.get("/user/info-user?dni=34556332")

        self.assertEqual(response.status_code, 200)
        
        data = response.json()

        self.assertEqual(data["dni"], 34556332)
        self.assertEqual(data["saldo"], 20000.0)
        
    def test_get_user_not_found(self):
        response = self.client.get("/user/info-user?dni=34556334")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Usuario no encontrado")
                