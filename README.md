# Tutor IA para Formación Profesional

Sistema RAG (Retrieval-Augmented Generation) desarrollado en Python para asistir al alumnado de Formación Profesional respondiendo preguntas únicamente a partir de la documentación proporcionada por el profesorado.

Actualmente utiliza ChromaDB como base de datos vectorial y Ollama para la ejecución local del modelo de lenguaje. La arquitectura está preparada para utilizar Gemini en producción.

---

# Características

- Gestión de documentos desde la interfaz web.
- Conversión automática de PDF a Markdown mediante Docling.
- Limpieza del texto generado por OCR.
- División automática en chunks.
- Generación de embeddings con Sentence Transformers.
- Almacenamiento vectorial mediante ChromaDB.
- Recuperación semántica mediante RAG.
- Construcción automática del prompt.
- Generación de respuestas mediante Ollama (Gemma 3).
- Arquitectura modular preparada para sustituir componentes (LLM, base vectorial, etc.).

---

# Arquitectura

```
PDF
 │
 ▼
Docling
 │
 ▼
Markdown
 │
 ▼
Limpieza
 │
 ▼
Chunker
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Retriever
 │
 ▼
Prompt Builder
 │
 ▼
LLM
 │
 ▼
Respuesta
```

---

# Estructura del proyecto

```
Proyecto-IA-FP/

├── data/
│   ├── markdown_raw/
│   ├── markdown_clean/
│   └── vector_store/
│
├── documents/
│
├── src/
│   ├── core/
│   ├── ingestion/
│   ├── rag/
│   └── llm/
│
├── tests/
│
├── web/
│
├── requirements.txt
└── README.md
```

---

# Instalación

## 1. Clonar el proyecto

```bash
git clone ...
```

## 2. Crear entorno virtual

```bash
python -m venv .venv
```

Activarlo.

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Instalación de Ollama

Instalar Ollama desde:

https://ollama.com

Descargar el modelo:

```bash
ollama pull gemma3:4b
```

Comprobar que funciona:

```bash
ollama run gemma3:4b
```

---

# Funcionamiento interno

El sistema sigue una arquitectura RAG (Retrieval-Augmented Generation):

1. Los documentos PDF se convierten a Markdown.
2. El texto se limpia automáticamente.
3. Se divide en chunks.
4. Cada chunk se transforma en un embedding.
5. Los embeddings se almacenan en ChromaDB.
6. Cuando el usuario realiza una pregunta:
   - se genera el embedding de la consulta;
   - se recuperan los chunks más similares;
   - se construye un prompt con ese contexto;
   - el LLM genera la respuesta utilizando únicamente la información recuperada.

# Flujo de indexación

Para generar la base vectorial:

1. Convertir PDFs.
2. Limpiar Markdown.
3. Crear chunks.
4. Generar embeddings.
5. Indexar en ChromaDB.

---

# Ejecución

Iniciar la aplicación web:

```bash
python run.py
```

o

```bash
flask --app web.app run
```

---

# Tecnologías utilizadas

- Python
- Flask
- Docling
- Sentence Transformers
- ChromaDB
- Ollama
- Gemma 3
- NumPy

---

# Próximas mejoras

- Integración con Gemini.
- Reranking de resultados.
- Historial de conversaciones.
- Evaluación automática de respuestas.

---

# Licencia

Proyecto desarrollado con fines educativos.
