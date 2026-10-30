// Acceptance screenshots of a running 2.0 site, written as JPEG for the QA report.
//
//   PUPPETEER_ROOT=<folder with node_modules/puppeteer-core> CHROME_PATH=<chrome>
//   node capture_screens.mjs http://127.0.0.1:8069 ../qa/screenshots [quick]
//
// Every page is opened in a fresh browser context (Odoo remembers the visitor's
// last language in a cookie, which would otherwise leak between captures). Each
// capture records the viewport, whether JavaScript, reduced motion or zoom was
// applied, the number of elements wider than the viewport, the H1 (size and
// line count), the top of the first primary action and the page height, so the
// log doubles as the measurement table of the QA report.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [base, out, mode] = process.argv.slice(2);
if (!base || !out) {
  console.error('usage: node capture_screens.mjs <base-url> <output-dir> [quick]');
  process.exit(2);
}
const require = createRequire(join(process.env.PUPPETEER_ROOT || process.cwd(), 'package.json'));
const puppeteer = require('puppeteer-core');
mkdirSync(out, { recursive: true });

const LANGS = ['', 'fr', 'de', 'es', 'uk'];
const lang = (code, path) => (code ? `/${code}${path === '/' ? '' : path}` : path);
const SIZES = [[1280, 800], [1440, 900], [1920, 1080], [1024, 900], [768, 1024], [390, 844], [375, 812], [320, 800]];
const CORE = {
  home: '/',
  platform: '/platform',
  readers: '/products/readers',
  'setup-result': '/find-your-setup?role=property_manager&sites=two_to_ten&doors=six_to_twentyfive&connection=wifi&interests=cards',
  contact: '/contact?interest=project&role=property_manager&sites=two_to_ten&connection=wifi&interests=cards',
};
const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH, headless: true });
const log = [];

async function shoot(name, path, { width, height, scale = 1, js = true, motion = 'no-preference', full = false, before } = {}) {
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  await page.setJavaScriptEnabled(js);
  await page.setViewport({ width, height, deviceScaleFactor: scale });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: motion }]);
  try {
    await page.goto(base + path, { waitUntil: 'load', timeout: 60000 });
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await new Promise((resolve) => setTimeout(resolve, 600));
    if (before) await before(page);
    if (full && !js) {
      // Without JavaScript page.evaluate is unavailable: walk the page with the mouse wheel instead.
      const pageHeight = (await page.$eval('html', (el) => el.scrollHeight).catch(() => 0)) || 20000;
      for (let y = 0; y < pageHeight; y += height - 100) {
        await page.mouse.wheel({ deltaY: height - 100 });
        await new Promise((resolve) => setTimeout(resolve, 80));
      }
      await page.mouse.wheel({ deltaY: -pageHeight - height });
      await new Promise((resolve) => setTimeout(resolve, 600));
    } else if (full) {
      // Full-page captures: the product screenshots below the fold are lazy, so walk the page once,
      // wait until every image has loaded, then return to the top before the capture.
      await page.evaluate(async () => {
        const step = Math.max(400, window.innerHeight - 100);
        for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
          window.scrollTo(0, y);
          await new Promise((resolve) => setTimeout(resolve, 80));
        }
        const pending = [...document.images].filter((img) => !img.complete).map((img) => new Promise((resolve) => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        }));
        // Never wait longer than a few seconds: an image that never settles must not block the capture.
        await Promise.race([Promise.all(pending), new Promise((resolve) => setTimeout(resolve, 4000))]);
        window.scrollTo(0, 0);
      });
      await new Promise((resolve) => setTimeout(resolve, 300));
    }
    const info = await page.evaluate(() => {
      const width = document.documentElement.clientWidth;
      const overflow = [...document.querySelectorAll('body *')].filter((element) => {
        if (element.closest('.spk-table, [hidden], .visually-hidden, .hp-field, .skip, details:not([open]) > :not(summary)')) return false;
        const box = element.getBoundingClientRect();
        return box.width > 0 && (box.right > width + 0.5 || box.left < -0.5);
      }).length;
      const h1 = document.querySelector('h1');
      const button = document.querySelector('main .button, main a.button, main button.button');
      const rect = (el) => el.getBoundingClientRect();
      const h1Lines = h1 ? Math.round(rect(h1).height / parseFloat(getComputedStyle(h1).lineHeight)) : null;
      return {
        overflow,
        scrollWidth: document.documentElement.scrollWidth,
        h1: h1 ? h1.textContent.trim().replace(/\s+/g, ' ') : null,
        h1Size: h1 ? getComputedStyle(h1).fontSize : null,
        h1Lines,
        buttonTop: button ? Math.round(rect(button).top) : null,
        buttonBottom: button ? Math.round(rect(button).bottom) : null,
        buttonText: button ? button.textContent.trim() : null,
        font: document.fonts ? document.fonts.check('700 1em Manrope') : null,
        height: document.documentElement.scrollHeight,
      };
    });
    const file = join(out, `${name}.jpg`);
    await page.screenshot({ path: file, type: 'jpeg', quality: 72, fullPage: full });
    log.push({ name, path, width, height, scale, js, motion, full, ...info });
  } catch (error) {
    log.push({ name, path, width, height, error: error.message });
  }
  await context.close();
}

const quick = mode === 'quick';

// 1. The five core pages at 1440 and 390 in every language (brief §10).
for (const code of LANGS) {
  const prefix = code || 'en';
  for (const [key, path] of Object.entries(CORE)) {
    await shoot(`${prefix}-${key}-1440x900`, lang(code, path), { width: 1440, height: 900 });
    await shoot(`${prefix}-${key}-390x844`, lang(code, path), { width: 390, height: 844 });
  }
  await shoot(`${prefix}-home-1440-full`, lang(code, '/'), { width: 1440, height: 900, full: true });
  await shoot(`${prefix}-home-390-full`, lang(code, '/'), { width: 390, height: 844, full: true });
  await shoot(`${prefix}-readers-390-full`, lang(code, '/products/readers'), { width: 390, height: 844, full: true });
}
if (!quick) {
  // 2. English home, platform and contact at all eight sizes.
  for (const [width, height] of SIZES) {
    for (const key of ['home', 'platform', 'contact']) {
      await shoot(`en-${key}-${width}x${height}`, CORE[key].split('?')[0], { width, height });
    }
  }
  // 3. Longest-content cases: German and Ukrainian at 320, 768, 1024, 1280 and 1920.
  for (const code of ['de', 'uk']) {
    for (const [width, height] of [[320, 800], [768, 1024], [1024, 900], [1280, 800], [1920, 1080]]) {
      await shoot(`${code}-home-${width}x${height}`, lang(code, '/'), { width, height });
      await shoot(`${code}-readers-${width}x${height}`, lang(code, '/products/readers'), { width, height });
    }
    await shoot(`${code}-compatibility-320-full`, lang(code, '/compatibility'), { width: 320, height: 800, full: true });
    await shoot(`${code}-setup-result-390-full`, lang(code, CORE['setup-result']), { width: 390, height: 844, full: true });
  }
  // 4. States: no JavaScript, reduced motion, 200% zoom, menus, errors, long tables.
  await shoot('en-setup-no-js-390', '/find-your-setup?connection=unsure&sites=eleven_plus&interests=automation', { width: 390, height: 844, js: false, full: true });
  await shoot('en-setup-result-both-1440', '/find-your-setup?role=integrator&sites=eleven_plus&doors=twentysix_plus&connection=both&interests=cards&interests=wallets', { width: 1440, height: 900 });
  await shoot('en-contact-no-js-1440', '/contact?interest=compatibility', { width: 1440, height: 900, js: false });
  await shoot('en-readers-no-js-1440', '/products/readers', { width: 1440, height: 900, js: false, full: true });
  await shoot('en-home-reduced-motion-1440', '/', { width: 1440, height: 900, motion: 'reduce' });
  await shoot('en-platform-zoom-200', '/platform', { width: 640, height: 450, scale: 2 });
  await shoot('en-contact-zoom-200', '/contact', { width: 640, height: 450, scale: 2 });
  await shoot('en-compatibility-320-full', '/compatibility', { width: 320, height: 800, full: true });
  await shoot('en-compatibility-1440-full', '/compatibility', { width: 1440, height: 900, full: true });
  await shoot('en-contact-errors-1440', '/contact', {
    width: 1440, height: 900,
    before: async (page) => { await page.click('[data-spk-submit]'); await new Promise((resolve) => setTimeout(resolve, 300)); },
  });
  await shoot('en-menu-platform-1440', '/', {
    width: 1440, height: 900,
    before: async (page) => { await page.click('.desktop-nav details:first-of-type summary'); await new Promise((resolve) => setTimeout(resolve, 200)); },
  });
  await shoot('de-lang-menu-1440', '/de/platform', {
    width: 1440, height: 900,
    before: async (page) => { await page.click('.lang-switch summary'); await new Promise((resolve) => setTimeout(resolve, 200)); },
  });
  for (const code of ['', 'uk']) {
    await shoot(`${code || 'en'}-menu-open-390`, lang(code, '/compatibility'), {
      width: 390, height: 844,
      before: async (page) => { await page.click('.mobile-nav summary'); await new Promise((resolve) => setTimeout(resolve, 200)); },
    });
  }
  await shoot('en-guide-matter-1440-full', '/resources/matter-thread-access-control', { width: 1440, height: 900, full: true });
  await shoot('uk-guide-mifare-390-full', '/uk/resources/mifare-classic-desfire-ev3', { width: 390, height: 844, full: true });
  await shoot('en-thank-you-1440', '/thank-you', { width: 1440, height: 900 });
  await shoot('en-404-390', '/no-such-page', { width: 390, height: 844 });
}
await browser.close();
writeFileSync(join(out, 'capture-log.json'), JSON.stringify(log, null, 2));
const lines = log.map((entry) => entry.error
  ? `${entry.name}: ERROR ${entry.error}`
  : `${entry.name}: ${entry.width}x${entry.height}${entry.scale > 1 ? ' @' + entry.scale + 'x' : ''}${entry.js ? '' : ' no-JS'}${entry.motion === 'reduce' ? ' reduced-motion' : ''} overflow=${entry.overflow} scrollWidth=${entry.scrollWidth} h1=${entry.h1Size}/${entry.h1Lines} lines button=${entry.buttonTop}-${entry.buttonBottom} font=${entry.font} height=${entry.height}`);
writeFileSync(join(out, 'capture-log.txt'), lines.join('\n') + '\n');
console.log(lines.join('\n'));
