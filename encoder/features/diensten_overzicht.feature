Feature: Lijst met diensten

    Er moet een diensten overzicht worden getoond op deze pagina met de diensten uit de database
  
  Scenario: 
    Given I am on the home page
    And I am not logged in
    When I click the "onze behandelingen" button
    Then I should see a table with diensten and their price
    And I should not see a button with aanpassen
  
  Scenario:
    Given I am logged in
    And I am on the home page
    When I click the "onze behandelingen" button
    Then I should see a button named behandelingen aanpasen
  
  Scenario:
    Given I am logged in 
    And I am on the behandelingen page
    When I click the "aanpassen" button
    Then I should go to the aanpassen page
  
  Scenario:
    Given I am logged in 
    And I am on the behandelingen aanpassen page
    When I click the "submit" button
    Then I should see a button named behandelingen aanpasen
