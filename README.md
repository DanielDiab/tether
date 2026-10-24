# DEFENDER - Proyecto final MISW-4407

Reproduccion del arcade **Defender** (Williams Electronics, 1981) en Python con
pygame-ce y arquitectura **ECS** (esper).

> **Por confirmar con el profesor:** el enunciado deja la resolucion en `<TODO>`.
> Este proyecto usa **320x256**, que es la del original y la que usan los clones
> del curso. Si el `window.json` oficial de "RECURSOS DEL PROYECTO" dice otra cosa,
> basta con cambiar `assets/cfg/window.json` (y el `layout` de HUD/radar).

## Ejecutar

```bash
pip install -r requirements.txt
python main.py
```

`esper/` viene incluido en el repo (version 2.5), asi que solo hace falta `pygame-ce`.

## Controles

| Accion | Tecla |
|---|---|
| Mover la nave | Flechas o WASD |
| Disparar | Espacio (o clic izquierdo) |
| Pausa | P |
| Volver al menu | ESC |

### Trampas y depuracion

| Tecla | Efecto |
|---|---|
| F1 | Muestra las cajas de colision |
| F2 | +1 vida |
| F3 | Elimina todos los Landers (pasa de ola) |

Todas las teclas se configuran en `assets/cfg/input.json`.

## Como se juega

Defiende a los astronautas de la superficie. Los **Landers** bajan, buscan un
astronauta, lo capturan y lo suben al techo de la pantalla: si lo logran, el
astronauta se pierde. Si destruyes al Lander mientras sube, el astronauta cae, y
puedes atraparlo con la nave y volver a dejarlo en el suelo (500 puntos).
Cuidado: tu propio laser tambien mata astronautas.

El **radar** de la franja superior muestra el planeta completo: el mundo mide
1920 px (6 pantallas) y es cilindrico, da la vuelta sobre si mismo.

## Estructura

```
main.py                     punto de entrada asincrono (compatible con pygbag)
esper/                      libreria esper 2.5 incluida
assets/cfg/                 TODA la configuracion del juego en JSON
assets/img/                 sprites (placeholder, ver tools/)
assets/snd/ assets/fnt/     sonidos y fuente (pendientes, ver LEEME.txt)
tools/make_placeholder_art.py   genera los sprites placeholder
src/engine/game_engine.py   game loop + gestor de escenas
src/engine/scenes/          Scene, MenuScene, PlayScene, GameOverScene
src/engine/service_locator.py   acceso unico a texturas, sonidos y fuentes
src/engine/service/         TextureService, SoundService, FontService
src/engine/world_math.py    matematicas del mundo cilindrico
src/engine/collision.py     colision AABB con wrap horizontal
src/create/prefab_creator.py    fabrica de entidades
src/ecs/components/         componentes (datos)
src/ecs/systems/            sistemas (logica)
```

## Patrones aplicados (rubrica de codigo fuente)

| Patron | Donde |
|---|---|
| **ECS** | `src/ecs/` completo; los componentes solo tienen datos y los sistemas solo logica |
| **Game Loop** | `GameEngine.run`: tiempo -> eventos -> update -> draw |
| **Command** | `CInputCommand` + `system_input_player`; las escenas reciben nombres de accion, nunca teclas. El mapeo esta en `input.json` |
| **State** | `CPlayerState`, `CLanderState` (DESCEND/SEARCH/ABDUCT), `CHumanoidState` (WALK/ABDUCTED/FALLING/CARRIED) con un sistema por maquina de estados |
| **Service Locator** | `ServiceLocator` con los tres servicios de recursos; ningun sistema carga archivos por su cuenta |
| **Escena** | `Scene` y sus tres implementaciones; cada escena tiene su propio mundo ECS |
| **Archivos de configuracion** | 11 archivos en `assets/cfg/` |

## Estado actual

Implementado: menu, juego y game over; mundo cilindrico con camara y radar; terreno
procedural; nave con disparo; Landers con maquina de estados y abduccion; astronautas
con sus cuatro estados; colisiones; explosiones animadas; HUD; olas; vidas e
invulnerabilidad con parpadeo; trampas y depuracion.

Pendiente (semana 3 del plan): Mutants, Bombers, Pods/Swarmers, Baiters, smart bomb,
hyperspace, sonidos, sprites definitivos, y la explosion del planeta al perder a todos
los astronautas.

## Publicar

```bash
# Web (itch.io)
pygbag --build .        # genera build/web/
# subir build/web/web.zip a itch.io marcandolo como "This file will be played in the browser"

# Windows
pyinstaller --onefile --add-data "assets;assets" --add-data "esper;esper" main.py
```
