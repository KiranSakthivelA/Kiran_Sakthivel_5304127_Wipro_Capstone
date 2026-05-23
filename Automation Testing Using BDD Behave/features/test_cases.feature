Feature: Lightweight Positive and Negative Tests
  As a user of Apollo 247
  I want to interact with popular health checkups securely
  So that I can verify proper behavior

  # POSITIVE TEST CASES

  @positive @popular_packages
  Scenario: TC_POS_01 Verify Popular Health Checkup Packages page loads
    Given I navigate directly to Popular Health Checkups
    Then I verify page loaded successfully with packages

  @positive @popular_packages
  Scenario Outline: TC_POS_02 Verify Category Filter Application
    Given I navigate directly to Popular Health Checkups
    When I apply category filter "<filter_name>"
    Then I verify filter "<filter_name>" was applied

    Examples:
      | filter_name    |
      | Women's Health |

  @positive @popular_packages
  Scenario: TC_POS_03 Verify Sorting (Price: High to Low)
    Given I navigate directly to Popular Health Checkups
    When I select 'Price: High to Low' from Sort dropdown
    Then I verify sorting interaction

  @positive @popular_packages
  Scenario: TC_POS_04 Verify clicking package title opens PDP
    Given I navigate directly to Popular Health Checkups
    When I click on a package title
    Then I verify Product Description Page loaded

  # NEGATIVE TEST CASES

  @negative @authentication
  Scenario Outline: TC_NEG_01 Login fails with invalid mobile number
    Given I navigate to Homepage and open Login
    When I enter invalid mobile number "<invalid_number>"
    And I click continue
    Then I verify OTP screen does not appear

    Examples:
      | invalid_number |
      | 12345          |

  @negative @popular_packages
  Scenario Outline: TC_NEG_02 Verify invalid category filter via URL
    Given I navigate to Popular Health Checkups with Bogus Category "<bogus_category>"
    Then I verify page handles invalid category gracefully

    Examples:
      | bogus_category   |
      | BogusCategory123 |

  @negative @popular_packages
  Scenario: TC_NEG_03 Verify Duplicate Add to Cart behavior
    Given I navigate directly to Popular Health Checkups
    When I add 'Apollo Full Body Checkup' to cart
    And I attempt to add same package again from listing
    Then I verify duplicate addition is handled gracefully

  @negative @popular_packages
  Scenario: TC_NEG_04 Proceed from Cart Popup without selecting patient
    Given I navigate directly to Popular Health Checkups
    When I add 'Apollo Full Body Checkup' to cart
    And I proceed to cart popup
    And I attempt to proceed without selecting a patient
    Then I verify error or remaining on patient screen
