#!/usr/bin/env bash
# scenes.py = the show-tell kit (pasted, never imported: Gate A copies only scenes.py) + this film's body.
# ART_HOME = your brutalist.art checkout (default: two folders up, where this film was built).
cd "$(dirname "$0")" && ART_HOME="${ART_HOME:-$(cd ../.. && pwd)}" && cat "$ART_HOME/skills/make/show-tell/templates/iso_kit.py" scene_body.py > scenes.py
