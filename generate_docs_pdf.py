from fpdf import FPDF


class BlackjackDocs(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, "Blackjack Python - Documentacion de Arquitectura", align="R")
            self.ln(5)
            self.set_draw_color(200, 200, 200)
            self.line(10, 15, 200, 15)
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")


pdf = BlackjackDocs()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

pdf.add_page()

pdf.set_font("Helvetica", "B", 24)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 20, "Blackjack Python", align="C", ln=True)

pdf.set_font("Helvetica", "I", 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Documentacion de Proyecto y Arquitectura", align="C", ln=True)
pdf.ln(10)

pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "API REST de Juego Blackjack con FastAPI y MongoDB", align="C", ln=True)
pdf.ln(15)

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "1. Descripcion del Proyecto", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)
descripcion = (
    "Blackjack Python es un proyecto de aprendizaje desarrollado por Brais Moure "
    "(@mouredev) en Twitch. Implementa una API REST completa para el juego de "
    "Blackjack (21) utilizando FastAPI como framework web y MongoDB como base de datos.\n\n"
    "El proyecto demuestra conceptos de arquitectura por capas, patrones de diseno "
    "modernos en Python, y buenas practicas de desarrollo de APIs REST."
)
pdf.multi_cell(0, 6, descripcion)
pdf.ln(5)

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "2. Caracteristicas Principales", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

features = [
    ("Gestion de Usuarios", "Crear usuarios con DNI y nombre de usuario"),
    ("Sistema de Apuestas", "Saldo inicial de 20.000 para apuestas"),
    ("Dos Versiones de API", "v1 (en memoria) y v2 (por usuario con BD)"),
    ("Logica de Juego", "Repartir, Hit, Stand con calculo de puntos"),
    ("Manejo de Asas", "Los Asas valen 11 o 1 segun convenga"),
    ("Tests Unitarios", "Suite completa de tests con unittest"),
]

for title, desc in features:
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 6, f"* {title}:", ln=False)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, desc, ln=True)

pdf.add_page()

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "3. Stack Tecnologico", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

stack = [
    ("Lenguaje", "Python 3.10+"),
    ("Framework", "FastAPI"),
    ("Base de Datos", "MongoDB"),
    ("Driver BD", "PyMongo"),
    ("Validacion", "Pydantic"),
    ("Testing", "unittest + TestClient"),
    ("Deployment", "Vercel / Uvicorn"),
]

for tech, val in stack:
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 6, f"{tech}:", ln=False)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, val, ln=True)

pdf.ln(8)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "4. Estructura del Proyecto", ln=True)
pdf.set_font("Courier", "", 8)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

estructura = """blackjack-python/
+-- Backend/FastAPI/
|   +-- main.py              # Punto de entrada FastAPI
|   +-- requirements.txt    # Dependencias
|   +-- negocio/             # Capa de negocio
|   |   +-- models/          # Modelos Pydantic
|   |   +-- dto/            # Objetos de transferencia
|   +-- dataBase/           # Capa de datos
|   |   +-- client.py       # Cliente MongoDB
|   |   +-- schemas/        # Esquemas BD
|   +-- routers/            # Controladores API
|   |   +-- dataBase/users_db.py
|   |   +-- blackjack/
|   |       +-- blackjack_v1.py
|   |       +-- blackjack_v2.py
|   +-- tests/              # Tests unitarios
+-- collection - postman/   # Coleccion Postman
+-- Images/                 # Imagenes
+-- README.md
+-- Blackjack.txt          # Reglas del juego
+-- LICENSE"""

pdf.multi_cell(0, 5, estructura)
pdf.ln(5)

pdf.add_page()

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "5. Arquitectura por Capas", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

capas = [
    ("Routers (HTTP)", "Manejan las peticiones HTTP y responden al cliente"),
    ("Business Logic", "Contiene la logica de negocio (models, dto)"),
    ("Data Access", "Gestionan la comunicacion con MongoDB"),
]

for capa, desc in capas:
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 6, f"* {capa}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(10, 5, "", ln=False)
    pdf.multi_cell(0, 5, f"  {desc}")
    pdf.ln(2)

pdf.ln(5)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "6. Endpoints de la API", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

pdf.set_font("Helvetica", "B", 10)
pdf.cell(0, 6, "Usuarios:", ln=True)
pdf.set_font("Courier", "", 9)
endpoints_users = [
    "POST   /user/new-user        - Crear usuario",
    "GET    /user/info-user?dni=X - Obtener info",
]
for ep in endpoints_users:
    pdf.cell(10, 5, "", ln=False)
    pdf.cell(0, 5, ep, ln=True)

pdf.ln(3)
pdf.set_font("Helvetica", "B", 10)
pdf.cell(0, 6, "Blackjack v1 (en memoria):", ln=True)
pdf.set_font("Courier", "", 9)
endpoints_v1 = [
    "GET    /v1/blackjack/repartir         - Repartir cartas",
    "GET    /v1/blackjack/solicitar_carta  - Pedir carta",
    "GET    /v1/blackjack/plantarse        - Plantarse",
]
for ep in endpoints_v1:
    pdf.cell(10, 5, "", ln=False)
    pdf.cell(0, 5, ep, ln=True)

pdf.ln(3)
pdf.set_font("Helvetica", "B", 10)
pdf.cell(0, 6, "Blackjack v2 (por usuario):", ln=True)
pdf.set_font("Courier", "", 9)
endpoints_v2 = [
    "POST   /v2/blackjack/new-game?dni=X - Nueva partida",
    "POST   /v2/blackjack/hit/{user_id}  - Pedir carta",
    "POST   /v2/blackjack/stand/{user_id} - Plantarse",
]
for ep in endpoints_v2:
    pdf.cell(10, 5, "", ln=False)
    pdf.cell(0, 5, ep, ln=True)

pdf.add_page()

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "7. Patrones de Diseno", ln=True)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(0, 0, 0)
pdf.ln(2)

patrones = [
    ("Router Pattern", "Routers separados por dominio (usuarios, blackjack)"),
    ("Pydantic Models", "Validacion de datos con BaseModel"),
    ("Repository Pattern", "Esquemas separados para transformacion de datos"),
    ("Error Handling", "HTTPException con codigos de estado apropiados"),
    ("Convention Spanish", "Comentarios y mensajes en espanol"),
]

for patron, desc in patrones:
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, f"* {patron}: {desc}", ln=True)

pdf.ln(8)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(40, 60, 100)
pdf.cell(0, 10, "8. Ejecutar el Proyecto", ln=True)
pdf.set_font("Courier", "", 9)
pdf.set_text_color(0, 0, 0)

comandos = """# Instalar dependencias
pip install -r Backend/FastAPI/requirements.txt

# Ejecutar con uvicorn
cd Backend/FastAPI
uvicorn main:app --reload

# Ejecutar con fastapi CLI
cd Backend/FastAPI
fastapi dev main.py

# Ejecutar tests
python -m unittest discover -s Backend/FastAPI/tests -v"""

pdf.multi_cell(0, 5, comandos)

pdf.ln(10)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, "Proyecto creado por Brais Moure (@mouredev)", align="C", ln=True)
pdf.cell(0, 6, "Aprende Python desde cero con proyectos reales", align="C", ln=True)

pdf.output("Documentacion_Blackjack_Python.pdf")
print("PDF generado: Documentacion_Blackjack_Python.pdf")
