# SmartAstronaut - Proyecto IA

Sistema completo con backend FastAPI y frontend React para resolver problemas de busqueda inteligente.

> Este proyecto simula un astronauta autonomo navegando en una cuadricula marciana de 10x10 para recolectar muestras cientificas usando algoritmos de busqueda inteligente. El entorno incluye obstaculos naturales, costos variables de terreno (rocoso y volcanico), y una nave auxiliar de combustible limitado que reduce temporalmente el costo de movimiento.

## Estructura del Proyecto

```
smart-astronaut-ia/
├── smart_backend/          # Backend con FastAPI
│   ├── app.py             # Punto de entrada de la API
│   ├── core/              # Lógica del núcleo
│   │   ├── map_loader.py  # Cargador de mapas
│   │   └── executor.py    # Ejecutor de algoritmos
│   ├── algorithms/        # Algoritmos de búsqueda
│   ├── requirements.txt   # Dependencias Python
│   └── Dockerfile         # Imagen Docker del backend
│
├── smart_frontend/        # Frontend con React + Vite
│   ├── src/              # Código fuente
│   │   ├── App.jsx       # Componente principal
│   │   └── App.css       # Estilos
│   ├── package.json      # Dependencias Node
│   └── Dockerfile        # Imagen Docker del frontend
│
├── docker-compose.yml    # Orquestación de servicios
└── README.md            # Este archivo
```

## Tecnologias

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Python 3.11** - Lenguaje de programación
- **Uvicorn** - Servidor ASGI
- **Puerto:** 8000

### Frontend
- **React** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **Axios** - Cliente HTTP
- **Node 20** - Runtime de JavaScript
- **Puerto:** 5173

## Inicio Rapido

### Opción 1: Con Docker (Recomendado)

```bash
# Levantar todos los servicios
docker-compose up --build

# Para correr en segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Opción 2: Desarrollo Local

#### Backend
```bash
cd smart_backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd smart_frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

## Acceso a los Servicios

Una vez levantados los servicios, podrás acceder a:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Backend Docs:** http://localhost:8000/docs (Swagger UI automático)
- **Backend Health:** http://localhost:8000/health

## API Endpoints

### Backend (FastAPI)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Estado de salud del servicio |

## Comandos Docker Utiles

```bash
# Ver contenedores en ejecución
docker ps

# Ver logs de un servicio específico
docker-compose logs smart_backend
docker-compose logs smart_frontend

# Reconstruir un servicio específico
docker-compose up -d --build smart_backend

# Limpiar todo (contenedores, redes, volúmenes)
docker-compose down -v

# Ejecutar comando dentro del contenedor
docker-compose exec smart_backend bash
docker-compose exec smart_frontend sh
```

## Desarrollo

### Agregar Dependencias

#### Backend (Python)
```bash
# Activar entorno virtual
cd smart_backend
source venv/bin/activate

# Instalar nueva dependencia
pip install <paquete>

# Actualizar requirements.txt
pip freeze > requirements.txt
```

#### Frontend (Node)
```bash
cd smart_frontend

# Instalar nueva dependencia
npm install <paquete>

# Instalar dependencia de desarrollo
npm install -D <paquete>
```

### Variables de Entorno

#### Frontend
Puedes crear un archivo `.env` en `smart_frontend/`:
```env
VITE_BACKEND_URL=http://localhost:8000
```

## Proximos Pasos

1. **Implementar algoritmos de búsqueda** en `smart_backend/algorithms/`
2. **Crear interfaz de usuario** para visualizar mapas y soluciones
3. **Agregar endpoints** para ejecutar algoritmos
4. **Implementar visualización** de recorridos y estados

## Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto.

## Autor

**Ivan Ausecha**

---

**Happy Coding!**
