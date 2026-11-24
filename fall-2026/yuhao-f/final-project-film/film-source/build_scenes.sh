#!/usr/bin/env bash
# scenes.py = the show-tell kit (pasted, never imported: Gate A copies only scenes.py) + this film's body.
cd "$(dirname "$0")" && ART_HOME="${ART_HOME:-$(cd ../.. && pwd)}" && cat "$ART_HOME/skills/make/show-tell/templates/iso_kit.py" scene_body.py > scenes.py
