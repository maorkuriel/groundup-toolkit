const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/usr/bin/chromium-browser',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    const cookies = JSON.parse(fs.readFileSync('google-cookies.json'));
    await page.setCookie(...cookies);
    
    await page.goto('https://meet.google.com/xxx-xxxx-xxx', {waitUntil: 'domcontentloaded', timeout: 60000});
    
    console.log('Waiting for Join button...');
    await page.waitForFunction(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        return btns.some(b => b.textContent.includes('Join now'));
    }, {timeout: 30000});
    
    console.log('Clicking Join button...');
    await page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const joinBtn = btns.find(b => b.textContent.includes('Join now'));
        joinBtn.click();
    });
    
    console.log('Waiting 20 seconds...');
    await new Promise(r => setTimeout(r, 20000));
    await page.screenshot({path: '/tmp/actually-joined.png'});
    
    console.log('✅ CLICKED JOIN! Staying 2 hours...');
    await new Promise(r => setTimeout(r, 7200000));
    await browser.close();
})().catch(console.error);
