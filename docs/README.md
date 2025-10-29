# Documentos anteriores de Gantt

Este directorio contenía artefactos de Gantt solo para apoyo temporal. Fueron deshabilitados a petición del usuario.

- gantt_proyecto.html: deshabilitado
- gantt_tareas.csv: deshabilitado

# Documentación de Planificación

Este directorio contiene artefactos de planificación para la Evaluación Sumativa (Unidad 2):

- `gantt_proyecto.html`: Diagrama de Gantt interactivo (Mermaid.js). Ábrelo en tu navegador.
- `gantt_tareas.csv`: Versión tabular para Excel/Google Sheets o importación en herramientas de Gantt/Kanban.

## Cómo ver el Gantt

1. Haz doble clic en `docs/gantt_proyecto.html` para abrirlo en tu navegador (requiere conexión a Internet para cargar Mermaid desde CDN).
2. Alternativa VS Code: instala una extensión de Mermaid Preview y usa un `.md` si prefieres (podemos generar uno a pedido).

## Cómo usar el CSV en Excel

1. Abre `gantt_tareas.csv` en Excel.
2. Inserta un diagrama de Gantt rápido:
   - Crea una columna "Inicio" y otra "Duración" (ya están) y usa un gráfico de barras apiladas.
   - Formatea la primera serie (Inicio) como transparente para lograr el efecto Gantt.

## Propietarios / Responsables

- Valentina Pérez — PM/BA
- Diego Henríquez — Backend
- Gabriel Ruiz — Frontend
- Camila Torres — QA

Ajusta nombres y fechas según tu realidad del equipo. Si quieres, puedo generar versiones separadas por sprint o exportables desde Trello (JSON ➜ CSV/Markdown).