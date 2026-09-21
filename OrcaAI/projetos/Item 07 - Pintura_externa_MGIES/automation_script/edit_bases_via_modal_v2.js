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

    console.log('Filling form fields inside #modal-edit-bases in browser context...');
    await page.evaluate(() => {
      // Helper function to check/select and trigger change events
      const setCheckbox = (selector, checked) => {
        const el = document.querySelector(selector);
        if (el) {
          el.checked = checked;
          el.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Checkbox ${selector} set to ${checked}`);
        } else {
          console.log(`Checkbox ${selector} not found`);
        }
      };

      const setSelect = (selector, value) => {
        const el = document.querySelector(selector);
        if (el) {
          el.value = value;
          el.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Select ${selector} set to ${value}`);
        } else {
          console.log(`Select ${selector} not found`);
        }
      };

      // Open the modal
      const modalLink = document.querySelector('a[href="#modal-edit-bases"]');
      if (modalLink) modalLink.click();

      // Configure SINAPI (ES) 02/2026
      setCheckbox('#SINAPI_exibir_relatorio', true);
      setSelect('#SINAPI_estado', 'ES');
      setSelect('#SINAPI_data', '02/2026');

      // Configure IOPES (ES) 12/2025
      setCheckbox('#IOPES_exibir_relatorio', true);
      setSelect('#IOPES_data', '12/2025');

      // Configure ORSE (SE) 12/2025
      setCheckbox('#ORSE_exibir_relatorio', true);
      setSelect('#ORSE_data', '12/2025');

      // Configure EMOP (RJ) 02/2026
      setCheckbox('#EMOP_exibir_relatorio', true);
      setSelect('#EMOP_data', '02/2026');

      // Configure SBC (ES) 03/2026
      setCheckbox('#SBC_exibir_relatorio', true);
      setSelect('#SBC_estado', 'VTA');
      setSelect('#SBC_data', '03/2026');
    });

    // Wait 1.5 seconds for UI events
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Clicking the submit button and waiting 10 seconds...');
    await page.click('#submit_button_bases');
    
    // Wait for page to reload/submit
    await new Promise(resolve => setTimeout(resolve, 10000));

    console.log('Current page URL after click:', page.url());
    
    // Dump text to verify active databases
    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('budget_dashboard_text_after_modal.txt', text);
    console.log('Saved budget_dashboard_text_after_modal.txt');

    // Parse the updated databases text from page
    console.log('Updated databases section:');
    const dbIndex = text.indexOf('Bancos');
    if (dbIndex !== -1) {
      console.log(text.substring(dbIndex, dbIndex + 500));
    } else {
      console.log('Could not find "Bancos" text in body');
    }

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
