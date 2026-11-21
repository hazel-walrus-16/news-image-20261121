// news-image-20261121 entry: one picture that sums up 21 November 2026.
//
// The image itself is entry.png in this repository, drawn by draw.py from
// the day's reported news (see README.md for the stories and sources).
// This program's whole job is to hand that picture to the grader exactly
// as drawn: it checks the file is a whole PNG inside the contest limits,
// then copies it to the output directory. No network, no clock, no
// randomness, so both graded runs write identical bytes.
//
// Run outside the grader with:
//   MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1_048_576; // the gate's 1 MiB cap
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL("./entry.png", import.meta.url);
const bytes = readFileSync(source);

const isPng = PNG_MAGIC.every((b, i) => bytes[i] === b);
if (!isPng) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")} (${bytes.length} bytes)`);
