# How to print the joystick cap

**Read this before you print `joystick.stl`.** The other parts print fine on
normal PETG settings. The joystick cap does not. It is small (10 × 10 × 5 mm),
and on default settings it comes out weak and breaks easily.
These settings came from Austin printing many of them.

## The settings

| Setting | Value |
|---|---|
| Material | PETG |
| Nozzle | 0.4 mm |
| Layer height | 0.16 mm (first layer 0.2 mm) |
| Walls (perimeters) | 4 |
| Top layers | 6 |
| Bottom layers | 4 |
| Infill | 15 %, grid |
| First layer | 20 mm/s, 0.42 mm line width, 0.95 flow |
| Elephant-foot compensation | 0.2 mm |
| Outer wall speed | 40 mm/s |
| Inner wall speed | 60 mm/s |
| Minimum layer time | 20 s |
| Part cooling fan | 60–90 %, off for the first 3 layers |
| Nozzle temperature | 240 °C first layer, then 235 °C |
| Bed temperature | 70 °C first layer, then 60 °C |
| Bed | Textured plate |
| Supports | None |
| Brim / raft | None |
| Copies | **6 or more on one plate** |

Don't rotate it. The file is already the right way up: flange on the bed.

## Why

- **Print at least 6.** One cap is too small to cool between layers. Each
  layer takes a couple of seconds, so the hot nozzle sits on plastic that
  is still soft, and the layers come out melted together and weak. With 6
  on the plate, each cap gets time to cool while the nozzle does the others.
  You only need one cap. Keep the rest as spares.
- **Minimum layer time 20 s.** Same reason. If you print fewer than 6, this
  makes the printer slow down to get the cooling time. 6 or more is still
  better, because a very slow nozzle also heats the part.
- **4 walls, 6 top, 4 bottom.** The cap is so small that this makes it
  almost solid plastic, which is what makes it strong. The 15 % infill
  hardly matters.
- **Slow first layer, elephant-foot 0.2, slow outer wall.** The stem socket
  is at the bottom. A squished first layer shrinks it. These keep the socket
  the right size, so the cap grips the joystick stem.
- **Fan off for the first 3 layers, hotter first layer.** Helps the caps
  stick to the bed. After that the fan cools each layer so it sets.
- **No brim.** A brim on a part this small is hard to take off cleanly, and
  what is left stops the flange sitting flat under the lid.
- **Pull them cold.** PETG sticks hard to the bed
  when hot. Pulling a warm cap bends it or tears the bottom layers, and the
  socket stops fitting.

## Check before you use one

- The cap is not stringy or blobby on top.
- The socket on the bottom is clean, with no strings or bits inside.
- Push it onto the stem by hand. It should sit firm and not wobble. If it
  is loose or will not go on, try another one from the batch.
