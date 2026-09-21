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

    await new Promise(resolve => setTimeout(resolve, 1500));

    await page.evaluate(() => {
      const clickCheckbox = (id, check) => {
        const el = document.getElementById(id);
        if (el) {
          if (el.checked !== check) {
            el.click();
            console.log(`Clicked checkbox #${id} to set it to ${check}`);
          } else {
            console.log(`Checkbox #${id} was already ${check}`);
          }
        } else {
          console.log(`Checkbox #${id} NOT FOUND`);
        }
      };

      const setSelect = (id, value) => {
        const el = document.getElementById(id);
        if (el) {
          el.value = value;
          el.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Select #${id} set to ${value}`);
        } else {
          console.log(`Select #${id} NOT FOUND`);
        }
      };

      // Check SINAPI (should be checked)
      clickCheckbox('SINAPI_exibir_relatorio', true);
      setSelect('SINAPI_estado', 'ES');
      setSelect('SINAPI_data', '02/2026');

      // Check IOPES (should be checked)
      clickCheckbox('IOPES_exibir_relatorio', true);
      setSelect('IOPES_data', '12/2025');

      // Check ORSE
      clickCheckbox('ORSE_exibir_relatorio', true);
      setSelect('ORSE_data', '12/2025');

      // Check EMOP
      clickCheckbox('EMOP_exibir_relatorio', true);
      setSelect('EMOP_data', '02/2026');

      // Check SBC
      clickCheckbox('SBC_exibir_relatorio', true);
      setSelect('SBC_estado', 'VTA');
      setSelect('SBC_data', '03/2026');

      // Let's also check if updating comps radio is checked
      // Select "radio_false" to only update prices, or "radio_true"
      const radio = document.getElementById('radio_false');
      if (radio && !radio.checked) {
        radio.click();
        console.log('Clicked radio_false');
      }
    });

    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Clicking submit button...');
    await page.click('#submit_button_bases');
    
    // Wait for submission response
    await new Promise(resolve => setTimeout(resolve, 10000));

    console.log('Current page URL after click:', page.url());
    const content = await page.content();
    fs.writeFileSync('budget_dashboard_after_submit_v4.html', content);
    console.log('Saved budget_dashboard_after_submit_v4.html');

    const text = await page.evaluate(() => document.body.innerText);
    
    console.log('Updated active databases table:');
    const pos = text.indexOf('Bancos');
    if (pos !== -1) {
      console.log(text.substring(pos, pos + 500));
    } else {
      console.log('Bancos section not found in page text');
    }

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
