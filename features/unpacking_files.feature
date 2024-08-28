Feature: Unpacking files

  Scenario: No dxp files, default options
    Given a folder with no dxp files
    When I run the tool with default options
    Then the tool should report the error "the following arguments are required: -i/--input-file"


  Scenario: One dxp file, default options
    Given a folder with files "scripts.dxp"
    When I run the tool with default options
    Then it should create the folder "src" with the file "JavaScript/accordian.js" inside it
    And it should not create the folder "dxp_contents"
    And it should exit successfully


  Scenario: One dxp and 'pc' flag
    Given a folder with files "scripts.dxp"
    When I run the tool with arguments "-pc"
    Then it should create the folder "src" with the file "JavaScript/accordian.js" inside it
    And it should create the folder "dxp_contents" with the file "Metadata.xml" inside it
    And it should exit successfully


  Scenario: Two dxp files and 'i' flag
    Given a folder with files "scripts.dxp, no_scripts.dxp"
    When I run the tool with arguments "-i scripts.dxp"
    Then it should create the folder "src" with the file "JavaScript/accordian.js" inside it
    And it should not create the folder "dxp_contents"
    And it should exit successfully


  Scenario: One dxp file and flags 'oc' and 'pc'
    Given a folder with files "scripts.dxp"
    When I run the tool with arguments "-oc my_output -pc"
    Then it should create the folder "src" with the file "JavaScript/accordian.js" inside it
    And it should create the folder "my_output" with the file "Metadata.xml" inside it
    And it should exit successfully


  Scenario: One dxp file and 'os' flag
    Given a folder with files "scripts.dxp"
    When I run the tool with arguments "-os my_src"
    Then it should create the folder "my_src" with the file "JavaScript/accordian.js" inside it
    And it should not create the folder "dxp_contents"
    And it should exit successfully


  Scenario: One empty dxp with default options
    Given a folder with files "no_scripts.dxp"
    When I run the tool with default options
    Then it should not create the folder "src"
    And it should exit successfully
