const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  try {
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    const budgetUrl = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8';
    await page.goto(budgetUrl, { waitUntil: 'networkidle2' });

    await page.evaluate(() => {
      const modalLink = document.querySelector('a[href="#modal-edit-bases"]');
      if (modalLink) modalLink.click();
    });
    await new Promise(resolve => setTimeout(resolve, 1000));

    const properties = await page.evaluate(() => {
      const check = (id) => {
        const el = document.getElementById(id);
        if (el) {
          return {
            id,
            disabled: el.disabled,
            visible: el.offsetWidth > 0 || el.offsetHeight > 0,
            checked: el.checked,
            value: el.value
          };
        }
        return { id, error: 'not found' };
      };
      return [
        check('SINAPI_exibir_relatorio'),
        check('IOPES_exibir_relatorio'),
        check('ORSE_exibir_relatorio'),
        check('EMOP_exibir_relatorio'),
        check('SBC_exibir_relatorio')
      ];
    });

    console.log('Database checkboxes properties in modal:');
    console.log(JSON.stringify(properties, null, 2));

  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
