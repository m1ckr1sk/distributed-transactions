Feature: Create a user
    Create a user with confirmation of creation over multiple services

    Scenario: Create a user across distributed services
        Given I need to create a user
        When I initiate the request
        Then I should be informed when the user has been created successfully
