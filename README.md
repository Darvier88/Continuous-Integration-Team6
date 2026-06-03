# CaféLibro — Library Loan Manager

Proyecto de taller de Integración Continua. Es una aplicación de línea de comandos para administrar préstamos de libros usando un archivo JSON como almacenamiento compartido.

## Integrantes y división sugerida para 6 personas

| Persona | Feature | Rama sugerida | Qué debe entregar |
|---|---|---|---|
| Integrante 1 | Registrar miembro | `feature/register-member` | Código, prueba de registro exitoso y prueba de ID duplicado |
| Integrante 2 | Prestar libro | `feature/loan-book` | Código, prueba de préstamo exitoso, libro inexistente, miembro inexistente y libro ya prestado |
| Integrante 3 | Devolver libro | `feature/return-book` | Código, prueba de devolución exitosa y prueba de libro no prestado |
| Integrante 4 | Listar préstamos de un miembro | `feature/member-loans` | Código, prueba de listado correcto y miembro inexistente |
| Integrante 5 | Reportar préstamos vencidos | `feature/overdue-loans` | Código, prueba de vencidos y prueba de no vencidos |
| Integrante 6 | Registrar libro | `feature/register-book` | Código, prueba de registro exitoso y código duplicado |

## Revisión cruzada recomendada

- Integrante 1 revisa a Integrante 2.
- Integrante 2 revisa a Integrante 3.
- Integrante 3 revisa a Integrante 4.
- Integrante 4 revisa a Integrante 5.
- Integrante 5 revisa a Integrante 6.
- Integrante 6 revisa a Integrante 1.

## Instalación local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .
```

## Ejecutar pruebas

```bash
pytest -q
```

## Uso de la aplicación

```bash
python -m cafelibro add-book B001 "Clean Code"
python -m cafelibro add-member M001 "Ana Torres"
python -m cafelibro loan B001 M001 2026-06-20
python -m cafelibro member-loans M001
python -m cafelibro overdue --today 2026-07-01
python -m cafelibro return B001
```

Por defecto usa `data/library.json`. Para pruebas manuales se puede usar otro archivo:

```bash
python -m cafelibro --db demo.json add-book B002 "Refactoring"
```

## Flujo de trabajo GitHub

1. Crear repositorio público.
2. Subir este proyecto.
3. Agregar a todos los miembros como colaboradores.
4. Cada integrante crea su rama: `git checkout -b feature/nombre-feature`.
5. Cada integrante hace commits propios y abre Pull Request contra `main`.
6. Otro integrante revisa y aprueba.
7. GitHub Actions debe estar en verde antes de hacer merge.

## Protección de rama main

En GitHub: `Settings > Branches > Add branch protection rule`.

Configurar:

- Branch name pattern: `main`
- Require a pull request before merging
- Require approvals: `1`
- Require status checks to pass before merging
- Seleccionar el check `test` del workflow `CI`

## Release automático

El archivo `.github/workflows/ci.yml` tiene dos jobs:

- `test`: se ejecuta en push y pull request hacia `main`.
- `release`: se ejecuta solo cuando hay push a `main`, después de que las pruebas pasan. Construye el paquete, sube el artifact y crea un tag tipo `v0.1.<run_number>`.
