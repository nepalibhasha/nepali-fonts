import { CHARACTER_MAP as himalb } from "./himalb";
import { CHARACTER_MAP as kantipur } from "./kantipur";
import { CHARACTER_MAP as preeti } from "./preeti";
import { CHARACTER_MAP as sagarmatha } from "./sagarmatha";

export const FONT_MAPS: Record<string, Record<string, string>> = {
  preeti,
  kantipur,
  sagarmatha,
  himalb,
};

export const SUPPORTED_FONTS = Object.keys(FONT_MAPS);
