const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER EXCEPTION:', err.toString()));

  try {
    console.log('Navigating to login page...');
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    const budgetUrl = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8';
    console.log(`Navigating to budget dashboard: ${budgetUrl}...`);
    await page.goto(budgetUrl, { waitUntil: 'networkidle2' });

    console.log('Opening modal and filling fields...');
    await page.evaluate(() => {
      const modalLink = document.querySelector('a[href="#modal-edit-bases"]');
      if (modalLink) modalLink.click();
    });

    await new Promise(resolve => setTimeout(resolve, 1000));

    await page.evaluate(() => {
      const setCheckbox = (id, checked) => {
        const el = document.getElementById(id);
        if (el) {
          el.checked = checked;
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }
      };

      const setSelect = (id, value) => {
        const el = document.getElementById(id);
        if (el) {
          el.value = value;
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }
      };

      // Configure SINAPI (ES) 02/2026
      setCheckbox('SINAPI_exibir_relatorio', true);
      setSelect('SINAPI_estado', 'ES');
      setSelect('SINAPI_data', '02/2026');

      // Configure IOPES (ES) 12/2025
      setCheckbox('IOPES_exibir_relatorio', true);
      setSelect('IOPES_data', '12/2025');

      // Configure ORSE (SE) 12/2025
      setCheckbox('ORSE_exibir_relatorio', true);
      setSelect('ORSE_data', '12/2025');

      // Configure EMOP (RJ) 02/2026
      setCheckbox('EMOP_exibir_relatorio', true);
      setSelect('EMOP_data', '02/2026');

      // Configure SBC (ES) 03/2026
      setCheckbox('SBC_exibir_relatorio', true);
      setSelect('SBC_estado', 'VTA');
      setSelect('SBC_data', '03/2026');

      // Verify immediate DOM values
      const verifyInput = (id) => {
        const el = document.getElementById(id);
        if (el) {
          console.log(`VERIFY DOM: #${id} value = "${el.value}", checked = ${el.checked}`);
        } else {
          console.log(`VERIFY DOM: #${id} NOT FOUND`);
        }
      };

      verifyInput('SINAPI_exibir_relatorio');
      verifyInput('SINAPI_estado');
      verifyInput('SINAPI_data');
      verifyInput('IOPES_exibir_relatorio');
      verifyInput('IOPES_data');
      verifyInput('ORSE_exibir_relatorio');
      verifyInput('ORSE_data');
      verifyInput('EMOP_exibir_relatorio');
      verifyInput('EMOP_data');
      verifyInput('SBC_exibir_relatorio');
      verifyInput('SBC_estado');
      verifyInput('SBC_data');
    });

    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Clicking the submit button and waiting 10 seconds...');
    await page.click('#submit_button_bases');
    
    // Wait for submission response
    await new Promise(resolve => setTimeout(resolve, 10000));

    console.log('Current page URL after click:', page.url());
    const content = await page.content();
    fs.writeFileSync('budget_dashboard_after_submit.html', content);
    console.log('Saved budget_dashboard_after_submit.html');

    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('budget_dashboard_text_after_submit.txt', text);

    // Let's check if there are any alert/flash elements
    const flashMessages = await page.evaluate(() => {
      const alerts = document.querySelectorAll('.alert, .notice, .flash, .toast-message, .alert-danger, .alert-success');
      return Array.from(alerts).map(el => el.innerText.trim());
    });
    console.log('Flash messages found:', flashMessages);

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
