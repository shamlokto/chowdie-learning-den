# Ten new Bible stories: build plan (HQ, Nov 2026)

Owner approved all ten. Same process and style as Abraham / Samson / Ruth / David: faithful NIV retelling, "only good qualities
that God loves", holy and decent, quiet golden Bible look (no den-buddy, no fireworks, no confetti, soft golden glow).
God the Father is never shown (light from above only). Jesus (story 9 and the hillside in story 2) is only seen from behind
or the side, face not shown, white robe and soft golden light. No blood, no weapons in use, nothing scary.

Art: HQ paints everything on RunPod into `img/<dir>/<scene>.webp` (1280x720 stills, `paint(n)` full-stage like the
existing Bible decks). Clips are wired by HQ through `tools/den-clips.py` (it overlays the clip on the still automatically),
so decks just call `paint('<scene>')`; do not add your own <video> for these. Sticker object: `img/bible/sticker-<dir>.webp`.

Deck file: `bible/<dir>.html`, copied from `bible/abraham.html` (keep its engine, voices, quiz, quiet polish; ~6 chapters,
5 quizzes, a "Say thank you to God" style ending). Voices: run `node tools/den-voices.js bible/<dir>.html` (add any new
CAST voices in tools/den-voices.js the way abraham/sarah were added).

| # | dir | Title (polished) | Builder | Bible |
|---|-----|------------------|---------|-------|
| 1 | noah | Noah and the Rainbow: God Keeps His Promise | story team | Genesis 6–9 |
| 2 | builders | The Wise and Foolish Builders | story team | Matthew 7:24–27 |
| 3 | nehemiah | Nehemiah Rebuilds the Wall: The Lord Builds | story team | Nehemiah 1–6, 8, 12 |
| 4 | sheep | The Lost Sheep and the Good Shepherd | story team | Luke 15:1–7; Psalm 23 |
| 5 | jonah | Jonah and God's Second Chance | artwork team | Jonah 1–4 |
| 6 | joseph | Joseph Forgives His Brothers | artwork team | Genesis 37, 39–46 |
| 7 | daniel | Daniel and His Friends: Faithful in a Strange Land | artwork team | Daniel 1, 3, 6 |
| 8 | prodigal | The Prodigal Son: The Father's Welcome Home | software team | Luke 15:11–32 |
| 9 | children | Jesus Blesses the Children | software team | Mark 10:13–16 |
| 10 | church | The First Church: Sharing and Praying Together | software team | Acts 2:1–47; 4:32–35 |

Scenes (10 each, in story order). **Bold** = also a looping clip.

1. noah: world (grey village, people turned away from God, gentle), call (Noah kneels at sunset, light from above), build (Noah and sons build the ark on dry land, neighbours laugh), animals (animals two by two up the ramp), **rain** (rain pours, ark afloat, door shut), flood (ark alone on wide calm water), **dove** (Noah sends out the dove), olive (dove returns with an olive leaf), land (ark on a green mountain, animals come out), **rainbow** (family gives thanks under the rainbow)
2. builders: teach (crowd on a hillside listening, teacher far away seen from behind), dig (wise builder digs down to rock), rock (stone house built on rock), sand (foolish builder lounging on a beach), quick (flimsy house on sand), **stormrock** (storm beats the house on the rock, it stands, warm window), **stormsand** (waves wash sand from under the house on sand), fallen (house on sand collapsed, builder sad under a cloak, gentle), **firm** (sun returns, wise builder's family safe at the door), listen (family reading God's word by lamplight)
3. nehemiah: news (in the Persian palace, sad news from Jerusalem), cup (Nehemiah serves the king, the king notices his sad face), prays (Nehemiah prays at a night window), journey (riding with a small group toward Jerusalem), ruins (by moonlight with a lamp, broken walls and burnt gates), **together** (families rebuild the wall together), mockers (two scornful men laugh from a hill, workers keep working), watch (workers build while others keep watch with a trumpet), **done** (finished wall and new gates in sunlight), **praise** (people celebrate with music on the wall)
4. sheep: flock (shepherd counts sheep at the fold at sunset), missing (one is missing, 99 resting), **search** (shepherd crosses rocky hills with a lantern at dusk), thorns (searching by thorny bushes and a stream), found (finds the little lamb on a ledge), carry (carries the lamb home on his shoulders), party (neighbours rejoice with him), **waters** (leads the flock beside quiet waters), rest (sheep lie down in green pastures), **stars** (shepherd keeps watch by a fire under the stars)
5. jonah: call (Jonah worried, turning away), ship (boards a ship at the port of Joppa), **storm** (ship tossed in a great storm, sailors with ropes), calm (sea calm again, sailors praying), **fish** (a huge gentle fish swims toward Jonah), inside (Jonah prays inside the fish, dim glow), shore (the fish brings him to the beach), nineveh (Jonah speaks in the great city), sorry (the king and people kneel, sorry), **vine** (Jonah under a leafy vine looking at the city)
6. joseph: coat (Jacob gives Joseph the colourful coat, brothers jealous), dreams (Joseph asleep, dream of sun, moon and eleven stars), well (Joseph sad in an empty dry well, looking up), **caravan** (walking with a traders' camel caravan to Egypt), prison (Joseph kindly helps two prisoners), pharaoh (Joseph explains Pharaoh's dreams), **grain** (Joseph the ruler stores grain in great granaries), bow (the brothers bow, not knowing him), **forgive** (Joseph hugs his brothers with tears of joy), family (old Jacob reunited with Joseph)
7. daniel: babylon (four young men arrive at the Babylon palace), food (Daniel politely chooses vegetables and water), healthy (after ten days they are bright and strong), statue (three friends stand while everyone bows to the golden statue), **furnace** (three friends walk safe in the fire with a fourth figure of bright light), **praying** (Daniel prays at his open window), den (Daniel calm in the lions' den, lions lying down), **lions** (soft light, lions asleep beside Daniel), morning (King Darius at the den mouth at dawn, overjoyed), faithful (Daniel and his friends pray together under the stars)
8. prodigal: ask (younger son asks for his share, father sad), leave (son leaves on a donkey, father watches), spend (son feasting and spending in a far city), empty (empty purse, famine, alone), pigs (son feeds pigs, hungry), think (son remembers home), **road** (son walks the long road home), **run** (father runs to him with open arms), robe (father hugs him, gives robe and ring), **feast** (welcome-home feast; father invites the older brother in)
9. children: road (families bring little children along a road), crowd (crowd around Jesus, seen from behind), stop (disciples tell the families to go away, children disappointed), **welcome** (Jesus, from behind, opens his arms; children run to him), bless (children gathered close, his hand gently on a child's head), story (children listen and laugh), flowers (children give him wildflowers), **meadow** (children play joyfully in a sunlit meadow), **home** (families walk home at sunset), bedtime (children pray at bedtime)
10. church: **pentecost** (believers praying in an upper room, soft flames of light, curtains blowing), peter (Peter speaks to a big crowd), baptise (people baptised in a river, joyful), **share** (believers share bread together in a home), give (bringing things to share with those in need), temple (praying together in the temple courts), help (caring for widows and the sick), sing (families singing praise), **grow** (more and more homes lit at evening in Jerusalem), today (a small white church on a hill today)

Hub and extras: artwork team adds the ten cards to the Bible panel on `index.html` (with NEW signs) once each deck is merged;
software team adds the ten stickers to `stickers.html`. HQ verifies and merges every deck (sweep at 1280/375, NIV quotes,
art), merging as each is ready.
