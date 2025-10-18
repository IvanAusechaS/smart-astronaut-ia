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

## Despliegue en Producción

### 🚀 URLs de Producción

- **Frontend (Vercel):** https://smart-astronaut.vercel.app
- **Backend (Render):** https://smart-astronaut-backend.onrender.com
- **Backend Docs:** https://smart-astronaut-backend.onrender.com/docs

### Configuración de CI/CD

El proyecto utiliza GitHub Actions para despliegue automatizado al hacer push o pull request en la rama `main`.

#### Variables de Entorno Requeridas en GitHub Secrets

Para que el despliegue automatizado funcione, necesitas configurar los siguientes secrets en tu repositorio de GitHub:

1. **RENDER_API_KEY** - Token de autenticación de Render
   - Obtenerlo en: [Render Dashboard → Account Settings → API Keys](https://dashboard.render.com/u/settings)
   
2. **RENDER_SERVICE_ID** - ID del servicio en Render
   - Encontrarlo en la URL del servicio: `https://dashboard.render.com/web/srv-XXXXXXXXXXXXXXXX`
   - El ID es la parte después de `srv-`
   
3. **VERCEL_TOKEN** - Token de autenticación de Vercel
   - Crear en: [Vercel Dashboard → Account Settings → Tokens](https://vercel.com/account/tokens)
   
4. **VERCEL_ORG_ID** - ID de tu organización/cuenta de Vercel
   - Ejecutar en la raíz del proyecto: `vercel link`
   - El ID se guarda en `.vercel/project.json`
   
5. **VERCEL_PROJECT_ID** - ID del proyecto en Vercel
   - También disponible después de ejecutar `vercel link`
   - Se guarda en `.vercel/project.json`

#### Cómo Configurar los Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Click en **Settings** → **Secrets and variables** → **Actions**
3. Click en **New repository secret**
4. Agrega cada uno de los 5 secrets mencionados arriba

### Configuración Manual de Despliegue

#### Backend en Render

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente el archivo `render.yaml`
4. El servicio se desplegará usando Docker desde `smart_backend/Dockerfile`
5. Variables de entorno configuradas automáticamente:
   - `PYTHONUNBUFFERED=1`
   - `PORT=8000`
   - `CORS_ORIGINS=https://smart-astronaut.vercel.app,https://smart-astronaut-*.vercel.app`

#### Frontend en Vercel

1. Crea una cuenta en [Vercel](https://vercel.com)
2. Importa tu repositorio de GitHub
3. Vercel detectará automáticamente el archivo `vercel.json`
4. Configuración automática:
   - Build command: `cd smart_frontend && npm install && npm run build`
   - Output directory: `smart_frontend/dist`
   - Variable de entorno: `VITE_BACKEND_URL=https://smart-astronaut-backend.onrender.com`

### Flujo de CI/CD

Cuando haces push a la rama `main`:

1. **Test Job** - Ejecuta las pruebas del backend con pytest
2. **Deploy Backend** - Si las pruebas pasan, despliega en Render
3. **Deploy Frontend** - Si las pruebas pasan, despliega en Vercel

Los pull requests solo ejecutan las pruebas sin desplegar.

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
