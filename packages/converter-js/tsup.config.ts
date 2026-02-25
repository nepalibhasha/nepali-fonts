import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs", "iife"],
  globalName: "NepaliConverter",
  dts: true,
  clean: true,
  sourcemap: true,
});
