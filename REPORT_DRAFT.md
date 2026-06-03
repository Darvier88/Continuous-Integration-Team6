# Reporte de práctica — Integración Continua

## Portada

**Materia:** Software Engineering II  
**Tema:** Continuous Integration  
**Proyecto:** CaféLibro — Library Loan Manager  
**Repositorio:** [pegar URL del repositorio público]  
**Integrantes:** [pegar nombres]

## Introducción

En esta práctica se implementó una aplicación de línea de comandos llamada CaféLibro, cuyo objetivo es administrar los préstamos de una biblioteca pequeña. El sistema permite registrar libros y miembros, prestar libros, devolverlos, consultar los préstamos de un miembro y reportar préstamos vencidos. Además, el equipo configuró una tubería de integración continua para ejecutar automáticamente las pruebas en cada push y en cada pull request hacia la rama principal.

La integración continua ayuda a que el equipo trabaje en paralelo sin romper la rama principal. Cada cambio se desarrolla en una rama separada, se prueba automáticamente en GitHub Actions y solo se integra a `main` después de pasar las pruebas y recibir revisión de otro integrante.

## Desarrollo

### Repositorio y features

Repositorio: [pegar URL]

| Integrante | Feature desarrollada | Pull Request abierto | Pull Request revisado |
|---|---|---|---|
| Integrante 1 | Registrar miembro | [link] | [link] |
| Integrante 2 | Prestar libro | [link] | [link] |
| Integrante 3 | Devolver libro | [link] | [link] |
| Integrante 4 | Listar préstamos de un miembro | [link] | [link] |
| Integrante 5 | Reportar préstamos vencidos | [link] | [link] |
| Integrante 6 | Registrar libro | [link] | [link] |

### Aplicación construida

La aplicación usa Python y almacena el estado en un archivo JSON. El archivo contiene tres colecciones principales:

- `books`: libros registrados con código único y título.
- `members`: miembros registrados con identificador único y nombre.
- `loans`: préstamos activos con código de libro, identificador del miembro y fecha de vencimiento.

Reglas implementadas:

- Un libro no puede prestarse si ya está prestado.
- Un miembro no puede tener más de tres libros prestados al mismo tiempo.
- No se puede prestar un libro inexistente.
- No se puede prestar a un miembro inexistente.
- No se puede devolver un libro que no está prestado.
- Las fechas se manejan en formato `YYYY-MM-DD`.

### Workflow de integración continua

Archivo: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
          pip install -e .
      - name: Run tests
        run: pytest -q
```

Captura requerida: pegar una captura del workflow pasando en la pestaña Actions.

### Protección de la rama principal

Se configuró la rama `main` para exigir que el workflow de CI pase antes de permitir el merge. Además, se requiere al menos una aprobación de otro integrante. Esto evita que se integren cambios sin revisión o con pruebas fallidas.

Captura requerida: pegar captura de `Settings > Branches` mostrando el check obligatorio y la revisión obligatoria.

### Pull requests y revisión

Cada integrante trabajó en su propia rama, abrió un pull request y recibió revisión de otro integrante. De esta forma todos participaron como autores de código y como revisores.

Capturas requeridas: para cada integrante, pegar captura del PR abierto y del PR revisado, mostrando que el build corrió.

### Prueba de bloqueo por fallo

Para demostrar que la tubería bloquea errores, se realizó un cambio intencional que rompió una prueba. GitHub Actions marcó el check como fallido y el pull request quedó bloqueado. Luego se corrigió el error en un nuevo commit, el workflow volvió a pasar y el merge quedó habilitado.

Capturas requeridas:

1. Pull request bloqueado por check fallido.
2. Check pasando después de corregir el error.

### Release automatizado

El workflow también incluye un job de release que se ejecuta después de un push a `main` si las pruebas pasan. Este job construye el paquete con `python -m build`, sube el resultado como artifact descargable y crea un tag de versión para el commit.

Capturas requeridas:

- Artifact generado en GitHub Actions.
- Tag de versión creado en el repositorio.

## Decisión sobre Continuous Deployment

No activaríamos continuous deployment todavía para esta aplicación. El pipeline actual ya hace integración continua y deja un paquete listo para entregar, lo cual se acerca a continuous delivery. Sin embargo, desplegar automáticamente cada cambio sin aprobación humana puede ser riesgoso si una prueba no cubre un caso importante.

Para convertirlo en continuous deployment habría que agregar un paso que publique o instale automáticamente cada versión aprobada en el entorno usado por los usuarios. También habría que eliminar la aprobación manual de release. En esta aplicación, los riesgos principales son errores en los préstamos: por ejemplo, permitir que un libro ya prestado vuelva a prestarse, calcular mal los vencimientos o corromper el archivo JSON de datos. Si uno de esos errores llegara a producción, afectaría directamente el control de la biblioteca.

Antes de confiar en despliegues automáticos, el equipo debería agregar salvaguardas como rollback, ambiente de staging y monitoreo. Un rollback permite volver rápido a una versión anterior si una versión nueva falla. Un ambiente de staging permite probar el sistema en condiciones parecidas a producción antes de exponerlo a usuarios reales. El monitoreo permite detectar fallos después del despliegue.

La decisión cambiaría si el proyecto tuviera más cobertura de pruebas, pruebas de integración sobre el archivo JSON, respaldo automático de datos, un mecanismo claro de rollback y monitoreo básico de errores.

## Preguntas

### ¿Por qué vale la pena configurar integración continua en un proyecto de equipo?

Vale la pena porque reduce el riesgo de integrar tarde cambios incompatibles. Sin CI, cada integrante puede creer que su parte funciona localmente, pero al juntar todo aparecen conflictos, errores ocultos o pruebas rotas. Con CI, cada push y cada pull request se verifica en un ambiente limpio, así que los problemas aparecen temprano y se pueden corregir cuando todavía es fácil identificar qué cambio los causó.

### Comparación de herramientas de CI/CD

| Herramienta | Cómo se configura | Dónde corre el build | Ventaja principal | Desventaja principal |
|---|---|---|---|---|
| GitHub Actions | Archivos YAML en `.github/workflows` | Runners de GitHub o self-hosted runners | Muy integrado con repositorios de GitHub | Depende del ecosistema de GitHub |
| Jenkins | Jobs o Jenkinsfile en el repositorio | Servidor propio o agentes configurados | Muy flexible y personalizable | Requiere más instalación y mantenimiento |
| GitLab CI | Archivo `.gitlab-ci.yml` | Runners de GitLab o propios | Muy completo para repositorios en GitLab | Menos conveniente si el código está en GitHub |
| CircleCI | Archivo `.circleci/config.yml` | Infraestructura de CircleCI o runners propios | Configuración clara y buena experiencia CI | Puede requerir cuenta/plan aparte |

Para este proyecto se escogería GitHub Actions porque el repositorio está en GitHub, no requiere instalar un servidor adicional y su configuración con YAML es suficiente para correr pruebas, proteger ramas, generar artifacts y crear tags.

### ¿Cómo se relaciona CI con equipos ágiles?

La integración continua encaja con equipos ágiles porque las iteraciones cortas necesitan feedback rápido. Si el equipo entrega cambios pequeños y frecuentes, CI confirma constantemente que el producto sigue funcionando. Esto permite corregir problemas durante la iteración y no al final, cuando ya hay muchos cambios acumulados.

## Conclusiones

La práctica permitió construir una aplicación funcional y organizar el trabajo en ramas independientes. La integración continua ayudó a verificar automáticamente cada cambio y a mantener estable la rama principal. La protección de rama y las revisiones obligatorias reforzaron el trabajo colaborativo, porque ningún cambio pudo entrar sin pruebas exitosas y revisión de otro integrante.

## Recomendaciones

Se recomienda aumentar la cobertura de pruebas antes de activar despliegues automáticos. También conviene documentar mejor los comandos de uso, mantener commits pequeños y revisar los pull requests con atención. Para proyectos reales, sería importante añadir respaldo de datos, ambiente de staging, rollback y monitoreo.

## Referencias

- GitHub Docs. GitHub Actions documentation.
- Jenkins Documentation. Using Jenkins.
- GitLab Docs. GitLab CI/CD.
- CircleCI Docs. Configuration reference.
