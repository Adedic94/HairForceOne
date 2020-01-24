Feature: Plaats een reservering

    Als gebruiker wil ik een reservering kunnen maken.
    Vervolgens wil ik op een bevestigingspagina terecht komen.
    
  Scenario Outline: Reservering maken
    Given the reserveren page is in front of me
    And I see the text "Selecteer een dienst"
    When dienst is selected <dienst>
    And date is selected <date> in the date picker
    And medewerker is selected <medewerker>
    And tijdslot is selected <tijdslot>
    And I fill in my voornaam <voornaam>, <achternaam>, <email>, <telefoonnummer>
    And I click on the submit button
    Then I see a confirmation message of my reservation with <dienst> and <tijdslot>

    Examples:
      |                           dienst |   medewerker | date | tijdslot | voornaam | achternaam |           email | telefoonnummer |
      |Heren Wasmassage, knippen, stylen |Geen voorkeur |   20 |    13:00 |      Bob |  El Gringo | bob@elgringo.nl |     0628755472 | 

  @reserveren-geenklantengegevens
  Scenario Outline: geen klant gegevens ingevuld
    Given the reserveren page is in front of me
      And I see the text "Selecteer een dienst"
      When I click on the submit button
      Then name not filled in error should be shown
      And email not filled in error should be shown
      And telefoonnummer not filled in error should be shown
      And tijdslot not filled in error should be shown 
      And date not filled in error should be shown
      And medewerker not filled in error should be shown 
      And dienst not filled in error should be shown  

      Examples:
        |                           dienst |   medewerker | date | tijdslot | voornaam | achternaam |           email | telefoonnummer |
        |Heren Wasmassage, knippen, stylen |Geen voorkeur |   20 |    13:00 |      Bob |  El Gringo | bob@elgringo.nl |     0628755472 | 