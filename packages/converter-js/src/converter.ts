import { FONT_MAPS, SUPPORTED_FONTS } from "./maps";

const POST_RULES: [RegExp, string][] = [
  [/्ा/g, ""],
  [/(त्र|त्त)([^उभप]+?)m/g, "$1m$2"],
  [/त्रm/g, "क्र"],
  [/त्तm/g, "क्त"],
  [/([^उभप]+?)m/g, "m$1"],
  [/उm/g, "ऊ"],
  [/भm/g, "झ"],
  [/पm/g, "फ"],
  [/इ\{/g, "ई"],
  [/ि((.्)*[^्])/g, "$1ि"],
  [/(.[ािीुूृेैोौंःँ]*?)\{/g, "{$1"],
  [/((.्)*)\{/g, "{$1"],
  [/\{/g, "र्"],
  [/([ाीुूृेैोौंःँ]+?)(्(.्)*[^्])/g, "$2$1"],
  [/्([ाीुूृेैोौंःँ]+?)((.्)*[^्])/g, "्$2$1"],
  [/([ंँ])([ािीुूृेैोौः]*)/g, "$2$1"],
  [/ँँ/g, "ँ"],
  [/ंं/g, "ं"],
  [/ेे/g, "े"],
  [/ैै/g, "ै"],
  [/ुु/g, "ु"],
  [/ूू/g, "ू"],
  [/^ः/g, ":"],
  [/टृ/g, "ट्ट"],
  [/ेा/g, "ाे"],
  [/ैा/g, "ाै"],
  [/अाे/g, "ओ"],
  [/अाै/g, "औ"],
  [/अा/g, "आ"],
  [/एे/g, "ऐ"],
  [/ाे/g, "ो"],
  [/ाै/g, "ौ"],
];

export function convert(text: string, sourceFont: string): string {
  const fontKey = sourceFont.toLowerCase();
  const charMap = FONT_MAPS[fontKey];
  if (!charMap) {
    throw new Error(
      `Unknown font: ${JSON.stringify(sourceFont)}. Supported: ${SUPPORTED_FONTS.join(", ")}`
    );
  }

  const tokens = text.split(/(\s+)/);
  const out: string[] = [];

  for (const token of tokens) {
    if (!token || /^\s+$/.test(token)) {
      out.push(token);
      continue;
    }

    let mapped = "";
    for (const ch of token) {
      mapped += charMap[ch] ?? ch;
    }

    for (const [pattern, replacement] of POST_RULES) {
      mapped = mapped.replace(pattern, replacement);
    }
    out.push(mapped);
  }

  return out.join("");
}
