#!/bin/bash
# usage: run_wheel.sh WORKDIR part...   (parts: axle ringsleeve sun planets carrierA carrierB hub cover tyre bought all)
W=$1; shift
for p in "$@"; do
  echo "== $p"; timeout 500 solidcraft-cli run $W/$p.json --out exports/stl/wheel/$p.stl --out exports/step/wheel_$p.step 2>&1 | tail -4
done
