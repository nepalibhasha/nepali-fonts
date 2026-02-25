const FONT_SIGNATURES: Record<string, Set<string>> = {
  preeti: new Set(["\u02c6", "\u203a", "\u00cb", "\u00cc", "\u00cd", "\u00ce"]),
  kantipur: new Set(["\u2122", "\u00c2", "\u00b5", "\u00ba", "\u00cf", "\u00f8"]),
  sagarmatha: new Set(["\u0192", "\u0160", "\u2021", "\u00b7", "\u00b8", "\u00c7", "\u00c9", "\u00de", "\u00e8"]),
  himalb: new Set(["\u00d1", "\u00e9", "\u00ed", "\u00fa"]),
};

const LEGACY_SPECIAL = new Set(["{", "}", "[", "]", "|", "\\"]);

function isDevanagari(text: string): boolean {
  for (const ch of text) {
    if ((ch >= "\u0900" && ch <= "\u097f") || (ch >= "\ua8e0" && ch <= "\ua8ff")) {
      return true;
    }
  }
  return false;
}

function hasNonAsciiLegacy(text: string): boolean {
  for (const ch of text) {
    const code = ch.charCodeAt(0);
    if (
      (code >= 0x80 && code <= 0xff) ||
      [
        0x0152, 0x0153, 0x0160, 0x0192, 0x02c6, 0x02dc, 0x2018, 0x2019, 0x201a, 0x201c, 0x201d, 0x201e, 0x2020, 0x2021, 0x2022,
        0x2026, 0x2030, 0x2039, 0x203a, 0x2122,
      ].includes(code)
    ) {
      return true;
    }
  }
  return false;
}

export function detectFont(text: string): string | null {
  if (!text || !text.trim()) {
    return null;
  }

  if (isDevanagari(text)) {
    return null;
  }

  const chars = new Set(text.split(""));
  const scores: Record<string, number> = {};
  for (const [fontName, signatures] of Object.entries(FONT_SIGNATURES)) {
    let score = 0;
    for (const ch of chars) {
      if (signatures.has(ch)) {
        score += 1;
      }
    }
    scores[fontName] = score;
  }

  let best: string | null = null;
  let bestScore = 0;
  for (const [fontName, score] of Object.entries(scores)) {
    if (score > bestScore) {
      best = fontName;
      bestScore = score;
    }
  }
  if (best && bestScore > 0) {
    return best;
  }

  if (hasNonAsciiLegacy(text)) {
    return "preeti";
  }

  let specialCount = 0;
  let nonSpace = 0;
  for (const ch of text) {
    if (!/\s/.test(ch)) {
      nonSpace += 1;
      if (LEGACY_SPECIAL.has(ch)) {
        specialCount += 1;
      }
    }
  }
  if (nonSpace > 0 && specialCount / nonSpace > 0.05) {
    return "preeti";
  }
  return null;
}
