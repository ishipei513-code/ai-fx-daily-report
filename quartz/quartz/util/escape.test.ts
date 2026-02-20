import test, { describe } from "node:test"
import assert from "node:assert"
import { escapeHTML, unescapeHTML } from "./escape"

describe("escapeHTML", () => {
  test("escapes basic HTML characters", () => {
    assert.strictEqual(escapeHTML("&"), "&amp;")
    assert.strictEqual(escapeHTML("<"), "&lt;")
    assert.strictEqual(escapeHTML(">"), "&gt;")
    assert.strictEqual(escapeHTML('"'), "&quot;")
    assert.strictEqual(escapeHTML("'"), "&#039;")
  })

  test("does not modify alphanumeric strings", () => {
    assert.strictEqual(escapeHTML("hello world"), "hello world")
    assert.strictEqual(escapeHTML("1234567890"), "1234567890")
  })

  test("handles mixed strings", () => {
    assert.strictEqual(escapeHTML("<b>bold</b> & 'quoted'"), "&lt;b&gt;bold&lt;/b&gt; &amp; &#039;quoted&#039;")
  })

  test("handles empty string", () => {
    assert.strictEqual(escapeHTML(""), "")
  })
})

describe("unescapeHTML", () => {
  test("unescapes basic HTML entities", () => {
    assert.strictEqual(unescapeHTML("&amp;"), "&")
    assert.strictEqual(unescapeHTML("&lt;"), "<")
    assert.strictEqual(unescapeHTML("&gt;"), ">")
    assert.strictEqual(unescapeHTML("&quot;"), '"')
    assert.strictEqual(unescapeHTML("&#039;"), "'")
  })

  test("does not modify alphanumeric strings", () => {
    assert.strictEqual(unescapeHTML("hello world"), "hello world")
  })

  test("handles mixed strings", () => {
    assert.strictEqual(unescapeHTML("&lt;b&gt;bold&lt;/b&gt; &amp; &#039;quoted&#039;"), "<b>bold</b> & 'quoted'")
  })

  test("handles empty string", () => {
    assert.strictEqual(unescapeHTML(""), "")
  })

  test("reversibility check", () => {
    const original = "<b>bold</b> & 'quoted'"
    const escaped = escapeHTML(original)
    const unescaped = unescapeHTML(escaped)
    assert.strictEqual(unescaped, original)
  })

  test("reversibility check with specific problematic input", () => {
    const original = "&lt;"
    const escaped = escapeHTML(original) // "&amp;lt;"
    const unescaped = unescapeHTML(escaped)
    // Expected: "&lt;"
    // Current (buggy): "<"
    assert.strictEqual(unescaped, original, `Failed to reverse escapeHTML("${original}")`)
  })
})
