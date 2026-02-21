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
          light: "#ffffff",
          lightgray: "#f3f4f6",
          gray: "#9ca3af",
          darkgray: "#374151",
          dark: "#111827",
          secondary: "#2563eb",
          tertiary: "#1d4ed8",
          highlight: "rgba(37, 99, 235, 0.15)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#0f172a",
          lightgray: "#1e293b",
          gray: "#94a3b8",
          darkgray: "#cbd5e1",
          dark: "#f1f5f9",
          secondary: "#3b82f6",
          tertiary: "#60a5fa",
          highlight: "rgba(59, 130, 246, 0.15)",
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