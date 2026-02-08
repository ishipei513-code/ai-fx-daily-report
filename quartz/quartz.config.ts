import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 * https://quartz.jzhao.xyz/configuration
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "AI FX Daily Report",
    pageTitleSuffix: "",
    enableSPA: false,                  // SPAオフで静的表示を強制（Loading...対策）
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "ja-JP",
    baseUrl: "ishipei513-code.github.io/ai-fx-daily-report",
    ignorePatterns: [],
    defaultDateType: "created",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Sans JP",
        body: "Noto Sans JP",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#f5f7fa",
          lightgray: "#e5e5e5",
          gray: "#b8b8b8",
          darkgray: "#2c3e50",
          dark: "#1a252f",
          secondary: "#2980b9",
          tertiary: "#16a085",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#0b0e14",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#e0e6ed",
          secondary: "#3498db",
          tertiary: "#2ecc71",
          highlight: "rgba(52, 152, 219, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({ priority: ["frontmatter", "git", "filesystem"] }),
      Plugin.SyntaxHighlighting({ theme: { light: "github-light", dark: "github-dark" }, keepBackground: false }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [],  // RemoveDraftsオフで自動生成レポートが確実に表示
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,       // 正しいスペル（S大文字）
        enableRSS: true,
        // staticIndex: true,      // 最新版では不要（または indexStrategy: "static" に置き換え可能）
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Plugin.CustomOgImages(),  // ビルド高速化のためコメントアウト
    ],
  },
}

export default config