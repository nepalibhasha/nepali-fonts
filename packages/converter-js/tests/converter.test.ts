import { describe, expect, it } from "vitest";

import { convert } from "../src/converter";
import { SUPPORTED_FONTS } from "../src/maps";

describe("converter", () => {
  it("throws for unknown font", () => {
    expect(() => convert("hello", "comic_sans")).toThrow(/Unknown font/);
  });

  for (const font of SUPPORTED_FONTS) {
    it(`handles empty string for ${font}`, () => {
      expect(convert("", font)).toBe("");
    });

    it(`handles whitespace for ${font}`, () => {
      expect(convert("   ", font)).toBe("   ");
    });

    it(`supports case-insensitive font names for ${font}`, () => {
      expect(() => convert("test", font.toUpperCase())).not.toThrow();
      expect(() => convert("test", font[0].toUpperCase() + font.slice(1))).not.toThrow();
    });
  }
});
