Feature: Bekijk en wijzig de werkrooster op de rooster pagina

    Als manager wil ik de rooster pagina bezoeken. 
    Dan wil ik een medewerker selecter om vervolgens zijn
    werktijden te kunnen bekijken. Ook wil ik de beschikbaarheid
    kunnen wijzigen.

  Background:
    Given I am logged in
    
  Scenario: Bekijk werkrooster van medewerker
    Given the rooster page is in front of me
    And I see the text "Selecteer een medewerker"
    When I select the dropdown menu to select a medewerker
    Then the work time schedule of the medewerker is visible.
  
  @wijzigen-werkrooster
  Scenario: wijzig beschikbaarheid van werkrooster
    Given the rooster page is in front of me
    And I see the text "Selecteer een medewerker"
    When I click on the aanpassen button
    And I see the text "Rooster aanpassen" 
    And I select the dropdown menu to select the medewerker
    And I change the beschikbaarheid field
    When I click on the bevestiging button
    And I select the selected medewerker that was adjusted
    Then the changes of the beschikbaarheid of the medewerker is visible.