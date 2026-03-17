import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';

test.describe('Testes de Internacionalização (i18n)', () => {
    let homePage: HomePage;

    test.beforeEach(async ({ page }) => {
        homePage = new HomePage(page);
        await homePage.navigate();
    });

    test('Deve traduzir a home para inglês corretamente e alterar o link do currículo', async () => {
        // 1. Verifica estado inicial em PT-BR
        await expect(homePage.headerSubtitle).toHaveText('QA Lead, Automatizador Cypress, Empreendedor');
        await expect(homePage.langToggleBtn).toHaveText('🇺🇸 English');
        await expect(homePage.contactNameLabel).toHaveText('Nome:');

        // O currículo inicial em PT-BR não faz download de PDF a princípio, aponta para #curriculo
        await expect(homePage.cvDownloadBtn).toHaveAttribute('href', '#curriculo');

        // 2. Aciona a troca de idioma
        await homePage.toggleLanguage();

        // 3. Verifica se as traduções para EN-US foram aplicadas
        await expect(homePage.headerSubtitle).toHaveText('Senior Quality Engineering Lead | LLM-Assisted Testing | Entrepreneur');
        await expect(homePage.langToggleBtn).toHaveText('🇧🇷 Português');
        await expect(homePage.contactNameLabel).toHaveText('Name:');

        // O currículo em EN-US deve apontar pro PDF ATS-friendly 
        await expect(homePage.cvDownloadBtn).toHaveAttribute('href', '../static/Isaias_Silva_Resume.pdf');
        await expect(homePage.cvDownloadBtn).toHaveAttribute('target', '_blank');

        // 4. Verifica persistência ao recarregar a página (localStorage guardando `en`)
        await homePage.page.reload();
        await expect(homePage.headerSubtitle).toHaveText('Senior Quality Engineering Lead | LLM-Assisted Testing | Entrepreneur');
    });

    test('Deve retornar para português após segundo clique', async () => {
        // Muda para EN
        await homePage.toggleLanguage();
        await expect(homePage.langToggleBtn).toHaveText('🇧🇷 Português');

        // Muda de volta para PT
        await homePage.toggleLanguage();
        await expect(homePage.langToggleBtn).toHaveText('🇺🇸 English');
        await expect(homePage.headerSubtitle).toHaveText('QA Lead, Automatizador Cypress, Empreendedor');
    });
});
