#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { URL } from "node:url";

const DEFAULT_BASE_URL = "https://www.k4nul.com";

function parseArgs(argv) {
  const options = {
    site: "_site",
    baseUrl: DEFAULT_BASE_URL,
    diagnose: [],
    http: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--site") {
      options.site = argv[++i];
    } else if (arg.startsWith("--site=")) {
      options.site = arg.slice("--site=".length);
    } else if (arg === "--base-url") {
      options.baseUrl = argv[++i];
    } else if (arg.startsWith("--base-url=")) {
      options.baseUrl = arg.slice("--base-url=".length);
    } else if (arg === "--diagnose") {
      options.diagnose.push(...String(argv[++i] || "").split(","));
    } else if (arg.startsWith("--diagnose=")) {
      options.diagnose.push(...arg.slice("--diagnose=".length).split(","));
    } else if (arg === "--http") {
      options.http = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  options.baseUrl = options.baseUrl.replace(/\/+$/, "");
  options.diagnose = options.diagnose.map((url) => url.trim()).filter(Boolean);
  return options;
}

function walkFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkFiles(fullPath));
    } else if (entry.isFile()) {
      files.push(fullPath);
    }
  }

  return files;
}

function decodeHtml(value) {
  return String(value || "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ");
}

function getAttr(tag, name) {
  const pattern = new RegExp(`\\s${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, "i");
  const match = tag.match(pattern);
  return match ? decodeHtml(match[2] || match[3] || match[4] || "") : "";
}

function getTags(html, tagName) {
  return Array.from(html.matchAll(new RegExp(`<${tagName}\\b[^>]*>`, "gi")), (match) => match[0]);
}

function getCanonicalUrls(html) {
  return getTags(html, "link")
    .filter((tag) => getAttr(tag, "rel").toLowerCase().split(/\s+/).includes("canonical"))
    .map((tag) => getAttr(tag, "href"))
    .filter(Boolean);
}

function getMetaContent(html, name) {
  const tag = getTags(html, "meta").find((candidate) => getAttr(candidate, "name").toLowerCase() === name);
  return tag ? getAttr(tag, "content") : "";
}

function getTitle(html) {
  const match = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);
  return match ? decodeHtml(match[1]).replace(/\s+/g, " ").trim() : "";
}

function stripHtml(html) {
  return decodeHtml(
    html
      .replace(/<script\b[\s\S]*?<\/script>/gi, " ")
      .replace(/<style\b[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
  ).replace(/\s+/g, " ").trim();
}

function extractMainText(html) {
  const mainMatch = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  return stripHtml(mainMatch ? mainMatch[1] : html);
}

function publicPathForFile(siteDir, file) {
  const rel = path.relative(siteDir, file).split(path.sep).join("/");
  if (rel === "index.html") {
    return "/";
  }
  if (rel.endsWith("/index.html")) {
    return `/${rel.slice(0, -"index.html".length)}`;
  }
  return `/${rel}`;
}

function publicUrlForFile(siteDir, file, baseUrl) {
  return `${baseUrl}${publicPathForFile(siteDir, file)}`;
}

function localPathForUrl(siteDir, url) {
  const parsed = new URL(url);
  const pathname = decodeURIComponent(parsed.pathname);
  const rel = pathname.replace(/^\/+/, "");

  if (pathname.endsWith("/")) {
    return path.join(siteDir, rel, "index.html");
  }

  if (path.extname(pathname)) {
    return path.join(siteDir, rel);
  }

  return path.join(siteDir, rel, "index.html");
}

function parseSitemap(siteDir) {
  const sitemapPath = path.join(siteDir, "sitemap.xml");
  if (!fs.existsSync(sitemapPath)) {
    return { path: sitemapPath, urls: [] };
  }

  const xml = fs.readFileSync(sitemapPath, "utf8");
  const urls = Array.from(xml.matchAll(/<loc>([\s\S]*?)<\/loc>/gi), (match) => decodeHtml(match[1].trim()));
  return { path: sitemapPath, urls };
}

function findInternalLinks(html) {
  return Array.from(html.matchAll(/<a\b[^>]*\shref\s*=\s*("([^"]*)"|'([^']*)')/gi), (match) =>
    decodeHtml(match[2] || match[3] || "")
  ).filter(Boolean);
}

function isHtmlDocument(html) {
  return /<html\b/i.test(html);
}

function isNoindex(html) {
  return getMetaContent(html, "robots").toLowerCase().includes("noindex");
}

function hasMetaRefresh(html) {
  return getTags(html, "meta").some(
    (tag) => getAttr(tag, "http-equiv").toLowerCase() === "refresh"
  );
}

function isPostHtml(html) {
  return /property=["']article:published_time["']/i.test(html) || /"@type"\s*:\s*"BlogPosting"/i.test(html);
}

function validateUrlSignal(url, label, errors) {
  if (/^http:\/\//i.test(url)) {
    errors.push(`${label} uses http: ${url}`);
  }
  if (/^https?:\/\/k4nul\.github\.io\b/i.test(url)) {
    errors.push(`${label} points to old GitHub Pages domain: ${url}`);
  }
  if (/^https:\/\/k4nul\.com\b/i.test(url)) {
    errors.push(`${label} points to non-www domain: ${url}`);
  }
  if (/[?&][^#]*/.test(new URL(url).search)) {
    errors.push(`${label} contains a query string: ${url}`);
  }
  if (/\/index\.html(?:$|[?#])/i.test(url)) {
    errors.push(`${label} points to an index.html URL instead of the public directory URL: ${url}`);
  }
}

function shortList(items, limit = 4) {
  if (items.length <= limit) {
    return items.join(", ");
  }
  return `${items.slice(0, limit).join(", ")} (+${items.length - limit} more)`;
}

function addDuplicateWarnings(kind, map, warnings) {
  for (const [value, urls] of map.entries()) {
    if (!value || urls.length < 2) {
      continue;
    }
    warnings.push(`Duplicate ${kind}: "${value.slice(0, 120)}" on ${shortList(urls)}`);
  }
}

async function fetchHead(url) {
  try {
    const response = await fetch(url, {
      method: "HEAD",
      redirect: "manual",
    });

    return {
      status: response.status,
      location: response.headers.get("location") || "",
    };
  } catch (error) {
    return {
      status: "error",
      location: error.message,
    };
  }
}

function printDiagnostic(url, page, inSitemap, httpStatus) {
  console.log("");
  console.log(`Diagnostic: ${url}`);
  if (httpStatus) {
    const suffix = httpStatus.location ? ` -> ${httpStatus.location}` : "";
    console.log(`  httpStatus: ${httpStatus.status}${suffix}`);
  }
  if (!page) {
    console.log("  localStatus: 404 (no generated file for this URL)");
    return;
  }

  console.log("  localStatus: 200");
  console.log(`  canonical: ${page.canonicals[0] || "(missing)"}`);
  console.log(`  noindex: ${page.noindex ? "yes" : "no"}`);
  console.log(`  title: ${page.title || "(missing)"}`);
  console.log(`  descriptionLength: ${page.description.length}`);
  console.log(`  textLength: ${page.textLength}`);
  console.log(`  inSitemap: ${inSitemap ? "yes" : "no"}`);
  console.log(`  structuredDataBlocks: ${page.structuredDataBlocks}`);
  console.log(`  brokenInternalLinks: ${page.brokenLinks.length}`);
}

async function main() {
  const options = parseArgs(process.argv);
  const siteDir = path.resolve(options.site);
  const base = new URL(`${options.baseUrl}/`);
  const errors = [];
  const warnings = [];

  if (!fs.existsSync(siteDir)) {
    throw new Error(`Site directory does not exist: ${siteDir}`);
  }

  const sitemap = parseSitemap(siteDir);
  const sitemapUrls = new Set(sitemap.urls);
  const htmlFiles = walkFiles(siteDir).filter((file) => file.toLowerCase().endsWith(".html"));
  const pageByUrl = new Map();
  const titleMap = new Map();
  const descriptionMap = new Map();

  const forbiddenReference = /(https?:\/\/k4nul\.github\.io\b|http:\/\/www\.k4nul\.com\b|https?:\/\/k4nul\.com\b)/i;

  const robotsPath = path.join(siteDir, "robots.txt");
  if (!fs.existsSync(robotsPath)) {
    errors.push("robots.txt is missing from generated site");
  } else {
    const robots = fs.readFileSync(robotsPath, "utf8");
    if (/^\s*Disallow:\s*\/\s*$/im.test(robots)) {
      errors.push("robots.txt blocks the whole site with Disallow: /");
    }
    if (!robots.includes(`Sitemap: ${options.baseUrl}/sitemap.xml`)) {
      errors.push(`robots.txt does not advertise ${options.baseUrl}/sitemap.xml`);
    }
  }

  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, "utf8");
    if (!isHtmlDocument(html)) {
      continue;
    }

    const publicUrl = publicUrlForFile(siteDir, file, options.baseUrl);
    const noindex = isNoindex(html);
    const canonicals = getCanonicalUrls(html);
    const title = getTitle(html);
    const description = getMetaContent(html, "description").trim();
    const textLength = extractMainText(html).length;
    const brokenLinks = [];
    let structuredDataBlocks = 0;

    pageByUrl.set(publicUrl, {
      file,
      publicUrl,
      noindex,
      canonicals,
      title,
      description,
      textLength,
      brokenLinks,
      structuredDataBlocks,
    });

    if (forbiddenReference.test(html)) {
      errors.push(`Generated HTML contains an old or non-canonical domain reference: ${path.relative(siteDir, file)}`);
    }

    if (canonicals.length !== 1 && !noindex) {
      errors.push(`Indexable page must emit exactly one canonical: ${publicUrl} (${canonicals.length} found)`);
    }
    if (canonicals.length > 1) {
      errors.push(`Page emits multiple canonical tags: ${publicUrl}`);
    }

    if (canonicals[0]) {
      try {
        validateUrlSignal(canonicals[0], `Canonical for ${publicUrl}`, errors);
      } catch {
        errors.push(`Canonical is not a valid URL for ${publicUrl}: ${canonicals[0]}`);
      }

      if (!noindex && canonicals[0] !== publicUrl) {
        errors.push(`Indexable page has a canonical mismatch: ${publicUrl} -> ${canonicals[0]}`);
      }
    }

    if (isPostHtml(html) && noindex) {
      errors.push(`Post page has noindex: ${publicUrl}`);
    }

    if (!noindex && canonicals[0] === publicUrl && !sitemapUrls.has(publicUrl)) {
      errors.push(`Indexable self-canonical page is missing from sitemap: ${publicUrl}`);
    }

    if (!noindex && !description) {
      errors.push(`Indexable page is missing a meta description: ${publicUrl}`);
    }

    if (!noindex && textLength < 300) {
      warnings.push(`Very thin indexable page candidate (${textLength} chars): ${publicUrl}`);
    }

    for (const match of html.matchAll(/<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
      structuredDataBlocks += 1;
      try {
        JSON.parse(match[1].trim());
      } catch (error) {
        errors.push(`Invalid JSON-LD on ${publicUrl}: ${error.message}`);
      }
    }
    pageByUrl.get(publicUrl).structuredDataBlocks = structuredDataBlocks;

    for (const href of findInternalLinks(html)) {
      if (/^(#|mailto:|tel:|javascript:)/i.test(href)) {
        continue;
      }

      let parsed;
      try {
        parsed = new URL(href, publicUrl);
      } catch {
        warnings.push(`Unparseable link on ${publicUrl}: ${href}`);
        continue;
      }

      if (parsed.origin !== base.origin) {
        continue;
      }

      if (parsed.search && parsed.pathname !== "/search/" && parsed.pathname !== "/en/search/") {
        warnings.push(`Internal link contains a query string on ${publicUrl}: ${parsed.href}`);
      }

      const localPath = localPathForUrl(siteDir, parsed.href);
      if (!fs.existsSync(localPath)) {
        brokenLinks.push(parsed.href);
      }
    }

    if (brokenLinks.length > 0) {
      errors.push(`Broken internal links on ${publicUrl}: ${shortList([...new Set(brokenLinks)])}`);
    }

    if (!noindex) {
      const titles = titleMap.get(title) || [];
      titles.push(publicUrl);
      titleMap.set(title, titles);

      const descriptions = descriptionMap.get(description) || [];
      descriptions.push(publicUrl);
      descriptionMap.set(description, descriptions);
    }
  }

  for (const url of sitemap.urls) {
    if (!url.startsWith(`${options.baseUrl}/`)) {
      errors.push(`Sitemap URL is not under ${options.baseUrl}: ${url}`);
    }

    try {
      validateUrlSignal(url, `Sitemap URL`, errors);
    } catch {
      errors.push(`Sitemap contains an invalid URL: ${url}`);
      continue;
    }

    if (/\/(?:feed\.xml|search\/|en\/search\/)(?:$|[?#])/i.test(url)) {
      errors.push(`Sitemap contains utility/search/feed URL: ${url}`);
    }

    const localPath = localPathForUrl(siteDir, url);
    if (!fs.existsSync(localPath)) {
      errors.push(`Sitemap URL has no generated local file: ${url}`);
      continue;
    }

    if (localPath.toLowerCase().endsWith(".html")) {
      const html = fs.readFileSync(localPath, "utf8");
      if (isHtmlDocument(html)) {
        if (isNoindex(html)) {
          errors.push(`Sitemap contains a noindex page: ${url}`);
        }
        if (hasMetaRefresh(html)) {
          errors.push(`Sitemap contains a client-side redirect page: ${url}`);
        }
        const canonicals = getCanonicalUrls(html);
        if (canonicals[0] && canonicals[0] !== url) {
          errors.push(`Sitemap URL does not match page canonical: ${url} -> ${canonicals[0]}`);
        }
      }
    }
  }

  if (sitemap.urls.length !== sitemapUrls.size) {
    errors.push("Sitemap contains duplicate URLs");
  }

  addDuplicateWarnings("title", titleMap, warnings);
  addDuplicateWarnings("meta description", descriptionMap, warnings);

  for (const rawUrl of options.diagnose) {
    let url;
    try {
      url = new URL(rawUrl, options.baseUrl).href;
    } catch {
      warnings.push(`Could not diagnose unparseable URL: ${rawUrl}`);
      continue;
    }

    const localPath = localPathForUrl(siteDir, url);
    const publicUrl = fs.existsSync(localPath) ? publicUrlForFile(siteDir, localPath, options.baseUrl) : url;
    const httpStatus = options.http ? await fetchHead(url) : null;
    printDiagnostic(url, pageByUrl.get(publicUrl), sitemapUrls.has(publicUrl), httpStatus);
  }

  console.log("");
  console.log(`SEO audit checked ${pageByUrl.size} HTML documents and ${sitemap.urls.length} sitemap URLs.`);

  if (warnings.length > 0) {
    console.log("");
    console.log(`Warnings (${warnings.length}):`);
    for (const warning of warnings.slice(0, 40)) {
      console.log(`- ${warning}`);
    }
    if (warnings.length > 40) {
      console.log(`- ... ${warnings.length - 40} more warnings omitted`);
    }
  }

  if (errors.length > 0) {
    console.log("");
    console.log(`Errors (${errors.length}):`);
    for (const error of errors) {
      console.log(`- ${error}`);
    }
    process.exitCode = 1;
    return;
  }

  console.log("");
  console.log("SEO audit passed.");
}

try {
  await main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
