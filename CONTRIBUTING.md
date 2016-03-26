# Contributing

Pull requests are an important part of improving Adapt and making it easier for people to adopt. We\'re 
constantly striving to better the code and the documentation, and gladly welcome input from the community.
In order to keep the quality of Adapt high, we have a few guidelines for changes.

## Getting Started
 * Set up your environment
As described in our README, set up your development environment. We use virtualenv and virtualenvwrapper, tools that are available for all platforms.

To ensure your environment is set up properly, install requirements.txt as well as test-requirements.txt, then attempt to run the existing unit tests with the following command:

```
PYTHONPATH=. python run_tests.py
```

 * Submit a ticket for your issue, assuming one doesn't already exist.
 * Fork the repository on GitHub

## Making changes
 * Create a topic branch off of master
 * Make commits of logical units.
 * Rebase off master before submitting.
 * Make sure you have added the necessary unit tests for your changes.
 * Run _all_ the tests to assure nothing else was accidentally broken.

## Submitting Changes
 * Push your changes to a topic branch in your fork of the repository.
 * Submit a pull request to the MycroftAI/adapt repository.
 * The MycroftAI organization reviews pull requests regularly. We will provide feedback as necessary, and TravisCI will verify that your changes pass all tests.
 * After feedback, we expect responses in 2 weeks. After 2 weeks, we may close or coopt the change request.


#### Modeled after the Puppet Labs contributing documentation.
