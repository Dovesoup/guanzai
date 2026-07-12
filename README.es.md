# GuanZai · 观在

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

> 观而后动，众智自生。
> Observar a fondo. Actuar juntos. Evolucionar continuamente.

GuanZai es una capa pequeña y determinista de gobernanza y planificación para agentes de IA locales. Antes de añadir más mecanismos, plantea tres preguntas: ¿conviene que este trabajo siga en solo?, ¿compensa el coste de incorporar otro agente?, ¿y sus consecuencias exigen una auditoría independiente?

Está creado en el punto de encuentro entre los sistemas técnicos y el criterio humano. El objetivo no es reunir el equipo más grande posible, sino elegir con intención y dejar espacio suficiente para que las personas conserven el control.

> [!WARNING]
> **Alpha pública — `v0.3.0-alpha.1`.** GuanZai produce planes y comandos para adaptadores; todavía no es un ciclo de ejecución completo y desatendido. Revisa cada manifiesto y comando antes de usarlo. Las interfaces y los detalles de las políticas pueden cambiar.

## Qué ofrece esta versión

- Clasifica las tareas de forma determinista en planes `solo`, `single`, `team` o `audited`, este último con prioridad por motivos de seguridad.
- Hace visibles el valor de la orquestación, el impacto de la acción y la revisión independiente en un manifiesto JSON.
- Construye comandos explícitos de Codex CLI y WorkBuddy a partir de paquetes de tareas acotados.
- Detecta las capacidades locales de Codex CLI y WorkBuddy CLI con `guanzai doctor`.
- Evita confundir el trabajo mecánico en bloque con la complejidad cognitiva.
- Exige una auditoría independiente para tareas financieras destinadas a la toma de decisiones y cambios de consecuencias importantes que coincidan con la política actual.
- Incluye un Codex Skill instalable y 28 pruebas de políticas, enrutamiento, paquetes, CLI y capacidades.

Actualmente, GuanZai **no** inicia los comandos de los trabajadores generados, consulta su progreso, recopila resultados ni cierra automáticamente el ciclo plan–ejecución–auditoría. Que un manifiesto indique `"execution": "planned"` significa exactamente eso.

## Políticas predeterminadas

- WorkBuddy Hy3 / Hunyuan 3 (`hunyuan-3`) es la primera opción de bajo coste; DeepSeek V4 Pro (`deepseek-v4-pro`) es el siguiente nivel de WorkBuddy.
- Los comandos de WorkBuddy siempre usan un esfuerzo de razonamiento `high`.
- WorkBuddy GLM está bloqueado.
- Se prohíbe el modo Premium Fast/de alta velocidad; los elementos de trabajo generados usan la velocidad estándar.
- La selección de modelos de Codex solo está disponible cuando la Codex CLI local la admite. En caso contrario, los trabajadores de colaboración de Codex heredan la selección de modelos administrada por el host.
- Un requisito de auditoría puede prevalecer sobre el presupuesto de trabajadores solicitado, porque un presupuesto pequeño no debe eliminar silenciosamente una comprobación independiente.

Estos son los valores predeterminados del código actual, no afirmaciones universales sobre la calidad de los modelos.

## Instalación

GuanZai requiere Python 3.9 o posterior. Desde un clon:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

En Windows, usa `py` en lugar de `python3` y activa el entorno con `.venv\Scripts\activate`.

El paquete de Python solo instala la CLI `guanzai`. Para que Codex pueda usar el Skill incluido, instálalo por separado desde la raíz del repositorio:

```bash
mkdir -p ~/.codex/skills/guanzai
cp -R skill/guanzai/. ~/.codex/skills/guanzai/
```

Reinicia Codex después de instalar o actualizar el Skill. El Skill orienta a Codex sobre cuándo invocar GuanZai; no convierte los comandos de adaptadores planificados en un ciclo de ejecución automático.

## Inicio rápido

En el proyecto que quieras planificar:

```bash
guanzai init
guanzai doctor
guanzai plan "Research, design, implement, and verify a privacy-safe export" --json
```

`guanzai init` crea `.guanzai/config.toml` y un directorio de memoria local vacío. Se niega a sobrescribir una configuración existente.

Para solicitar un modo acotado:

```bash
guanzai plan "Rename these files using the existing pattern" --mode solo --json
guanzai plan "Implement the approved parser" --mode single --json
guanzai plan "Research, design, and verify the migration" --mode team --max-workers 3 --json
```

`audited` se elige mediante la política y no se ofrece como anulación desde la línea de comandos. Cuando la acción y su impacto lo exigen, GuanZai conserva al menos un ejecutor y un auditor.

## Modos

| Modo | Significado |
| --- | --- |
| `solo` | Mantiene la tarea en el orquestador; no crea ningún elemento de trabajo. |
| `single` | Crea un elemento de trabajo acotado. |
| `team` | Crea roles complementarios cuando la amplitud o la verificación lo justifican. |
| `audited` | Conserva un auditor independiente para trabajos de consecuencias importantes que coincidan con la política, y prevalece sobre un presupuesto inseguro. |

Todo el enrutamiento es determinista y se basa en la política textual actual. Se puede explicar y probar, pero no constituye comprensión semántica: una redacción inusual, otros idiomas o la falta de contexto pueden producir un plan equivocado.

## Límite de capacidades

`guanzai doctor` informa de lo que puede exponer el host local. El enrutador siempre puede crear un plan, pero disponibilidad no significa ejecución:

- La generación de comandos de Codex CLI admite ajustes de modelo y razonamiento por comando cuando existe un ejecutable `codex` local.
- La interfaz actual de colaboración de Codex no permite seleccionar un modelo por subagente; esos trabajadores siguen administrados por el host.
- El descubrimiento de WorkBuddy busca `codebuddy` en `PATH` y, después, en la ruta estándar de su paquete de aplicación para macOS.
- Generar un comando de WorkBuddy no demuestra que WorkBuddy esté instalado o autenticado, ni que el modelo indicado esté disponible.

Nunca trates una recomendación o un comando generado como prueba de que un modelo se ejecutó.

## Privacidad y seguridad

El repositorio de GuanZai no contiene un almacén de credenciales ni un servicio en la nube. La configuración del proyecto y la memoria futura residen en `.guanzai/`. El archivo `.gitignore` del repositorio excluye todo el directorio `.guanzai/`; conserva esa regla cuando uses GuanZai en otros lugares y no fuerces la inclusión del estado local. Los paquetes de tareas generados pueden contener el texto de la tarea que proporciones; revísalos antes de entregarlos a cualquier agente o proveedor externo.

Lee [Privacidad](docs/PRIVACY.md) para conocer el límite de los datos y [Seguridad](SECURITY.md) antes de usar la Alpha con trabajo sensible. Informa de las vulnerabilidades mediante el sistema privado de GitHub, no mediante una incidencia pública.

## Arquitectura

El recorrido actual es breve de manera deliberada:

```text
task text -> deterministic value/risk gate -> role and model plan
          -> planned manifest -> optional adapter command construction
```

Consulta [Arquitectura](docs/ARCHITECTURE.md) para conocer las invariantes, los componentes y los límites de confianza.

## Hoja de ruta

- Un registro de ejecución duradero que conserve los estados planned, started, completed y failed.
- Ejecución opcional, consulta de estado, cancelación, resultados normalizados y puntos explícitos de aprobación humana.
- Calibración de capacidades a partir de resultados observados, no solo de preferencias estáticas.
- Adaptadores adicionales de proveedores mediante contratos estables, incluidas rutas compatibles con ACP/MCP.
- Políticas de enrutamiento versionadas, evaluación multilingüe de políticas y reversión segura.
- Una separación más sólida entre el conocimiento semilla público y la memoria privada del proyecto.

Los elementos de la hoja de ruta son intenciones, no capacidades ya publicadas.

## Desarrollo

```bash
python3 -m unittest discover -s tests -v
```

En Windows, el comando equivalente es `py -m unittest discover -s tests -v`.

La suite actual contiene 28 pruebas. Consulta [Contribuir](CONTRIBUTING.md), el [Código de conducta](CODE_OF_CONDUCT.md) y el [Registro de cambios](CHANGELOG.md).

## Trabajo independiente y antecedentes

GuanZai es un proyecto independiente, no una bifurcación de Superpowers, CC Switch, MCO/Hive, LiteLLM ni RouteLLM. No se ha copiado código fuente de esos proyectos en esta versión. Sus ideas y el trabajo de sus ecosistemas ayudaron a aclarar los límites en torno a los flujos de trabajo, los planos de control de configuración, la ejecución con varias CLI, las pasarelas, los presupuestos y la investigación sobre enrutamiento.

Consulta [Antecedentes](PRIOR_ART.md) y el [Aviso de terceros](THIRD_PARTY.md) para ver los reconocimientos precisos. Si en el futuro se copia o modifica código fuente de terceros, deberán conservarse con él sus licencias y avisos de derechos de autor.

## Licencia

[MIT](LICENSE) © 2026 Dovesoup.
