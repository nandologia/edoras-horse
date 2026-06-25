# Edoras Horse

A standalone larger-breed horse mob for **Mineclonia**, with deep locomotion and
behaviour: a four-tier gait system, per-horse speed genetics, hunger/thirst needs
with head-down grazing and drinking, and a canter flee when struck. It uses the
**PKZ Horse Rig** coat textures on an upscaled copy of the canonical Mineclonia
horse mesh.

## Features

* **Four-tier manual gaits** — Walk → Trot → Canter → Gallop, each with its own
  animation and speed. While riding, hold **W** to move; tap **E** to shift up a
  gait and **S** to shift down. Releasing W (or hitting an obstacle) drops back to
  a walk. **Sneak** to dismount.
* **Per-horse speed genetics** — every horse rolls a fixed quality level at spawn
  (shown as a 5-star rating in its gear panel) that sets its top speed in each gait.
* **Hunger & thirst** — hunger is a slow biological need; thirst doubles as a
  *sprint resource* drained by galloping. A hungry or parched horse gets balky and
  will refuse the faster gaits, or buck its rider when critical.
* **Grazing & drinking** — an unmounted horse forages: it lowers its head to the
  ground and crops grass spot by spot across a field, and drinks (head down,
  gradually) at water.
* **Flee** — when hit by a player it canters away from the attacker.
* **Taming** — a wild horse must be broken in before it accepts tack. Right-click
  it **empty-handed** to mount bareback; after a short ride it either accepts you
  (tamed, with heart particles) or bucks you off. Each attempt raises its temper, so
  it grows likelier to settle — and feeding a wild horse helps gentle it too.
* **Tack & storage** — a *tamed* horse accepts a saddle, horse armor, and a
  craftable **saddlebag** that unlocks an on-horse storage compartment. Sneak +
  right-click opens the gear panel (with a live condition readout).
* **Lead-following** — with the optional `leads` mod, a leashed horse trails the
  player under its own power instead of being dragged.
* **Potion of the Mearas** — a brewed potion that converts a **tamed** vanilla horse
  (`mobs_mc:horse`) into an Edoras horse, so you can upgrade one you already raised
  instead of waiting for a wild Edoras spawn. **Sneak + use** it on the horse; any
  saddle or armor it wears (and its tame/owner) carry over. Requires the optional
  `mcl_potions`.
* **Natural spawning** — populates Plains and Savanna (requires `mobs_mc`).

## Saddlebag recipe

```
[chest] [     ] [chest]
[leather][leather][leather]
[carpet][carpet][carpet]
```

## Potion of the Mearas recipe

Needs `mcl_potions`. Craft the dye from horse-charming foods, then brew it:

1. **Craft** the **Mearas Dye** on a crafting table:

   ```
   [sugar]       [white dye]    [sugar]
   [gold carrot] [golden apple] [gold carrot]
   [sugar]       [white dye]    [sugar]
   ```

2. **Brew** in a brewing stand: `Mearas Dye` + Water Bottles → **Potion of the Mearas**

Then **sneak + use** the potion on a **tamed** vanilla horse to turn it into an
Edoras horse. Its saddle and armor (and tame/owner) carry over. An untamed horse
must be tamed first.

## Installation

1. Copy the `edoras_horse` folder into your Mineclonia `mods/` directory.
2. Enable **Edoras Horse** in your world's mod configuration.

Get a horse via the creative spawn egg, or wait for one to spawn in grassland.

## Dependencies

* **Required:** `mcl_mobs` (core Mineclonia mob framework).
* **Optional:** `mobs_mc` (natural spawners + the vanilla horse the conversion
  potion targets), `mcl_formspec` (gear-panel slot backgrounds), `leads`
  (lead-following), `mcl_potions` + `mcl_core` + `mcl_farming` + `mcl_dyes` (the
  Potion of the Mearas and its recipe). The mod loads and runs without any of these
  — the related features just stay inactive.

No changes to Mineclonia's own files are required.

## License & credits

This mod combines works under two licenses (full texts bundled as `LICENSE.txt`
and `LICENSE-CC-BY-4.0.txt`; per-file details in `LICENSE-media.md`):

* **Code and model** — GPLv3.
  * The horse mesh is a modified copy of Mineclonia's `mobs_mc_horse.b3d`, which is
    by **22i** (https://github.com/22i) under GPLv3.
* **Coat & marking textures** — CC BY 4.0.
  * *PKZ Horse Rig by **Endertainer007**, licensed under CC BY 4.0*
    (https://creativecommons.org/licenses/by/4.0/). Used verbatim.

Mod by **nando**. When redistributing, keep the GPLv3 model/code terms and credit
22i (mesh) and Endertainer007 (coat textures).
