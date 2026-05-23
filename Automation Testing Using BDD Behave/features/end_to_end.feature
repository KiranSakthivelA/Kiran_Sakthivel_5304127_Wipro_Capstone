Feature: Lab Tests Checkout Flow
  As a user of Apollo 247
  I want to be able to book lab tests
  So that I can get health checkups done

  @e2e @labtests
  Scenario Outline: End to End Lab Test Booking
    Given I open Apollo 247 Homepage
    When I login with my mobile number
    And I wait for manual OTP entry
    And I navigate to Lab Tests Popular Health Checkup Packages
    And I apply filters "<filter1>" and "<filter2>" and Sort Low to High
    And I add package "<package_name>" to cart
    And I select Patient "<patient_name>"
    And I select Address "<address>"
    And I select Schedule "<schedule_date>" at "<schedule_time>"
    And I proceed to pay
    Then I should be on the checkout page

    Examples:
      | filter1   | filter2      | package_name             | patient_name | address | schedule_date | schedule_time |
      | Top Deals | Men's Health | Apollo Full Body Checkup | Test User    | 7A      | 22 May 2026   | 06:30 AM      |
