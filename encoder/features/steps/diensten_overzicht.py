from behave import *
from hamcrest import *
from selenium import *

@given(u'I am on the home page')
def step_impl(context):
    context.browser.visit(context.basicurl)

@when(u'I click the "onze behandelingen" button')
def step_impl(context):
    context.browser.click_link_by_id("behandelingen_button")


@then(u'I should see a table with diensten and their price')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Onze behandelingen"))


@given(u'I am logged in')
def step_impl(context):
    context.browser.visit(context.basicurl+"/login")
    context.browser.fill("email", "manager@hairforce1.nl")
    context.browser.fill("password", "password")
    context.browser.click_link_by_id("login_submit")


@then(u'I should see a button named behandelingen aanpasen')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Behadelingen aanpassen"))


@given(u'I am on the behandelingen page')
def step_impl(context):
    context.browser.visit(context.basicurl + '/services/')

@when(u'I click the "aanpassen" button')
def step_impl(context):
    context.browser.click_link_by_id("behandelingen_aanpassen")

@then(u'I should not see a button with aanpassen')
def step_impl(context):
    assert_that(context.browser.html, not(contains_string("Behadelingen aanpassen")))

@then(u'I should go to the aanpassen page')
def step_impl(context):
    assert_that(context.browser.html, contains_string("contenteditable"))

@given(u'I am not logged in')
def step_impl(context):
    assert_that(context.browser.html, contains_string("login"))

@given(u'I am on the behandelingen aanpassen page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/services/aanpassen")


@when(u'I click the "submit" button')
def step_impl(context):
    context.browser.click_link_by_id("submit_diensten")