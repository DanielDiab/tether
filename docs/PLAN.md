# Plan de trabajo

## Hecho (semanas 1 y 2 del plan)

- Service Locator con texturas, sonidos y fuentes; precarga desde `assets.json`
- Patron Escena: menu, juego y game over, cada una con su mundo ECS
- `main.py` asincrono: listo para exportar a web con pygbag
- Sprites y animacion cuadro a cuadro (placeholders generados con `tools/`)
- Mundo cilindrico de 1920 px, camara que sigue a la nave, terreno procedural
- Radar de largo alcance y HUD
- Astronautas con sus cuatro estados y abduccion por parte de los Landers
- Colisiones, explosiones, vidas, invulnerabilidad, olas
- Trampas (F2, F3) y vista de colisiones (F1)

## Pendiente (semana 3)

- Enemigos restantes: Mutant, Bomber, Pod, Swarmer, Baiter
- Smart bomb e hyperspace
- Explosion del planeta al perder a todos los astronautas
- Sonidos en .ogg y fuente de pixel
- Sprites definitivos (respetando los tamaños de `tools/make_placeholder_art.py`)
- Puntaje alto persistente, vidas y bombas extra cada 10.000 puntos
- Bono: steering behaviours en los Baiters

## Semana 4

- Publicacion en itch.io con descripcion y pantallazo
- Documento de arquitectura y post-mortem grupal (`docs/ARQUITECTURA.md`)
- Post-mortem individual de cada integrante
- Video de presentacion
- Tag final en GitHub

## Reparto sugerido (4 personas)

| Rol | Responsabilidad |
|---|---|
| Arquitectura | motor, escenas, service locator, configs, despliegue |
| Jugador | nave, disparo, camara, colisiones, game feel |
| IA | maquinas de estado de los enemigos, olas, steering |
| Presentacion | sprites, animacion, sonido, HUD, radar, video |

La rubrica penaliza que algun integrante no programe: cada rol debe tener commits.
