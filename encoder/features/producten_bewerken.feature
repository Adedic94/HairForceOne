Feature: Producten bewerken

        Als manager wil ik producten kunnen bewerken. Daarna wil ik deze bewerkte producten kunnen zien op de overzichtspagina.

    Scenario: Navigeer naar de diensten bewerken pagina
        Given I am logged in
        And I am on the producten page
        When I click the "producten aanpassen" button
        Then I should see a "Bevestigen" button to submit my actions

    Scenario: Bewerk een product en submit deze
        Given I am on the producten bewerken page
        When I click on the "+" product button
        And I edit the name of the new product
        And click on the submit producten button
        Then I should be returned to the producten page

    Scenario: Check of het nieuwe product is toegevoegd
        Given I am on the producten page
        When I click on the conditioner button
        Then I should see the new conditioner in the list