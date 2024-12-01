Feature: Load testing client login endpoint
  Scenario: Test client login with random data
    Given the login endpoint is "/client_login"
    When I send random login data
    Then the response status code should be 200
