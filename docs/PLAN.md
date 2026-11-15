# Plan de trabajo

## Hecho

- Service Locator con texturas, sonidos y fuentes; precarga desde `assets.json`
- Patron Escena: menu, juego y game over, cada una con su mundo ECS
- `main.py` asincrono: listo para exportar a web con pygbag
- Sprites y animacion cuadro a cuadro (placeholders generados con `tools/`)
- Fuente de mapa de bits 5x7 para HUD y menus
- Mundo cilindrico de 1920 px, camara que sigue a la nave, terreno procedural
- Radar de largo alcance y HUD
- Astronautas con sus cuatro estados y abduccion por parte de los Landers
- Colisiones, explosiones, vidas, invulnerabilidad, olas
- Trampas (F2, F3) y vista de colisiones (F1)

## Siguiente: que el juego tenga identidad propia

La base viene de Defender; lo que sigue es lo que lo hace distinto.

- Arte definitivo propio (respetando los tamaños de `tools/make_placeholder_art.py`)
- Sonidos en .ogg (sfxr + Audacity; ver `assets/snd/LEEME.txt`)
- Enemigos nuevos diseñados para este juego, construidos como combinaciones de
  componentes y no como subclases
- Una mecanica propia alrededor de los astronautas (el "tether": por ejemplo,
  remolcarlos con un cable que afecta el manejo de la nave)
- Puntaje alto persistente y vidas extra por puntaje

## Publicacion

- Build web con pygbag y pagina en itch.io con descripcion y pantallazos
- Tag de version en GitHub
