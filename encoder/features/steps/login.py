from behave import *
from hamcrest import *
from selenium import *
from features.logging_handler import loggerDEBUG


@given(u'the login page is in front of me')
def step_impl(context):
    context.browser.visit(context.basicurl+"/login")


@given(u'I see the text "Voer uw email adres & wachtwoord in om te loggen."')
def step_impl(context):
    assert_that(context.browser.html, contains_string("wachtwoord in om te loggen."))


@when(u'I enter email and password')
def step_impl(context):
    context.browser.fill("email", "manager@hairforce1.nl")
    context.browser.fill("password", "password")


@when(u'click on the login submit button')
def step_impl(context):
    context.browser.click_link_by_id("login_submit")


@then(u'I am succesfully logged in and received a cookie')
def step_impl(context):
    cookie_manager = context.browser.cookies.all()
    if cookie_manager['user_id'] != None and cookie_manager['session'] != None:
        pass


@when(u'I enter wrong email and password')
def step_impl(context):
    context.browser.fill("email", "fout@fout.nl")
    context.browser.fill("password", "foutpassword")


@then(u'I am redirected to the login error page')
def step_impl(context):
    pass
