# Analisis de arquitectura - Defender (MISW-4407)

> Borrador para el documento calificable de post-mortem grupal. Las secciones marcadas
> con [COMPLETAR] las llena el equipo; el resto ya corresponde al codigo actual.

## 1. Vision general

El juego sigue una arquitectura **ECS** (Entidad-Componente-Sistema) sobre `esper 2.5`:

- **Entidad**: un entero sin comportamiento ni datos propios.
- **Componente**: estructura de datos pura, sin logica (`src/ecs/components/`).
- **Sistema**: funcion libre que consulta el mundo por combinaciones de componentes y
  modifica sus datos (`src/ecs/systems/`).

Alrededor de ECS hay una capa de motor (`src/engine/`) que no conoce el juego: game
loop, escenas, servicios de recursos y utilidades matematicas.

## 2. Componentes

| Componente | Datos | Por que existe |
|---|---|---|
| `CTransform` | posicion en coordenadas de **mundo** | el mundo es 6 veces mas ancho que la pantalla |
| `CVelocity` | velocidad | separa "moverse" de "decidir a donde" |
| `CSurface` | textura, `area` (cuadro actual), `flip_h` | el area define tambien el tamaño de colision |
| `CAnimation` | cuadros y animaciones | animacion 2D cuadro a cuadro |
| `CInputCommand` | nombre de accion, tecla, dispositivo, fase | patron Command |
| `CCamera` | ventana del mundo visible | bono de camara |
| `CTerrain` | vertices del relieve | el suelo no es una linea recta |
| `CText` / `CHudField` | texto en pantalla / enlace a un dato de partida | HUD y menus dentro de ECS |
| `CGameState` | puntaje, vidas, olas, astronautas | estado de partida como componente singleton |
| `CPlayerState` | estado y direccion de la nave | patron State |
| `CLanderState` | estado del Lander y sus parametros | patron State |
| `CHumanoidState` | estado del astronauta y su captor | patron State |
| `CLifetime` | segundos de vida | el laser desaparece solo |
| `CBlink` | parpadeo temporal | game feel: invulnerabilidad visible |

Las **tags** (`CTagPlayer`, `CTagLander`, `CTagLaser`, `CTagHumanoid`,
`CTagExplosion`) son componentes vacios que sirven para filtrar consultas.

## 3. Sistemas y orden de ejecucion

El orden de `PlayScene.do_update` no es arbitrario:

1. `system_lander_state` - las IAs deciden su velocidad
2. `system_movement` - se aplica la velocidad
3. `system_world_wrap` - se normaliza la posicion al cilindro
4. `system_player_limits` - la nave no atraviesa el terreno ni el techo
5. `system_humanoid` - estados del astronauta y enganche al suelo
6. colisiones (laser-Lander, laser-astronauta, nave-astronauta, nave-Lander)
7. `system_lifetime` - muere lo que caduco
8. `system_player_state` - estado y volteo del sprite
9. `system_animation` / `system_blink` / `system_explosion_kill`
10. `system_camera` - la camara sigue a la nave (al final, para dibujar sin retraso)
11. `system_hud` - los textos copian el estado de la partida

El render tiene cuatro sistemas: terreno, sprites, radar y textos.

## 4. Decisiones de diseño

**Coordenadas de mundo, no de pantalla.** Todo `CTransform` esta en mundo y solo el
render convierte a pantalla. Asi ningun sistema de logica necesita saber que existe
una camara.

**El planeta es un cilindro.** `src/engine/world_math.py` concentra las tres
operaciones que eso implica (`wrap_x`, `signed_delta_x`, `world_to_screen_x`) y
`src/engine/collision.py` la colision con wrap. Es el punto donde mas se notan las
matematicas del juego: una resta de x simple produce bugs en la costura del mundo.

**Una escena = un mundo ECS.** Cambiar de escena no deja entidades sueltas y el menu
no necesita saber nada del nivel.

**Todo numero vive en JSON.** 11 archivos de configuracion; ajustar la dificultad no
toca codigo.

[COMPLETAR] Diagrama de componentes/sistemas.

## 5. Patrones

[COMPLETAR] Analisis de ECS frente a herencia tradicional, con ejemplos del propio
proyecto (ver `src/ecs/components/tags/` y como un Mutant sera un Lander con otros
componentes en vez de una subclase).

## 6. Reflexion

[COMPLETAR] Que salio bien, que salio mal, que cambiariamos.

## 7. Evolucion semana a semana

[COMPLETAR] Bitacora.
