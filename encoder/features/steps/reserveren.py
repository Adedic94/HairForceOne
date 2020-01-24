from behave import *
from hamcrest import *
from selenium import *
import time

# use_step_matcher("re")

@given(u'the reserveren page is in front of me')
def step_impl(context):
    context.browser.visit(context.basicurl+"/reserveren/submit")


@given(u'I see the text "Selecteer een dienst"')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Selecteer een dienst"))

@when(u'date is selected {date} in the date picker')
def step_impl(context, date):
    context.browser.find_link_by_text(date).first.click()

@when(u'dienst is selected {dienst}')
def step_impl(context, dienst):
    context.browser.select("dienst_dropdown", dienst)

@when(u'medewerker is selected {medewerker}')
def step_impl(context, medewerker):
    context.browser.select("medewerker_dropdown", medewerker)


@when(u'tijdslot is selected {tijdslot}')
def step_impl(context, tijdslot):
    time.sleep(2)
    context.browser.select_by_text("tijdslot", tijdslot)


@when(u'I fill in my voornaam {voornaam}, {achternaam}, {email}, {telefoonnummer}')
def step_impl(context, voornaam, achternaam, email, telefoonnummer):
    context.browser.fill("voornaam", voornaam)
    context.browser.fill("achternaam", achternaam)
    context.browser.fill("email", email)
    context.browser.fill("telefoon", telefoonnummer)


@when(u'I click on the submit button')
def step_impl(context):
    context.browser.click_link_by_id("reserveren_submit")


@then(u'I see a confirmation message of my reservation with {dienst} and {tijdslot}')
def step_impl(context, dienst, tijdslot):
    assert_that(context.browser.html, contains_string(dienst))
    assert_that(context.browser.html, contains_string(tijdslot))
    assert_that(context.browser.html, contains_string("Bedankt voor het reserveren"))

@then(u'name not filled in error should be shown')
def step_impl(context):
    time.sleep(3)
    assert_that(context.browser.html, contains_string("Geen voornaam ingevoerd"))
    assert_that(context.browser.html, contains_string("Geen achternaam ingevoerd"))


@then(u'email not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen email ingevoerd"))


@then(u'telefoonnummer not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen telefoonnummer ingevoerd"))

@then(u'tijdslot not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen tijdslot geselecteerd"))


@then(u'date not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen datum geselecteerd"))


@then(u'medewerker not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen medewerker geselecteerd"))


@then(u'dienst not filled in error should be shown')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Geen dienst geselecteerd"))


    
    
