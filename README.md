# necatimert_meric_test

For the load testing scenarios, I did not automate SQL injection scenarios as the website actively blocked such attempts.

To execute the load test scenarios:

- Import the .jmx file into JMeter.

- Download Selenium 4.x (Java bindings) and copy the .jar files into the jmeter/lib folder.

- Install the JMeter Plugin Manager:

- Copy the Plugin Manager into the /lib/ext folder.

- Use the Plugin Manager to install the Selenium/WebDriver Support plugin.

- Download the Firefox driver (geckodriver) and configure its path in the Firefox Driver Config element.

- Link the .csv file to the CSV Data Set Config in the test plan.

- Restart JMeter to apply all changes.
