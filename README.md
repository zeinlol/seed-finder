# Broken Seed Finder

Find interesting places in minecraft seeds.  
Supported most of minecraft versions. You can choose needed version.

This tool search for interesting places in game.

Now support:
- show seeds where target biome is closed to spawn (Default: Badlands)

In the future:
- Look for biomes in selected area(s)
- show large amount of villages
- show broken structures (different types in one place)
- show looped structures
- etc.


#### Features:
- json output  (in the future)
## Installation

1. You need to install target Minecraft version. T-Launcher is also supported. <b style='color: red'>Snapshots supported, but can be unstable</b>
2. For communication with Minecraft this sources uses [Amidst tool](https://github.com/toolbox4minecraft/amidst). They need to be placed at `assets` folder ([download here](https://github.com/toolbox4minecraft/amidst/releases)). Some of them are added in this repo. Use this step just for updating (you can select name or full path to amidst sources).
3. Install requirements: `pip install -r requirements.txt`. Tested on Python3.9

## Using

```angular2html
  -h, --help            show this help message and exit
  -gv GAME_VERSION, --game-version GAME_VERSION
                        Minecraft version. Use --show-versions to see
                        installed. Default is 1.16.1
  -src SOURCES, --sources SOURCES
                        Amidst sources path. You can put them in assets folder
                        or specify path to file. Default: amidst-v4-7.jar
  -s [SEEDS ...], --seeds [SEEDS ...]
                        Seeds to analyze world
  -b [BIOMES ...], --biomes [BIOMES ...]
                        Search for biome name. Case doesn't matter. Can be
                        more than one. Can search by part of name. If
                        'Badlands' than search for 'Eroded Badlands',
                        'Modified Badlands Plateau'... Default is Badlands.
                        Run --show-biomes to see all possible values.
  -a AMOUNT, --amount AMOUNT
                        Amount of seeds to find. Default: infinity
  -sv, --show-versions  See installed minecraft and sources versions and exit
  -sb, --show-biomes    See possible minecraft biomes and exit
```

### Show versions
```angular2html
Installed minecraft versions:
	1.15.2
	1.16-pre8
	1.16.1
	1.16.5
	1.17-pre1
	1.18.2
	22w17a
	Fabric 1.16.1
	OptiFine 1.16.4
	OptiFine 1.16.5

Installed amidst versions:
	FULL-PATH\seed-finder\assets\amidst-v4-5-beta3.jar
	FULL-PATH\seed-finder\assets\amidst-v4-5.jar
	FULL-PATH\seed-finder\assets\amidst-v4-6.jar
	FULL-PATH\seed-finder\assets\amidst-v4-7.jar
```

### Show biomes
```angular2html
Biomes in minecraft 1.15.2:
	0: Ocean
	1: Plains
	2: Desert
	3: Mountains
	4: Forest
	...
	12: Snowy Tundra
	13: Snowy Mountains
	14: Mushroom Fields
	15: Mushroom Field Shore
	16: Beach
	...
	44: Warm Ocean
	45: Lukewarm Ocean
	46: Cold Ocean
	47: Deep Warm Ocean
	48: Deep Lukewarm Ocean
	...
	157: Dark Forest Hills
	158: Snowy Taiga Mountains
	160: Giant Spruce Taiga
	161: Giant Spruce Taiga Hills
	162: Gravelly Mountains+
	163: Shattered Savanna
	164: Shattered Savanna Plateau
	165: Eroded Badlands
	166: Modified Wooded Badlands Plateau
	167: Modified Badlands Plateau
	168: Bamboo Jungle
	169: Bamboo Jungle Hills
```