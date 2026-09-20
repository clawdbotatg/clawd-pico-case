# Sources

## Forbidden. Never open while working here.

| What | Where | License | Why forbidden |
|---|---|---|---|
| Tomáš Plass, Waveshare Pico 1.3 LCD Case | printables.com/model/1322102 | CC BY-NC 4.0 | No commercial use |
| Zez0000, Raspberry Pi Pico 2 Case - Waveshare 1.3" LCD | makerworld.com/en/models/3230142 | CC BY-NC 4.0 | No commercial use, remix of the above |
| `austintgriffith/picowallet` `case/`, `tools/zezbase`, `tools/zezplate`, emu 3D meshes, HANDOFF case notes, `case/README.md`, `case/BUTTONS.md` | GitHub and `~/picowallet` | derivative of the above | Derived geometry and measurements of their parts |
| Any other case, lid, cap or joystick cap for this board or for a bare Pico | anywhere | any | Keeps the clean room clean. We do not need them |
| Community 3D model of the Pico-LCD-1.3 on GrabCAD | grabcad.com | GrabCAD terms | Someone else's model of the board. Not a case, but not ours. We model the board ourselves |

Photos of the assembled picowallet with the old case exist in the picowallet
repo and on Austin's phone. Do not use them as a design reference either.

## Allowed

Facts about the hardware. Dimensions are facts and are not copyrightable. The
drawings themselves belong to their publishers, so we cite them, we do not
redistribute them unless their license allows.

| What | Where | Notes |
|---|---|---|
| Caliper measurements of the boards on the bench | `MEASUREMENTS.md`, photos in `measurements/` | Primary source. Three readings each |
| Raspberry Pi Pico 2 W datasheet, mechanical drawing | datasheets.raspberrypi.com (pico-2-w-datasheet.pdf) | Board outline, hole positions, connector position |
| Raspberry Pi Pico 2 datasheet, mechanical drawing | datasheets.raspberrypi.com (pico-2-datasheet.pdf) | Same footprint, cross-check |
| Raspberry Pi Pico 2 official STEP model | pip.raspberrypi.com/documents/RP-009061-CA | Raspberry Pi: design files "openly available with no limitations", "use, copy, modify, and distribute for any purpose". Pico 2 W has no STEP; same outline, add the wireless module by caliper |
| Waveshare Pico-LCD-1.3 schematic | files.waveshare.com/wiki/Pico-LCD-1.3/Pico-LCD-1.3_SchDoc.pdf | No part numbers for switches or joystick. No 3D drawing exists for this board (checked 2026-09-20) |
| Waveshare Pico-LCD-1.3 wiki page, dimensions drawing and schematic | waveshare.com/wiki/Pico-LCD-1.3 | Board outline, screen position, button and joystick positions. Do not scroll into any user gallery or related-products case section |
| Component datasheets for the tact switches and the joystick on the LCD board | manufacturer sites, once identified from the schematic or by measurement | Plunger diameter, travel, height, stem shape |
| General engineering references on snap fits, press fits, tact switch caps, FDM tolerances | textbooks, manufacturer design guides, Prusa and Bambu printing guides | Methods, not geometry |
| Our own earlier work that does not touch the case: the Pico firmware, the wallet app | `austintgriffith/picowallet` outside `case/` | Not needed for the case, listed so nobody worries about it |

Anything else goes in `PROVENANCE.md` with a license and Austin's OK first.
