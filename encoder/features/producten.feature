Feature: Bekijk artikelgroepen en artikelen

    Als gebruiker wil ik de artikelgroepen kunnen bekijken
    op de producten pagina. En dan wil ik van ieder artikelgroep
    de bijbehorende artikelen zien.
    
  Scenario: bekijk de artikelgroepen en bijbehorende artikelen
    Given the products page is in front of me
    And I see the text "Producten"
    When I click on shampoo artikelgroep
    Then all shampoo articles are visible.