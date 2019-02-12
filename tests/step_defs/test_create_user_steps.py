from pytest_bdd import scenarios, scenario, given, when, then
from distributed_app.sender import Sender
import pytest
import time


@pytest.fixture(scope='function')
def context():
    return {}

@scenario('../features/create_user.feature', 'Create a user across distributed services')
def test_create_a_user_across_distributed_services(context):
    pass

@given('I need to create a user')
def i_need_to_create_a_user(context):
    context["username"] = "steve smith"

@when('I initiate the request')
def i_initiate_the_request(context):
    context["sender"] = Sender()
    context["transaction_id"] = context["sender"].create_user(context["username"])

@then('I should be informed when the user has been created successfully')
def i_should_be_informed_when_the_user_has_been_created_successfully(context):
    timeout = 0
    while not context["sender"].is_user_created(context["transaction_id"]) and timeout < 30:
        time.sleep(1)
        timeout = timeout + 1

    assert timeout != 30, "timeout is " + str(timeout)
