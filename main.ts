// Entry point for the news-image-20261121 submission.
//
// The artwork itself is produced ahead of time by draw.py and committed
// next to this file as entry.png. My job here is deliberately small:
// sanity-check that PNG, then deliver it untouched to the directory the
// harness points at through MAKEFUN_OUTPUT_DIR (falling back to /output).
// Nothing about the run may vary, so there is no clock, no randomness
// and no network use anywhere below.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The one file name this program knows about, both on the way in and out.
const IMAGE_NAME = "entry.png";

// Hard limits from the competition contract.
const MAX_BYTES = 1_048_576; // 1 MiB ceiling on the delivered image
const EXPECTED_SIDE = 1024; // the canvas is square: 1024 by 1024

// Every PNG stream opens with these eight bytes; anything else is not a PNG.
const PNG_SIGNATURE: readonly number[] = [
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
];

// Resolve the folder this script lives in so the sibling PNG can be found
// no matter which working directory the harness launches us from.
const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, IMAGE_NAME);

const bytes = readFileSync(sourcePath);

// --- Check 1: the file really is a PNG -------------------------------------
// Also guards the later reads: a genuine header is far longer than the
// 24 bytes we need to peek at for the dimensions.
const looksLikePng =
  bytes.length >= PNG_SIGNATURE.length &&
  PNG_SIGNATURE.every((value, index) => bytes[index] === value);
if (!looksLikePng) {
  throw new Error(
    `${IMAGE_NAME} does not start with the PNG magic bytes; refusing to deliver it.`,
  );
}

// --- Check 2: the file stays within the size budget ------------------------
if (bytes.length > MAX_BYTES) {
  throw new Error(
    `${IMAGE_NAME} weighs ${bytes.length} bytes, over the ${MAX_BYTES}-byte limit.`,
  );
}

// --- Check 3: the canvas really is 1024 by 1024 ----------------------------
// The IHDR chunk stores width and height as big-endian 32-bit integers at
// fixed offsets 16 and 20 from the start of the file.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED_SIDE || height !== EXPECTED_SIDE) {
  throw new Error(
    `${IMAGE_NAME} measures ${width}x${height}, not the required ${EXPECTED_SIDE}x${EXPECTED_SIDE}.`,
  );
}

// All checks passed: create the destination folder if it is missing and
// copy the image over byte for byte under its original name.
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(targetDir, { recursive: true });
const targetPath = join(targetDir, IMAGE_NAME);
writeFileSync(targetPath, bytes);

console.log(`Delivered ${IMAGE_NAME} (${bytes.length} bytes) to ${targetPath}`);
