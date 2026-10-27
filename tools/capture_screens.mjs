// Acceptance screenshots of a running 2.0 site (07: the eight viewport sizes,
// JavaScript off, reduced motion, 200% zoom), written as JPEG for the QA report.
//
//   PUPPETEER_ROOT=<folder with node_modules/puppeteer-core> CHROME_PATH=<chrome>
//   node capture_screens.mjs http://127.0.0.1:8069 ../qa/screenshots
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const [base, out] = process.argv.slice(2);
if (!base || !out) {
  console.error('usage: node capture_screens.mjs <base-url> <output-dir>');
  process.exit(2);
}
const require = createRequire(join(process.env.PUPPETEER_ROOT || process.cwd(), 'package.json'));
const puppeteer = require('puppeteer-core');
mkdirSync(out, { recursive: true });

const SIZES = [[1280, 800], [1440, 900], [1920, 1080], [1024, 900], [768, 1024], [390, 844], [375, 812], [320, 800]];
const PAGES = { home: '/', platform: '/platform', contact: '/contact' };
const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH, headless: true });
const shots = [];

async function shoot(name, path, { width, height, scale = 1, js = true, motion = 'no-preference', full = false, before } = {}) {
  const page = await browser.newPage();
  await page.setJavaScriptEnabled(js);
  await page.setViewport({ width, height, deviceScaleFactor: scale });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: motion }]);
  await page.goto(base + path, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  if (before) await before(page);
  const overflow = await page.evaluate(() => {
    const width = document.documentElement.clientWidth;
    return [...document.querySelectorAll('body *')].filter((element) => {
      if (element.closest('.spk-table, [hidden], .visually-hidden, .hp-field, .skip, details:not([open]) > :not(summary)')) return false;
      const box = element.getBoundingClientRect();
      return box.width > 0 && (box.right > width + 0.5 || box.left < -0.5);
    }).length;
  });
  const file = join(out, `${name}.jpg`);
  await page.screenshot({ path: file, type: 'jpeg', quality: 72, fullPage: full });
  shots.push(`${name}: ${width}x${height}${scale > 1 ? ' @' + scale + 'x' : ''}${js ? '' : ' no-JS'}${motion === 'reduce' ? ' reduced-motion' : ''} elements outside viewport=${overflow}`);
  await page.close();
}

for (const [width, height] of SIZES) {
  for (const [key, path] of Object.entries(PAGES)) {
    await shoot(`${key}-${width}x${height}`, path, { width, height });
  }
}
await shoot('home-1440-full', '/', { width: 1440, height: 900, full: true });
await shoot('home-390-full', '/', { width: 390, height: 844, full: true });
await shoot('setup-result-1440', '/find-your-setup?role=integrator&sites=two_to_ten&connection=cellular&interests=cards', { width: 1440, height: 900 });
await shoot('setup-no-js-390', '/find-your-setup?connection=wifi&sites=eleven_plus&interests=automation', { width: 390, height: 844, js: false, full: true });
await shoot('contact-no-js-1440', '/contact?interest=compatibility', { width: 1440, height: 900, js: false });
await shoot('readers-no-js-1440', '/products/readers', { width: 1440, height: 900, js: false, full: true });
await shoot('home-reduced-motion-1440', '/', { width: 1440, height: 900, motion: 'reduce' });
// 200% zoom: a 1280x900 window at 200% lays out like 640x450 CSS pixels.
await shoot('platform-zoom-200', '/platform', { width: 640, height: 450, scale: 2 });
await shoot('contact-zoom-200', '/contact', { width: 640, height: 450, scale: 2 });
await shoot('compatibility-320-full', '/compatibility', { width: 320, height: 800, full: true });
await shoot('contact-errors-1440', '/contact', {
  width: 1440, height: 900,
  before: async (page) => { await page.click('[data-spk-submit]'); await new Promise((resolve) => setTimeout(resolve, 300)); },
});
await shoot('menu-open-390', '/compatibility', {
  width: 390, height: 844,
  before: async (page) => { await page.click('.mobile-nav summary'); await new Promise((resolve) => setTimeout(resolve, 200)); },
});
await browser.close();
console.log(shots.join('\n'));
