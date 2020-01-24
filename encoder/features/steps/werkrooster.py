from behave import *
from hamcrest import *
import time

@given(u'the rooster page is in front of me')
def step_impl(context):
    context.browser.visit(context.basicurl+"/rooster/")


@given(u'I see the text "Selecteer een medewerker"')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Selecteer een medewerker"))


@when(u'I select the dropdown menu to select a medewerker')
def step_impl(context):
    context.browser.select("medewerker", "1")


@then(u'the work time schedule of the medewerker is visible.')
def step_impl(context):
    assert_that(context.browser.html, contains_string("1"))



######### Hier testen voor het aanpassen van de beschikbaarheid van een medewerker #########

@when(u'I click on the aanpassen button')
def step_impl(context):
    context.browser.click_link_by_id("aanpassen")

@when(u'I see the text "Rooster aanpassen"')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Rooster aanpassen"))

@when(u'I select the dropdown menu to select the medewerker')
def step_impl(context):
    context.browser.select("medewerker", "2")
    time.sleep(2)


@when(u'I change the beschikbaarheid field')
def step_impl(context):
    input_list = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr[1]/td[5]")
    input_list[0]._set_value("N")


@when(u'I click on the bevestiging button')
def step_impl(context):
    time.sleep(2)
    context.browser.click_link_by_id("bevestigen")
    time.sleep(3)


@when(u'I select the selected medewerker that was adjusted')
def step_impl(context):
    context.browser.select("medewerker", "2")


@then(u'the changes of the beschikbaarheid of the medewerker is visible.')
def step_impl(context):
    assert_that(context.browser.html, contains_string("2"))
