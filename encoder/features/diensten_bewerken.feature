Feature: Diensten bewerken

        Als manager wil ik diensten kunnen bewerken. Daarna wil ik deze bewerkte diensten kunnen zien op de overzichtspagina.

    Scenario: Navigeer naar de diensten bewerken pagina
        Given I am logged in
        And I am on the diensten page
        When I click the "behandelingen aanpassen" button
        Then I should see a submit button to submit my actions

    Scenario: Bewerk een dienst en submit deze
        Given I am on the diensten bewerken page
        When I click the "+" button
        And edit the name of the added dienst
        And click on the submit button
        Then I should see the just added dienst in the list