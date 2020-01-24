Feature: Login met email en wachtwoord

    Als manager wil ik kunnen inloggen, vervolgens wil ik
    op de home pagina extra knoppen zien waarmee ik manager
    functionaliteiten kan uitvoeren.
    
  Scenario: Log in
    Given the login page is in front of me
    And I see the text "Voer uw email adres & wachtwoord in om te loggen."
    When I enter email and password
    And click on the login submit button
    Then I am succesfully logged in and received a cookie

  Scenario: Log in faal
    Given the login page is in front of me
    And I see the text "Voer uw email adres & wachtwoord in om te loggen."
    When I enter wrong email and password
    And click on the login submit button
    Then I am redirected to the login error page