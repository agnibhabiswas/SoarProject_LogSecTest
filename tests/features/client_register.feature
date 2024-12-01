Feature: Load testing client registration endpoint
  Scenario: Test client registration with random data
    Given the registration endpoint is "/client_registeration"
    When I send random registration data
    Then the response status code should be 200
