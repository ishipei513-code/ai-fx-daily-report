import test, { describe } from "node:test"
import assert from "node:assert"
import { capitalize, classNames } from "./lang"

describe("capitalize", () => {
  test("empty string", () => {
    assert.strictEqual(capitalize(""), "")
  })

  test("single lowercase", () => {
    assert.strictEqual(capitalize("a"), "A")
  })

  test("single uppercase", () => {
    assert.strictEqual(capitalize("A"), "A")
  })

  test("multiple lowercase", () => {
    assert.strictEqual(capitalize("abc"), "Abc")
  })

  test("mixed case", () => {
    assert.strictEqual(capitalize("aBC"), "ABC")
    assert.strictEqual(capitalize("AbC"), "AbC")
  })

  test("non-letter start", () => {
    assert.strictEqual(capitalize("123"), "123")
    assert.strictEqual(capitalize("_abc"), "_abc")
  })
})

describe("classNames", () => {
  test("no arguments", () => {
    assert.strictEqual(classNames(undefined), "")
  })

  test("only displayClass", () => {
    assert.strictEqual(classNames("mobile-only"), "mobile-only")
    assert.strictEqual(classNames("desktop-only"), "desktop-only")
  })

  test("undefined displayClass with classes", () => {
    assert.strictEqual(classNames(undefined, "class1"), "class1")
    assert.strictEqual(classNames(undefined, "class1", "class2"), "class1 class2")
  })

  test("displayClass and classes", () => {
    assert.strictEqual(classNames("mobile-only", "class1"), "class1 mobile-only")
    assert.strictEqual(classNames("desktop-only", "class1", "class2"), "class1 class2 desktop-only")
  })

  test("empty strings in classes", () => {
    // Current implementation: classes.join(" ") simply joins everything.
    // If we pass empty strings, it might result in extra spaces or empty segments.
    // Let's check current behavior.
    assert.strictEqual(classNames(undefined, ""), "")
    assert.strictEqual(classNames(undefined, "a", ""), "a ")
    assert.strictEqual(classNames(undefined, "a", "", "b"), "a  b")
  })
})
