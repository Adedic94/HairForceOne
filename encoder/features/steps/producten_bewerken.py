from behave import *
from hamcrest import *
from selenium import *
from features.logging_handler import loggerDEBUG
import time

@given(u'I am on the producten page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/products")


@when(u'I click the "producten aanpassen" button')
def step_impl(context):
    context.browser.click_link_by_href("/products/aanpassen")


@then(u'I should see a "Bevestigen" button to submit my actions')
def step_impl(context):
    assert_that(context.browser.html, contains_string("+"))
    assert_that(context.browser.html, contains_string("Bevestigen"))


@given(u'I am on the producten bewerken page')
def step_impl(context):
    context.browser.visit(context.basicurl+"/products/aanpassen")

@when(u'I click on the "+" product button')
def step_impl(context):
    context.browser.click_link_by_id("add_product")

@when(u'I edit the name of the new product')
def step_impl(context):
    input_list = context.browser.find_by_text('Nieuw product')
    input_list[0]._set_value('Test Conditioner heavy')
    input_list = context.browser.find_by_text('Artikelen wijzigen')
    input_list[1]._set_value('Conditioner')


@when(u'click on the submit producten button')
def step_impl(context):
    context.browser.click_link_by_id("submit_producten")


@then(u'I should be returned to the producten page')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Producten aanpassen"))


@when(u'I click on the conditioner button')
def step_impl(context):
    context.browser.click_link_by_href("/products/conditioner")


@then(u'I should see the new conditioner in the list')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Test Conditioner heavy"))