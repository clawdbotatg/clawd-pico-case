# Assembly

Photos in order. Draft. This becomes a one-page guide later.

## What you need

- Screen board (Waveshare Pico-LCD-1.3)
- Pico (the red USB-C RP2040 board)
- Trust M chip board
- 4-wire cable (white, yellow, black, red) with a small plug: [the ones we use (Amazon)](https://www.amazon.com/dp/B0F6TYG426)
- Case: white lid, black base, joystick cap, 4 buttons (1 green, 2 gray, 1 red). Print the joystick cap with [its own settings](../stl/current/JOYSTICK-PRINT.md) or it breaks.
- Wire cutters and strippers, electrical tape, a stiff breadboard jumper wire, tweezers
- A computer with Chrome, and a USB-C cable

## 1. Cable and tools

![Cable and strippers](photos/01-cable-and-strippers.jpg)

![Cable and strippers](photos/01-cable-and-strippers.jpg)

## 2. Cut and strip the wires

Keep one plug. Cut the wires about 2 in (5 cm) from it. Strip off as much as a header socket is deep, about 5 mm (between 1/8 and 1/4 in), so the bare wire goes all the way down.

![Cut and stripped](photos/03-cut-and-stripped-a.jpg)
![Cut and stripped, other view](photos/03-cut-and-stripped-b.jpg)

## 3. Lay out the screen board and the wiring guide

Take out the screen board. Turn it face down, sockets up, USB mark at the top.

Each wire pushes into a socket. No solder. Count sockets from the USB end.

| Wire | Signal | Socket |
|---|---|---|
| White | GND | 3rd on the USB-side row (pin 38) |
| Yellow | 3.3 V | 5th on that row (pin 36) |
| Black | SDA | 6th on the other row (pin 6, GP4) |
| Red | SCL | 7th on the other row (pin 7, GP5) |

<!-- TODO: redraw the wiring guide as a clean diagram for the one-pager -->

![Board face down with wiring guide](photos/04-board-and-guide.jpg)

## 4. Push in white and yellow

Twist the strands at each wire tip tight, so each tip acts like one solid wire.

Push white into socket 3 (GND) and yellow into socket 5 (3V3) on the USB-side row. Do both together.

![White and yellow in the header](photos/05-white-yellow-in-header.jpg)

## 5. Tape over the wires

Put a small piece of electrical tape over the sockets, right on top of the wires, to hold them in.

![Tape over white and yellow](photos/06-tape-over-wires.jpg)

## 6. Poke the holes open

Push a stiff breadboard jumper wire through the tape into each covered socket. This opens the holes so the Pico pins fit later. The tape still holds the wires.

![Poke the holes through the tape (drawing)](photos/07-poke-holes-drawing.jpg)
![Holes poked through the tape](photos/08-black-red-taped.jpg)
![Poking holes through the tape](photos/07-poke-holes-through-tape.jpg)

## 7. Same on the other row: black and red

Push black into socket 6 and red into socket 7. Tape over them. Poke the holes open with the jumper wire.

![Black and red, with guide](photos/08-black-red-guide.jpg)
![Black and red in the header](photos/08-black-red-in-header.jpg)
![Black and red taped](photos/08-black-red-taped.jpg)

## 8. Header ready

All 4 wires in, taped, holes open. Ready for the Pico.

![Header ready for the Pico](photos/09-header-ready.jpg)

## 9. How the plug fits the Trust M

Only 4 wires. Top to bottom in the photo: white, yellow, black, red.

![Cable plugged into Trust M](photos/02-trust-m-plug.jpg)

## 10. Plug in the chip

Plug the cable into the Trust M. It only fits one way.

Lay the Trust M face up on the back of the screen board, over the wires. The Pico goes on top of it next.

![Chip plugged in and laid down (drawing)](photos/10-chip-drawing.jpg)
![Plugged in](photos/10-chip-plugged.jpg)
![Plugged in, from the side](photos/10-chip-plugged-side.jpg)
![Laid down on the board](photos/10-chip-laid-down.jpg)
![Ready for the Pico](photos/10-ready-for-pico.jpg)

## 11. Snap off extra board

Some Picos have a little extra board left on the end, away from the USB-C. Pinch it with pliers and snap it off. Otherwise it won't fit the case.

![Snap off the extra board (drawing)](photos/11-snap-off-tab-drawing.jpg)
![Pinch and snap](photos/11-snap-off-tab.jpg)
![Green Picos still have it, red ones are done](photos/11-picos-with-tabs.jpg)

## 12. Stack the boards

Push the Pico into the sockets, USB-C at the same end as the screen board's USB mark. The Pico's chips and BOOTSEL button face out, away from the screen. Push straight, never at an angle. The Trust M ends up wedged between the two boards. Push the Pico all the way in so it's flush. No pins or wires sticking out, chip fully inside.

If anything sticks out, do it again. It won't fit the case.

![Pico going on, chip wedged under it](photos/11-pico-going-on.jpg)
![Stacked, from the top](photos/10-stacked-top.jpg)
![Chip wedged in between](photos/10-chip-wedged.jpg)
![Headers flush](photos/10-headers-flush.jpg)
![Stacked, USB end](photos/11-stacked-usb.jpg)

## 13. Test the boards

Hold the Pico's BOOTSEL button (tweezers help) and plug in the USB-C. Always hold it. Many Picos come with software installed and won't show up without BOOTSEL. Our pink Picos do: out of the box they flash a green light. Some come blank and work either way. Use a data cable, not a charge-only one. Go to wedgie.dev/test in Chrome and click Test it. Don't unplug while it runs.

First time on this computer? The test page has a one-time setup (a Mac profile, or one command on Linux) so Chrome stops asking about every new Pico.

Wait for the first 3 to go green: Board, Firmware, Chip. That means everything is connected. Unplug it. The other 3 (Shake, Buttons, Colors) come after the case is on.

Chip fails? A wire is in the wrong socket (step 3), a wire came out, or the Trust M touches a Pico pin. Take it apart and check.

![Hold BOOTSEL, plug in](photos/11-bootsel.jpg)
![Test page](photos/11-test-page.jpg)
![Wiping, putting MicroPython on](photos/11-test-wiping.jpg)
![Installing the firmware](photos/11-test-firmware.jpg)

## 14. Pick the base

The base color says what's inside:

- Red: Pico W with a battery (the Atomic wedgie)
- Black: Trust M chip
- Gray: ATECC608 chip

This build is Trust M, so black.

![The three bases](photos/13-bases.jpg)

## 15. Check the USB-C fit

Set the stacked boards into the base, USB-C into the hole. The USB-C port must line up perfectly with the hole.

Not lined up? Push the Pico all the way into the screen board's sockets, and make sure the screen board sits flush on the base's supports.

![USB-C lined up with the hole (drawing)](photos/15-usb-fit-drawing.jpg)
![USB-C lined up with the hole](photos/15-usb-fit-check.jpg)

## 16. Peel the screen protector

Pull the blue tab off the screen.

![Screen protector off](photos/13-screen-protector.jpg)

## 17. Case parts

White lid, black base, joystick cap, 2 gray buttons, 1 green, 1 red.

![Case parts](photos/14-case-parts.jpg)

## 18. Joystick cap

Line up the square hole with the joystick and press hard until it snaps. It takes more force than you'd think.

Check: it stays on upside down, and it clicks up, down, left, right and in. The cap sits flat with a small gap under its rim. The gap is on purpose, so it can tilt.

![Joystick cap, side](photos/15-joystick-side.jpg)
![The gap under the rim](photos/15-joystick-gap.jpg)
![Joystick cap on](photos/15-joystick-on.jpg)

## 19. Buttons into the lid

Lay the lid face down at the edge of the mat, so the buttons can hang out the front. Drop the buttons in with tweezers: green, gray, gray, red. Green sits over the screen board's A button, red over Y.

![Placing buttons with tweezers](photos/16-buttons-tweezers.jpg)
![Buttons placed](photos/16-buttons-placed.jpg)
![Lid, boards and base ready](photos/16-ready.jpg)

## 20. Boards into the base

Push the stacked boards, screen up, into the black base. USB-C end first, into the base's hole, then lower the rest. Don't force it straight down. The screen board lies flat on the base's rails. The USB port is centered in the hole, so a cable plugs in cleanly.

![USB centered in the hole](photos/17-usb-centered.jpg)
![Boards in the base](photos/17-in-base.jpg)
![USB centered in the hole, case closed](photos/17-usb-centered-closed.jpg)

The USB-C port must sit right in the middle of the hole. If it doesn't, something is wrong: take it out and do it again before you close the case.

## 21. Close the case

Flip the base over and lower it, screen side down, into the lid (still face down with the buttons in). Line it up. Keep it upside down and press lid and base together, hard, until they snap. It's tight on purpose, so it won't fall apart.

![Lowering into the lid](photos/18-lower-into-lid.jpg)
![Pressed closed](photos/18-press-closed.jpg)
![Closed](photos/18-closed.jpg)
![USB port, closed](photos/18-closed-usb.jpg)

## 22. Check the feel

Press every button. Push the joystick every way and straight in. Each one should click. Look for anything off: a tilted joystick, a stuck button.

## 23. Full test

Plug it in. It shows "No software". Go to wedgie.dev/test and click Test only (skips the wipe and firmware).

The wedgie shows a red FULL CONTROL warning. Press green on the wedgie to let the computer in.

- Chip: wait for the green check.
- Shake: shake, tap, squeeze, lightly drop it on each side until the counter stops. It hammers the chip and the Pico to catch loose wires.
- Buttons: press each one it asks for. The joystick must not hit the wrong button.
- Colors: each press shows a color. Check for scratches, dead pixels, or a line of printer plastic. Clean it off.

PASS on the wedgie and the page: done. Unplug it.

Need to wipe it again after the case is closed? Press BOOTSEL through the small hole in the base with a paperclip while you plug it in.


![Plugged in](photos/20-booted.jpg)
![Test only](photos/20-test-only.jpg)
![Press green](photos/20-press-green.jpg)
![Full control warning](photos/20-full-control.jpg)
![Shake it](photos/20-shake.jpg)
![Button test](photos/20-buttons.jpg)
![Color test](photos/20-colors.jpg)
![PASS on the wedgie](photos/20-pass.jpg)
![PASS on the page](photos/20-pass-page.jpg)
![No software](photos/20-no-software.jpg)

## 24. Box it

Put it in the box. Build the next one. To use it: wedgie.dev/connect.

![In the box](photos/21-box.jpg)
