import { describe, expect, it } from "vitest";

import { detectFont } from "../src/detector";

describe("detector", () => {
  it("returns null for unicode nepali", () => {
    expect(detectFont("नेपाल")).toBeNull();
  });

  it("returns null for english", () => {
    expect(detectFont("Hello World")).toBeNull();
  });

  it("returns null for empty and whitespace", () => {
    expect(detectFont("")).toBeNull();
    expect(detectFont("   ")).toBeNull();
  });

  it("returns null for plain numbers", () => {
    expect(detectFont("12345")).toBeNull();
  });

  it("detects preeti with structural specials", () => {
    expect(detectFont("g]kfn sf7df08\"")).toBe("preeti");
  });

  it("detects preeti with non-ascii legacy chars", () => {
    expect(detectFont("6]\u00abS;")).toBe("preeti");
  });

  it("detects sagarmatha with unique signatures", () => {
    expect(detectFont("g]kfn \u0192")).toBe("sagarmatha");
  });
});
