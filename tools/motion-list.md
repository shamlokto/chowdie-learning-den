# "Things that move" clips (Den wish list): 18 clips

The player is already live in `motion.js`. Drop each finished clip into `img/motion/` and it starts playing; no code change is needed. A clip that isn't there yet is skipped, so these can arrive one at a time.

Style: the Den's warm children's picture-book gouache, matching the painting each clip starts from. No text, letters or numbers.

**Deliver each clip as**
- `img/motion/<id>.mp4`: H.264, 1280x720 (16:9), 3 to 6 seconds, muted, under 1 MB. Don't loop it; it plays once per tap.
- `img/motion/<id>-poster.webp`: the clip's first frame.

**Start and end on the still painting.** Each clip plays over a painting that is already on screen. The first frame should match that painting, and the clip should settle back to it at the end, so nothing jumps when the clip appears or disappears.

## Magic doors: tapping a subject in the Den wakes up its painting
Shown in the subject's banner, a wide strip cropped from the middle of the painting (vertical crop position in brackets). Keep the motion inside that band.

| Clip id | Starts from (img/…) | What moves |
|---|---|---|
| door-maths | maths-classroom.webp (68%) | counting beads click along, chalk dust sparkles, a paper plane drifts across |
| door-english | english-library.webp (68%) | book pages flutter, a bookmark ribbon sways, dust motes drift in the window light |
| door-chinese | chinese-garden.webp (68%) | red lanterns sway, koi ripple the pond, a willow branch moves in the breeze |
| door-science | sci-garden.webp (45%) | a butterfly flits, bubbles rise from a jar, leaves sway |
| door-spelling | spelling-nest.webp (30%) | the nest glows, embers drift up, feathers shimmer |
| door-music | music-stage.webp (68%) | spotlights sweep, music-note shapes float up, the curtain ripples |
| door-stories | stories-nook.webp (68%) | the lamp flickers warmly, a page turns, dust motes drift in the light |
| door-bible | bible-banner.webp (55%) | desert sand drifts, a palm frond sways, stars twinkle softly |
| door-grownups | grownups-desk.webp (68%) | steam curls from the cup, the curtain moves, the clock pendulum swings |

## Crew says hello: tapping a portrait in "Meet your learning crew"
Shown in a 16:9 pop-up. Start from the character's portrait (`img/crew/full/<name>.webp`), centred on a plain warm cream background.

| Clip id | Character | What they do |
|---|---|---|
| hello-chowdie | Chowdie the otter | waves with both paws and does a happy little spin |
| hello-wala | Wala the Koala | waves, then hugs a leaf and giggles |
| hello-flamecharge | Flamecharge the Phoenix | flaps her flame wings, sparks swirl round her |
| hello-flame | Flame the Eagle | spreads his wings, salutes with one wing tip |
| hello-mommy | Mommy the Elephant | raises her trunk and toots a cheerful note, ears flapping |
| hello-baddie | Baddie Vampire (crocodile) | sneaky wave, swirls his cape and grins (silly, not scary) |

## Baddie's lair and the Baddie Daddy celebration: boss levels
Shown over the lesson stage (16:10, a little taller than 16:9; keep the action away from the top and bottom edges).

| Clip id | Starts from | What happens | When it plays |
|---|---|---|---|
| lair-intro | img/boss-lair.webp | Baddie pops up from behind something with a cheeky laugh and a cape swirl | when a boss level opens |
| lair-escape | img/boss-lair.webp with Baddie in it | Baddie scurries off and vanishes in a puff of green smoke, leaving the lair empty | after the last Baddie lie; fireworks follow |
| daddy-bow | img/music-stage.webp | the crew cheers on stage while Baddie Daddy (top hat, cane, purple cape) takes a big funny bow and his hat falls off | after Baddie Daddy is beaten; fireworks follow |

## Notes
- Clips play only when tapped. They never play for children who turn off motion; they just see the still painting.
- A tap on a playing clip skips it.
- After `lair-escape` or `daddy-bow`, the win fireworks wait for the clip to finish. If a clip is missing, they go off as before.
