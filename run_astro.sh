#!/bin/bash

ORCH_DIR="orchestration"    # dossier où est le Dockerfile
SCRAPER_DIR="scraper"    # dossier scraper (relatif à ORCH_DIR)

echo "Copie du dossier scraper dans $ORCH_DIR..."
rm -rf "$ORCH_DIR/scraper"
cp -r "$SCRAPER_DIR" "$ORCH_DIR/scraper"

echo "Lancement de astro dev start dans $ORCH_DIR..."
cd "$ORCH_DIR" || exit 1
astro dev kill
astro dev stop
astro dev clean
astro dev start

echo "Nettoyage : suppression du dossier scraper copié..."
rm -rf "scraper"
