import test, { describe } from "node:test"
import * as assert from "node:assert"
import { escapeHTML, unescapeHTML } from "./escape"

describe("escape", () => {
  describe("escapeHTML", () => {
    test("should escape special characters", () => {
      assert.strictEqual(escapeHTML("&"), "&amp;")
      assert.strictEqual(escapeHTML("<"), "&lt;")
      assert.strictEqual(escapeHTML(">"), "&gt;")
      assert.strictEqual(escapeHTML('"'), "&quot;")
      assert.strictEqual(escapeHTML("'"), "&#039;")
    })

    test("should handle strings without special characters", () => {
      assert.strictEqual(escapeHTML("hello world"), "hello world")
      assert.strictEqual(escapeHTML("1234567890"), "1234567890")
    })

    test("should handle mixed strings", () => {
      assert.strictEqual(escapeHTML("Foo & Bar"), "Foo &amp; Bar")
      assert.strictEqual(escapeHTML("1 < 2"), "1 &lt; 2")
      assert.strictEqual(escapeHTML('He said "Hello"'), "He said &quot;Hello&quot;")
    })

    test("should handle empty string", () => {
      assert.strictEqual(escapeHTML(""), "")
    })
  })

  describe("unescapeHTML", () => {
    test("should unescape special characters", () => {
      assert.strictEqual(unescapeHTML("&amp;"), "&")
      assert.strictEqual(unescapeHTML("&lt;"), "<")
      assert.strictEqual(unescapeHTML("&gt;"), ">")
      assert.strictEqual(unescapeHTML("&quot;"), '"')
      assert.strictEqual(unescapeHTML("&#039;"), "'")
    })

    test("should handle strings without special characters", () => {
      assert.strictEqual(unescapeHTML("hello world"), "hello world")
    })

    test("should handle mixed strings", () => {
      assert.strictEqual(unescapeHTML("Foo &amp; Bar"), "Foo & Bar")
      assert.strictEqual(unescapeHTML("1 &lt; 2"), "1 < 2")
    })

    test("should handle empty string", () => {
      assert.strictEqual(unescapeHTML(""), "")
    })
  })

  describe("reversibility", () => {
    test("should be reversible for single special characters", () => {
      const chars = ["&", "<", ">", '"', "'"]
      for (const char of chars) {
        assert.strictEqual(unescapeHTML(escapeHTML(char)), char, `Failed for char: ${char}`)
      }
    })

    test("should be reversible for mixed strings", () => {
      const s = 'Foo & Bar < Baz > Quux " Quuz \''
      assert.strictEqual(unescapeHTML(escapeHTML(s)), s)
    })

    test("should be reversible for problematic cases", () => {
        // This case exposes the bug where &amp; is unescaped before &lt;
        // escapeHTML("&lt;") -> "&amp;lt;"
        // unescapeHTML("&amp;lt;") -> currently "&lt;" -> "<" (WRONG)
        // correct: "&lt;"
        const s = "&lt;"
        assert.strictEqual(unescapeHTML(escapeHTML(s)), s, `Failed for string: ${s}`)
    })
  })
})
