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
| Layer height | 0.16 mm |
| Walls (perimeters) | 4 |
| Top layers | 6 |
| Bottom layers | 4 |
| Infill | 15 % |
| First layer speed | 20 mm/s |
| Outer wall speed | 40 mm/s |
| Inner wall speed | 60 mm/s |
| Minimum layer time | 20 s |
| Nozzle temperature | 235 °C |
| Bed temperature | 60–70 °C |
| Supports | None |
| Brim / raft | None |
| Copies | **At least 6 on one plate** |

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
- **Slow first layer and slow outer wall.** The stem socket is at the
  bottom. A clean first layer and outer wall keep the socket the right size,
  so the cap grips the joystick stem.
- **No brim.** A brim on a part this small is hard to take off cleanly, and
  what is left stops the flange sitting flat under the lid.
- **Let them cool before you take them off.** PETG sticks hard to the bed
  when hot. Pulling a warm cap bends it or tears the bottom layers, and the
  socket stops fitting.

## Check before you use one

- The cap is not stringy or blobby on top.
- The socket on the bottom is clean, with no strings or bits inside.
- Push it onto the stem by hand. It should sit firm and not wobble. If it
  is loose or will not go on, try another one from the batch.
