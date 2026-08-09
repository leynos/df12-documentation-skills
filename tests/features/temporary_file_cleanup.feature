Feature: Exact temporary file cleanup
  The documented workflows remove only their own Markdown artefact.

  Scenario Outline: Cleanup removes an empty temporary directory
    Given a temporary "<workflow_name>" cleanup fixture
    When the documented cleanup function runs
    Then the expected Markdown artefact is removed
    And the empty temporary directory is removed
    And parent and sibling sentinels remain

    Examples:
      | workflow_name |
      | commit        |
      | pr            |
