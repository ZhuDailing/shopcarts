"""
Shopcart Steps
Steps file for shopcarts.feature
"""

from os import getenv
import json
import requests
from behave import *
import time
@when(u'I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.driver.find_element_by_id('app-js').text

@then(u'I should see "{user_id}" in the results')
def step_impl(context, user_id):
    row = 'shopcart-' + user_id + '-row'
    assert user_id in context.driver.find_element_by_id( row).text

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.driver.find_element_by_id('app-js').text

# CREATE SHOPCART
@when(u'I set the Shopcart "{user_id}" to "{value}"')
def step_impl(context, user_id, value):
    element = context.driver.find_element_by_id(user_id)
    element.clear()
    element.send_keys(value)

@when(u'I click the "Add Products" button')
def step_impl(context):
    context.driver.find_element_by_id('toggle-products').click()

@when(u'I add "{value}" of Product "{product_id}" to the cart')
def step_impl(context, value, product_id):
    select_element = context.driver.find_element_by_id('product-' + product_id + '-select')
    for option in select_element.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == value:
            option.click()
            break

@when(u'I click the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then(u'I should see Shopcart "{id}" in the results')
def step_impl(context, id):
    element_id = 'shopcart-' + id + '-row'
    assert context.driver.find_element_by_id(element_id)

@then(u'I should not see "{error}" in the form')
def step_impl(context, error):
    assert not context.driver.find_element_by_id('form-error').text == error

# DELETE SHOPCART
@given(u'the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/shopcarts/reset', headers=headers)
    assert context.resp.status_code == 204
    create_url = context.base_url + '/shopcarts'
    for row in context.table:
        data = {"user_id": row['user_id']}
        if 'product_id' in context.table.headings:
            data['products'] = {int(row['product_id']): int(row['quantity'])}

        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        assert context.resp.status_code == 201

@when(u'I visit Shopcart "{user_id}"')
def step_impl(context, user_id):
    button_id = 'view-shopcart-' + user_id
    context.driver.find_element_by_id(button_id).click()

@when(u'I delete product "{product_id}" from the cart')
def step_impl(context, product_id):
    button_id = 'product-' + product_id + "-delete"
    context.driver.find_element_by_id(button_id).click()

@then(u'I should not see Shopcart "{user_id}" in the results')
def step_impl(context, user_id):
    element = context.driver.find_element_by_id('shopcarts-table-list')
    assert not element.find_elements_by_id('shopcart-' + user_id + '-row')

@then(u'I should see "{message}" on the cart page')
def step_impl(context, message):
    parent = context.driver.find_element_by_class_name('mb-3')
    child = parent.find_element_by_class_name('card-body')
    assert message in child.text

@then(u'I should see "{value}" of Product "{product_id}" in the products list')
def step_impl(context, value, product_id):
    assert context.driver.find_element_by_id('shopcart-product-' + product_id)
    element_value = context.driver.find_element_by_id('product-' + product_id + '-quantity').get_attribute('value')
    assert value == element_value
