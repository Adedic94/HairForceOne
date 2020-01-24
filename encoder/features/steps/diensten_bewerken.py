from behave import *
from hamcrest import *
from selenium import *
from features.logging_handler import loggerDEBUG
import time

@given(u'I am on the diensten page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/services")


@when(u'I click the "behandelingen aanpassen" button')
def step_impl(context):
    context.browser.click_link_by_href("/services/aanpassen")


@then(u'I should see a submit button to submit my actions')
def step_impl(context):
    assert_that(context.browser.html, contains_string("+"))
    assert_that(context.browser.html, contains_string("Bevestigen"))


@given(u'I am on the diensten bewerken page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/services/aanpassen")


@when(u'I click the "+" button')
def step_impl(context):
    context.browser.click_link_by_id("add_dienst")


@when(u'edit the name of the added dienst')
def step_impl(context):
    input_list = context.browser.find_by_text('Dames Wasmassage, knippen, stylen')
    input_list[1]._set_value('just a text to see whether it is working')


@when(u'click on the submit button')
def step_impl(context):
    context.browser.click_link_by_id("submit_diensten")


@then(u'I should see the just added dienst in the list')
def step_impl(context):
    assert_that(context.browser.html, contains_string("just a text to see whether it is working"))