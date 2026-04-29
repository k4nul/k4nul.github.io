#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const DEFAULT_BASE_URL = "https://www.k4nul.com";
const DEFAULT_SITE_DIR = "_site";
const DEFAULT_TIMEOUT_MS = 15000;
const DEFAULT_CONCURRENCY = 8;

const REQUIRED_PATHS = [
  "/",
  "/security/",
  "/ai-engineering/",
  "/rust/",
  "/devops/",
  "/start-here/",
  "/about/",
  "/categories/",
  "/tags/",
  "/search/",
  "/contact/",
  "/privacy/",
  "/en/",
  "/en/about/",
  "/en/categories/",
  "/en/tags/",
  "/en/search/",
  "/en/contact/",
  "/en/privacy/",
  "/assets/css/main.css",
  "/assets/js/main.min.js",
  "/assets/images/k4nul.png",
  "/assets/images/k4nulA.png",
  "/feed.xml",
  "/sitemap.xml",
  "/robots.txt",
];

function parseArgs(argv) {
  const args = {
    baseUrl: DEFAULT_BASE_URL,
    siteDir: DEFAULT_SITE_DIR,
    mode: "local",
    jsonPath: "",
    includeRequired: true,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    concurrency: DEFAULT_CONCURRENCY,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => argv[++i];

    if (arg === "--prod") args.mode = "prod";
    else if (arg === "--local") args.mode = "local";
    else if (arg === "--no-required") args.includeRequired = false;
    else if (arg === "--base-url") args.baseUrl = next();
    else if (arg.startsWith("--base-url=")) args.baseUrl = arg.slice("--base-url=".length);
    else if (arg === "--site") args.siteDir = next();
    else if (arg.startsWith("--site=")) args.siteDir = arg.slice("--site=".length);
    else if (arg === "--json") args.jsonPath = next();
    else if (arg.startsWith("--json=")) args.jsonPath = arg.slice("--json=".length);
    else if (arg === "--timeout") args.timeoutMs = Number(next());
    else if (arg.startsWith("--timeout=")) args.timeoutMs = Number(arg.slice("--timeout=".length));
    else if (arg === "--concurrency") args.concurrency = Number(next());
    else if (arg.startsWith("--concurrency=")) args.concurrency = Number(arg.slice("--concurrency=".length));
    else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  args.baseUrl = normalizeBaseUrl(args.baseUrl);
  args.timeoutMs = Number.isFinite(args.timeoutMs) ? args.timeoutMs : DEFAULT_TIMEOUT_MS;
  args.concurrency = Number.isFinite(args.concurrency) ? args.concurrency : DEFAULT_CONCURRENCY;
  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/check-links.mjs --site _site
  node scripts/check-links.mjs --prod --base-url https://www.k4nul.com

Options:
  --local                 Check the built local _site output. This is the default.
  --prod                  Crawl the deployed sitemap and check internal HTTP targets.
  --site <dir>            Built site directory for local mode. Default: _site
  --base-url <url>        Canonical site origin. Default: https://www.k4nul.com
  --json <path>           Write the full report as JSON.
  --no-required           Do not add the repository's required smoke-test paths.
  --timeout <ms>          HTTP timeout in production mode. Default: 15000
  --concurrency <n>       HTTP concurrency in production mode. Default: 8
`);
}

function normalizeBaseUrl(raw) {
  const url = new URL(raw);
  url.pathname = "/";
  url.search = "";
  url.hash = "";
  return url.href.replace(/\/$/, "");
}

function toPosixPath(value) {
  return value.split(path.sep).join("/");
}

function listFiles(root, predicate) {
  const out = [];
  const stack = [root];

  while (stack.length > 0) {
    const current = stack.pop();
    if (!fs.existsSync(current)) continue;
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) stack.push(fullPath);
      else if (predicate(fullPath)) out.push(fullPath);
    }
  }

  return out.sort();
}

function htmlFileToUrlPath(siteDir, filePath) {
  const relative = toPosixPath(path.relative(siteDir, filePath));
  if (relative === "index.html") return "/";
  if (relative.endsWith("/index.html")) return `/${relative.slice(0, -"index.html".length)}`;
  return `/${relative}`;
}

function decodeEntities(value) {
  return value
    .replaceAll("&amp;", "&")
    .replaceAll("&quot;", "\"")
    .replaceAll("&#39;", "'")
    .replaceAll("&apos;", "'");
}

function extractRawLinks(html) {
  const links = [];
  const attrPattern = /\b(?:href|src|action)\s*=\s*(["'])(.*?)\1/gi;
  const srcsetPattern = /\bsrcset\s*=\s*(["'])(.*?)\1/gi;
  let match;

  while ((match = attrPattern.exec(html)) !== null) {
    links.push(decodeEntities(match[2].trim()));
  }

  while ((match = srcsetPattern.exec(html)) !== null) {
    for (const candidate of decodeEntities(match[2]).split(",")) {
      const urlPart = candidate.trim().split(/\s+/)[0];
      if (urlPart) links.push(urlPart);
    }
  }

  return links;
}

function isSkippedScheme(protocol) {
  return [
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
    "blob:",
    "sms:",
    "webcal:",
  ].includes(protocol);
}

function normalizeLink(rawValue, sourceUrl, baseUrl) {
  const raw = rawValue.trim();
  if (!raw || raw === "#" || raw.startsWith("#")) return { type: "skip" };

  let url;
  try {
    url = new URL(raw, sourceUrl);
  } catch {
    return { type: "invalid", raw };
  }

  if (isSkippedScheme(url.protocol)) return { type: "skip" };
  if (!["http:", "https:"].includes(url.protocol)) return { type: "skip" };

  const base = new URL(baseUrl);
  if (url.hostname !== base.hostname) {
    return { type: "external", raw, target: url.href };
  }

  url.protocol = base.protocol;
  url.host = base.host;
  url.hash = "";
  return {
    type: "internal",
    raw,
    target: normalizeTargetHref(url),
    path: url.pathname,
  };
}

function normalizeTargetHref(url) {
  url.hash = "";
  if (url.pathname !== "/" && url.pathname.endsWith("//")) {
    url.pathname = url.pathname.replace(/\/+$/, "/");
  }
  return url.href;
}

function addTarget(targets, target, source) {
  const existing = targets.get(target.target);
  if (existing) {
    existing.sources.push(source);
    return;
  }

  targets.set(target.target, {
    target: target.target,
    path: target.path,
    sources: [source],
  });
}

function addRequiredTargets(targets, baseUrl) {
  for (const requiredPath of REQUIRED_PATHS) {
    const source = {
      source: "(required path)",
      raw: requiredPath,
      kind: "required",
    };
    const target = normalizeLink(requiredPath, `${baseUrl}/`, baseUrl);
    if (target.type === "internal") addTarget(targets, target, source);
  }
}

function collectLocal(siteDir, baseUrl, includeRequired) {
  const htmlFiles = listFiles(siteDir, (filePath) => filePath.toLowerCase().endsWith(".html"));
  const targets = new Map();
  const externalTargets = new Map();
  const invalidLinks = [];
  let internalReferences = 0;
  let externalReferences = 0;

  for (const filePath of htmlFiles) {
    const sourcePath = htmlFileToUrlPath(siteDir, filePath);
    const sourceUrl = new URL(sourcePath, `${baseUrl}/`).href;
    const html = fs.readFileSync(filePath, "utf8");

    for (const raw of extractRawLinks(html)) {
      const normalized = normalizeLink(raw, sourceUrl, baseUrl);
      if (normalized.type === "internal") {
        internalReferences += 1;
        addTarget(targets, normalized, { source: sourcePath, raw, kind: "html" });
      } else if (normalized.type === "external") {
        externalReferences += 1;
        externalTargets.set(normalized.target, normalized.target);
      } else if (normalized.type === "invalid") {
        invalidLinks.push({ source: sourcePath, raw });
      }
    }
  }

  if (includeRequired) addRequiredTargets(targets, baseUrl);

  return {
    sourceCount: htmlFiles.length,
    targets,
    externalTargets,
    invalidLinks,
    internalReferences,
    externalReferences,
  };
}

function safeDecodePathname(pathname) {
  try {
    return decodeURIComponent(pathname);
  } catch {
    return pathname;
  }
}

function localPathCandidates(siteDir, pathname) {
  const decoded = safeDecodePathname(pathname);
  const clean = decoded.replace(/^\/+/, "");
  if (clean.split("/").includes("..")) return [];
  const targetPath = path.join(siteDir, clean);

  if (pathname.endsWith("/")) {
    return [{ filePath: path.join(targetPath, "index.html"), redirect: false }];
  }

  return [
    { filePath: targetPath, redirect: false },
    { filePath: path.join(targetPath, "index.html"), redirect: true },
    { filePath: `${targetPath}.html`, redirect: true },
  ];
}

function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

function checkLocalTarget(siteDir, item) {
  const url = new URL(item.target);
  for (const candidate of localPathCandidates(siteDir, url.pathname)) {
    if (fileExists(candidate.filePath)) {
      return {
        ...item,
        ok: true,
        status: candidate.redirect ? "redirect" : "ok",
        redirected: candidate.redirect,
        finalTarget: candidate.redirect && !url.pathname.endsWith("/") ? `${url.pathname}/` : url.pathname,
      };
    }
  }

  return {
    ...item,
    ok: false,
    status: "missing",
    redirected: false,
    finalTarget: "",
  };
}

async function fetchWithRedirects(url, { timeoutMs, readBody = false, maxRedirects = 10 }) {
  let current = url;
  const chain = [];

  for (let i = 0; i <= maxRedirects; i += 1) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    let response;

    try {
      response = await fetch(current, {
        redirect: "manual",
        signal: controller.signal,
        headers: {
          "user-agent": "k4nul-link-check/1.0",
          accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
      });
    } finally {
      clearTimeout(timer);
    }

    const status = response.status;
    const location = response.headers.get("location");
    const contentType = response.headers.get("content-type") || "";

    if (status >= 300 && status < 400 && location) {
      const nextUrl = new URL(location, current).href;
      chain.push({ status, from: current, to: nextUrl });
      current = nextUrl;
      continue;
    }

    return {
      status,
      ok: status >= 200 && status < 400,
      finalUrl: current,
      redirected: chain.length > 0,
      chain,
      contentType,
      text: readBody ? await response.text() : "",
    };
  }

  return {
    status: 0,
    ok: false,
    finalUrl: current,
    redirected: chain.length > 0,
    chain,
    contentType: "",
    text: "",
    error: `Too many redirects (${maxRedirects})`,
  };
}

async function mapLimit(items, limit, worker) {
  const results = new Array(items.length);
  let cursor = 0;

  async function run() {
    while (cursor < items.length) {
      const index = cursor;
      cursor += 1;
      results[index] = await worker(items[index], index);
    }
  }

  const workers = Array.from({ length: Math.min(limit, items.length) }, run);
  await Promise.all(workers);
  return results;
}

function parseSitemap(xml, baseUrl) {
  const urls = new Set();
  const base = new URL(baseUrl);
  const locPattern = /<loc>\s*([^<]+)\s*<\/loc>/gi;
  let match;

  while ((match = locPattern.exec(xml)) !== null) {
    const raw = decodeEntities(match[1].trim());
    try {
      const url = new URL(raw);
      if (url.hostname === base.hostname) {
        url.hash = "";
        urls.add(url.href);
      }
    } catch {
      // Ignore malformed sitemap entries; invalid links are reported from HTML.
    }
  }

  return [...urls].sort();
}

async function collectProd(baseUrl, includeRequired, timeoutMs, concurrency) {
  const targets = new Map();
  const externalTargets = new Map();
  const invalidLinks = [];
  let internalReferences = 0;
  let externalReferences = 0;

  const sourceUrls = new Set([`${baseUrl}/`]);
  if (includeRequired) {
    for (const requiredPath of REQUIRED_PATHS) {
      sourceUrls.add(new URL(requiredPath, `${baseUrl}/`).href);
    }
  }

  const sitemapUrl = new URL("/sitemap.xml", `${baseUrl}/`).href;
  try {
    const sitemap = await fetchWithRedirects(sitemapUrl, { timeoutMs, readBody: true });
    if (sitemap.ok) {
      for (const loc of parseSitemap(sitemap.text, baseUrl)) sourceUrls.add(loc);
    }
  } catch (error) {
    invalidLinks.push({ source: sitemapUrl, raw: String(error) });
  }

  const fetchedSources = await mapLimit([...sourceUrls].sort(), concurrency, async (sourceUrl) => {
    try {
      const result = await fetchWithRedirects(sourceUrl, { timeoutMs, readBody: true });
      return { sourceUrl, ...result };
    } catch (error) {
      return { sourceUrl, ok: false, status: 0, error: error.message || String(error), text: "", contentType: "" };
    }
  });

  for (const source of fetchedSources) {
    if (!source.ok || !source.contentType.includes("text/html")) continue;
    const sourcePath = new URL(source.sourceUrl).pathname;
    for (const raw of extractRawLinks(source.text)) {
      const normalized = normalizeLink(raw, source.sourceUrl, baseUrl);
      if (normalized.type === "internal") {
        internalReferences += 1;
        addTarget(targets, normalized, { source: sourcePath, raw, kind: "html" });
      } else if (normalized.type === "external") {
        externalReferences += 1;
        externalTargets.set(normalized.target, normalized.target);
      } else if (normalized.type === "invalid") {
        invalidLinks.push({ source: sourcePath, raw });
      }
    }
  }

  if (includeRequired) addRequiredTargets(targets, baseUrl);

  return {
    sourceCount: fetchedSources.length,
    targets,
    externalTargets,
    invalidLinks,
    internalReferences,
    externalReferences,
    sourceFetches: fetchedSources
      .filter((source) => !source.ok)
      .map((source) => ({
        source: source.sourceUrl,
        status: source.status,
        error: source.error || "",
      })),
  };
}

async function checkProdTarget(item, timeoutMs) {
  try {
    const result = await fetchWithRedirects(item.target, { timeoutMs, readBody: false });
    return {
      ...item,
      ok: result.ok,
      status: result.status,
      redirected: result.redirected,
      finalTarget: result.finalUrl,
      chain: result.chain,
      error: result.error || "",
    };
  } catch (error) {
    return {
      ...item,
      ok: false,
      status: 0,
      redirected: false,
      finalTarget: "",
      chain: [],
      error: error.message || String(error),
    };
  }
}

function conciseSources(sources) {
  const seen = new Set();
  const out = [];
  for (const source of sources) {
    const label = `${source.source} (${source.raw})`;
    if (!seen.has(label)) {
      seen.add(label);
      out.push(label);
    }
    if (out.length >= 5) break;
  }
  const extra = sources.length - out.length;
  if (extra > 0) out.push(`... ${extra} more`);
  return out;
}

function summarizeResults(mode, collection, checked) {
  const broken = checked.filter((item) => !item.ok);
  const redirected = checked.filter((item) => item.ok && item.redirected);
  const ok = checked.filter((item) => item.ok && !item.redirected);

  return {
    mode,
    sourcePages: collection.sourceCount,
    internalReferences: collection.internalReferences,
    externalReferencesSkipped: collection.externalReferences,
    externalTargetsSkipped: collection.externalTargets.size,
    uniqueTargets: checked.length,
    okTargets: ok.length,
    redirectedTargets: redirected.length,
    brokenTargets: broken.length,
    invalidLinks: collection.invalidLinks,
    sourceFetchFailures: collection.sourceFetches || [],
    broken: broken.map((item) => ({
      target: new URL(item.target).pathname + new URL(item.target).search,
      status: item.status,
      finalTarget: item.finalTarget,
      error: item.error || "",
      sources: conciseSources(item.sources),
    })),
    redirected: redirected.map((item) => ({
      target: new URL(item.target).pathname + new URL(item.target).search,
      status: item.status,
      finalTarget: item.finalTarget,
      sources: conciseSources(item.sources),
    })),
  };
}

function printReport(report) {
  console.log(`Link check mode: ${report.mode}`);
  console.log(`Source pages scanned: ${report.sourcePages}`);
  console.log(`Internal link references: ${report.internalReferences}`);
  console.log(`Unique internal targets checked: ${report.uniqueTargets}`);
  console.log(`OK targets: ${report.okTargets}`);
  console.log(`Redirected targets: ${report.redirectedTargets}`);
  console.log(`Broken targets: ${report.brokenTargets}`);
  console.log(`External references skipped: ${report.externalReferencesSkipped}`);
  console.log(`External targets skipped: ${report.externalTargetsSkipped}`);

  if (report.sourceFetchFailures.length > 0) {
    console.log("");
    console.log("Source pages that could not be fetched:");
    for (const failure of report.sourceFetchFailures.slice(0, 20)) {
      console.log(`- ${failure.source} status=${failure.status} ${failure.error}`);
    }
  }

  if (report.invalidLinks.length > 0) {
    console.log("");
    console.log("Invalid internal-looking links:");
    for (const invalid of report.invalidLinks.slice(0, 20)) {
      console.log(`- ${invalid.source}: ${invalid.raw}`);
    }
  }

  if (report.broken.length > 0) {
    console.log("");
    console.log("Broken internal targets:");
    for (const item of report.broken.slice(0, 100)) {
      const status = item.status === "missing" ? "missing" : `status=${item.status}`;
      const final = item.finalTarget ? ` final=${item.finalTarget}` : "";
      const error = item.error ? ` error=${item.error}` : "";
      console.log(`- ${item.target} ${status}${final}${error}`);
      for (const source of item.sources) console.log(`  from ${source}`);
    }
    if (report.broken.length > 100) {
      console.log(`... ${report.broken.length - 100} more broken targets`);
    }
  }

  if (report.redirected.length > 0) {
    console.log("");
    console.log("Redirected internal targets:");
    for (const item of report.redirected.slice(0, 50)) {
      console.log(`- ${item.target} -> ${item.finalTarget}`);
      for (const source of item.sources.slice(0, 2)) console.log(`  from ${source}`);
    }
    if (report.redirected.length > 50) {
      console.log(`... ${report.redirected.length - 50} more redirected targets`);
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let collection;
  let checked;

  if (args.mode === "prod") {
    collection = await collectProd(args.baseUrl, args.includeRequired, args.timeoutMs, args.concurrency);
    checked = await mapLimit([...collection.targets.values()], args.concurrency, (item) =>
      checkProdTarget(item, args.timeoutMs),
    );
  } else {
    collection = collectLocal(args.siteDir, args.baseUrl, args.includeRequired);
    checked = [...collection.targets.values()].map((item) => checkLocalTarget(args.siteDir, item));
  }

  checked.sort((a, b) => a.target.localeCompare(b.target));
  const report = summarizeResults(args.mode, collection, checked);
  printReport(report);

  if (args.jsonPath) {
    fs.writeFileSync(args.jsonPath, `${JSON.stringify(report, null, 2)}\n`);
  }

  if (report.brokenTargets > 0 || report.invalidLinks.length > 0) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
