/* 面知 设计稿 HTML → PNG 全页截图（playwright-core + 系统 Edge） */
const path = require('path');
const { chromium } = require('playwright-core');

const WORKDIR = 'C:/Users/20454/WorkBuddy/2026-08-20-09-35-19';

const TASKS = [
  {
    name: '产品功能架构图.png',
    file: 'AI面试陪练_功能架构.html',
    width: 1320,
  },
  {
    name: '产品页面设计图.png',
    file: 'AI面试陪练_线框原型预览.html',
    width: 1560,
  },
  {
    name: '产品主业务流程图.png',
    file: 'AI面试陪练_业务流程.html',
    width: 1260,
  },
];

(async () => {
  const browser = await chromium.launch({
    channel: 'msedge',
    headless: true,
    args: ['--hide-scrollbars', '--force-device-scale-factor=2'],
  });

  for (const t of TASKS) {
    const page = await browser.newPage({
      viewport: { width: t.width, height: 1000 },
      deviceScaleFactor: 2,
    });
    const url = 'file:///' + path.join(WORKDIR, t.file).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    // 等待字体与布局稳定
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(800);
    const out = path.join(WORKDIR, t.name);
    await page.screenshot({ path: out, fullPage: true });
    const dim = await page.evaluate(() => ({
      w: document.documentElement.scrollWidth,
      h: document.documentElement.scrollHeight,
    }));
    console.log(`OK  ${t.name}  page=${dim.w}x${dim.h}px -> ${out}`);
    await page.close();
  }

  await browser.close();
  console.log('DONE');
})().catch((e) => {
  console.error('FAIL:', e.message);
  process.exit(1);
});
