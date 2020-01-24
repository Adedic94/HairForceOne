from behave import *
from hamcrest import *
import time

from features.logging_handler import loggerDEBUG


@given(u'the products page is in front of me')
def step_impl(context):
    context.browser.visit(context.basicurl+"/products/")


@given(u'I see the text "Producten"')
def step_impl(context):
    assert_that(context.browser.html, contains_string("Producten"))


@when(u'I click on shampoo artikelgroep')
def step_impl(context):
    context.browser.click_link_by_href('/products/shampoo')


@then(u'all shampoo articles are visible.')
def step_impl(context):
    time.sleep(4)
    try:
        assert_that(context.browser.html, contains_string("Oribe Silverati Shampoo"))
        loggerDEBUG.debug("Shampoo zichtbaar op: " + context.browser.url)
    except:
        loggerDEBUG.error("Shampoo niet gevonden op: " + context.browser.url)

    