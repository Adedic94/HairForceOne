from behave import *
from hamcrest import *
from selenium import *

@given(u'I am on the reserveringen overzicht page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/reserveringen_overzicht")

@when(u'I select a medewerker named Adlan.')
def step_impl(context):
    context.browser.select("medewerker_dropdown", "Adlan")
    
def getNumberOfRows(context):
    table = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr")
    count = 0
    for row in table:
        count +=1
    return count

@then(u'the chosen tijdslot {tijdslot} should be visible')
def step_impl(context, tijdslot):
    nr = getNumberOfRows(context)
    print(nr)
    column = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr[" + str(getNumberOfRows(context))+ "]/td[2]")
    assert_that(column["innerHTML"], contains_string(tijdslot))

@then(u'the chosen datum {datum} should be visible')
def step_impl(context, datum):
    column = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr[" + str(getNumberOfRows(context))+ "]/td[3]")
    assert_that(column["innerHTML"], contains_string(datum))


@then(u'I should see the chosen medewerker')
def step_impl(context):
    column = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr[" + str(getNumberOfRows(context))+ "]/td[4]")
    assert_that(column["innerHTML"], contains_string("Adlan"))


@then(u'the chosen dienst {dienst} should be visible')
def step_impl(context, dienst):
    column = context.browser.find_by_xpath("/html/body/div[2]/table/tbody/tr[" + str(getNumberOfRows(context))+ "]/td[5]")
    assert_that(context.browser.html, contains_string(dienst))

@then(u'my name {voornaam} should be visible')
def step_impl(context, voornaam):
    assert_that(context.browser.html, contains_string(voornaam))