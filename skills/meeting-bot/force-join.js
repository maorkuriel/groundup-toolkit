const puppeteer = require('puppeteer');
const fs = require('fs');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    try {
        const browser = await puppeteer.launch({
            headless: true,
            executablePath: '/usr/bin/chromium-browser',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });

        const page = await browser.newPage();
        
        // Load cookies
        const path = require('path');
        const cookies = JSON.parse(fs.readFileSync(path.join(__dirname, 'google-cookies.json'), 'utf8'));
        await page.setCookie(...cookies);

        await page.goto('https://meet.google.com/xxx-xxxx-xxx', { waitUntil: 'networkidle2', timeout: 60000 });
        await sleep(5000);

        console.log('Clicking Join now button...');
        
        // Click the blue Join now button
        const clicked = await page.evaluate(() => {
            // Find button with text "Join now"
            const buttons = Array.from(document.querySelectorAll('button'));
            for (const btn of buttons) {
                if (btn.textContent.includes('Join now')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        });

        console.log('Clicked:', clicked);
        
        await sleep(10000);
        await page.screenshot({ path: '/tmp/force-joined.png' });
        
        console.log('✅ Joined! Staying in meeting...');
        await sleep(7200000);

        await browser.close();
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
