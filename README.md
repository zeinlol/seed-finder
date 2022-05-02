# Broken Seed Finder

Find interesting places in minecraft seeds.  
Supported most of minecraft versions. You can choose version if you want.

This tool search for interesting places in game.

Now:

- show seeds of worlds where Mesa biome is closed to spawn

In the future:
- Look for biomes in selected area(s)
- Look for different types of biomes
- show large amount of villages
- show broken structures (different types in one place)
- show looped structures
- etc.


#### Features:
- json output  (in the future)
## Installation

1. You need to install target Minecraft version. T-Launcher is also supported. <b style='color: red'>Snapshots supported, but can may be unstable</b>
2. For communication with Minecraft sources use [Amidst tool](https://github.com/toolbox4minecraft/amidst). They need to be placed at `assets` folder ([download here](https://github.com/toolbox4minecraft/amidst/releases)). Some of them are added in this repo. Use this step just for updating (you can choose one).
3. Install Python packages: `pip install -r requirements.txt`. Tested on Python3.9

## Using

```angular2html
  -h, --help            show this help message and exit
  -gv GAME_VERSION, --game-version GAME_VERSION
                        Minecraft version. Use --show-versions to see
                        installed. Default is 1.16.1
  -s SOURCES, --sources SOURCES
                        Amidst sources path. You can put them in assets folder
                        or specify path to file. Default:
                        amidst-v4-5-beta3.jar
  -a AMOUNT, --amount AMOUNT
                        Amount of seeds to find. Default: infinity
  -sv, --show-versions  See installed minecraft and sources versions and exit

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