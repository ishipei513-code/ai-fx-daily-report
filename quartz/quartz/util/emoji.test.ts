import test, { describe } from "node:test"
import assert from "node:assert"
import { getIconCode } from "./emoji.ts"

describe("getIconCode", () => {
  test("should convert simple emoji to hex code", () => {
    assert.strictEqual(getIconCode("😀"), "1f600")
  })

  test("should handle emoji with variation selector (no ZWJ)", () => {
    // Red heart is usually \u2764\uFE0F
    assert.strictEqual(getIconCode("❤️"), "2764")
  })

  test("should handle emoji with ZWJ and variation selector", () => {
    // Rainbow flag: \uD83C\uDFF3\uFE0F\u200D\uD83C\uDF08
    assert.strictEqual(getIconCode("🏳️‍🌈"), "1f3f3-fe0f-200d-1f308")
  })

  test("should handle complex ZWJ sequence", () => {
    // Family: \uD83D\uDC68\u200D\uD83D\uDC69\u200D\uD83D\uDC67
    assert.strictEqual(getIconCode("👨‍👩‍👧"), "1f468-200d-1f469-200d-1f467")
  })

  test("should return empty string for empty input", () => {
    assert.strictEqual(getIconCode(""), "")
  })

  test("should handle non-emoji characters", () => {
    assert.strictEqual(getIconCode("a"), "61")
    assert.strictEqual(getIconCode("abc"), "61-62-63")
  })
})
