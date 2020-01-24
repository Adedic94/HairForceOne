Feature: Zie gemaakte reserveringen in het reserveringen overzicht

    Wanneer er een reservering wordt gemaakt, dan moet die verschijnen in het reserveringen overzicht

Scenario Outline: Background
    Given I am logged in
    And the reserveren page is in front of me
    When dienst is selected <dienst>
    And date is selected <date> in the date picker
    And medewerker is selected <medewerker>
    And tijdslot is selected <tijdslot>
    And I fill in my voornaam <voornaam>, <achternaam>, <email>, <telefoonnummer>
    And I click on the submit button

        Examples:
        | dienst | medewerker | date | tijdslot | voornaam | achternaam | email | telefoonnummer |
        | Heren Wasmassage, knippen, stylen| Geen voorkeur | 20 | 13:00 | Bob | El Gringo | bob@elgringo.nl | 0628755472 | 


Scenario Outline: Maak een reservering aan en check deze
    Given I am on the reserveringen overzicht page
    Then the chosen tijdslot <tijdslot> should be visible
    And the chosen datum <date> should be visible
    And the chosen dienst <dienst> should be visible
    And my name <voornaam> should be visible
    
      Examples:|
      | dienst | medewerker | date | tijdslot | voornaam | achternaam | email | telefoonnummer |
      | Heren Wasmassage, knippen, stylen| Geen voorkeur | 20 | 13:00 | Bob | El Gringo | bob@elgringo.nl | 0628755472 | 

