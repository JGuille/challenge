# Sailpoint Coding Challenge

Using the language of your choice, write code that will use the GitHub API to retrieve a summary of all opened, and closed pull requests in the last week for a given repository and print an email summary report that might be sent to a manager or Scrum-master. Choose any public target GitHub repository you like that has had at least 3 pull requests in the last week. Format the content email as you see fit, with the goal to allow the reader to easily digest the events of the past week. Please print to console the details of the email you would send (From, To, Subject, Body). As part of the submission, you are welcome to create a Dockerfile to build an image that will run the program, however, other ways of implementing this is acceptable.

Definition of Done:

 - Your code demonstrates use of variables, looping structures, and
   control structures
 - Your code prints a user-friendly summary of open, and closed pull requests including counts of PRs as well as their titles. Use your judgement on what you think is important information.
 - Your code is able to be run/compiled without errors
 - Your code should be configurable when it runs. Use your judgement on what needs to be configurable.
 - Your solution describes how this would be run to produce regular reports. 


## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/JGuille/challenge.git
    ```

2. Navigate to the directory:

    ```bash
    cd challenge
    ```

3. Build the Docker image:

    ```bash
    docker build -t challenge .
    ```

4. Run the Docker container:

    ```bash
    docker run challenge <repository_url> <from_email_address> <to_email_address> <subject>
    ```

   Example:

    ```bash
    docker run challenge https://github.com/facebook/docusaurus sailpointcodingchallenge@gmail.com manager@company.com "Weekly Pull Request Report"
    ```
   Result:
	```bash
	Weekly Pull Request Report for facebook/docusaurus


	Open Pull Requests:
	  PR #10119 - chore: CI upgrade to Node 22
	    Updated at: 2024-05-31 16:28:39+00:00
	    Author: slorber
	    Link: https://github.com/facebook/docusaurus/pull/10119

	  PR #10180 - docs: backport #10173 to v3.3 (& revise the content)
	    Updated at: 2024-05-31 07:52:40+00:00
	    Author: tats-u
	    Link: https://github.com/facebook/docusaurus/pull/10180

	Closed Pull Requests:
	  PR #10188 - chore: update examples for v3.4.0
	    Updated at: 2024-05-31 17:55:12+00:00
	    Author: slorber
	    Link: https://github.com/facebook/docusaurus/pull/10188

	  PR #10186 - chore: release Docusaurus v3.4
	    Updated at: 2024-05-31 17:10:46+00:00
	    Author: slorber
	    Link: https://github.com/facebook/docusaurus/pull/10186

	  PR #10137 - feat(docs, blog): add support for `tags.yml`, predefined list of tags
	    Updated at: 2024-05-31 16:21:14+00:00
	    Author: OzakIOne
	    Link: https://github.com/facebook/docusaurus/pull/10137

	  PR #10185 - fix(docs, blog): Markdown link resolution does not support hot reload
	    Updated at: 2024-05-31 15:51:16+00:00
	    Author: slorber
	    Link: https://github.com/facebook/docusaurus/pull/10185

	  PR #10178 - fix(theme): SearchPage should respect `contextualSearch: false` setting
	    Updated at: 2024-05-30 15:50:56+00:00
	    Author: ncoughlin
	    Link: https://github.com/facebook/docusaurus/pull/10178

	  PR #10173 - docs: improve how to use `<details>`
	    Updated at: 2024-05-30 13:29:04+00:00
	    Author: tats-u
	    Link: https://github.com/facebook/docusaurus/pull/10173

	  PR #10176 - docs: add community plugin docusaurus-graph
	    Updated at: 2024-05-30 10:35:41+00:00
	    Author: Arsero
	    Link: https://github.com/facebook/docusaurus/pull/10176

	  PR #10175 - Update intro.md
	    Updated at: 2024-05-28 07:23:11+00:00
	    Author: kbirkenmayer
	    Link: https://github.com/facebook/docusaurus/pull/10175

	  PR #10167 - docs: suggest using `{<...>...</...>}` if don't use Markdown in migra…
	    Updated at: 2024-05-27 21:29:40+00:00
	    Author: tats-u
	    Link: https://github.com/facebook/docusaurus/pull/10167

	  PR #10156 - fix(search-algolia): Algolia plugin SearchPage does not respect configuration 
	    Updated at: 2024-05-27 11:38:35+00:00
	    Author: ncoughlin
	    Link: https://github.com/facebook/docusaurus/pull/10156

	  PR #10171 - Upgrade mermaid
	    Updated at: 2024-05-25 16:23:24+00:00
	    Author: yorhodes
	    Link: https://github.com/facebook/docusaurus/pull/10171


	Email sent successfully
	```
# Important!

- The `sailpointcodingchallenge@gmail.com` account was created with the only purpose of using it in this coding challenge. Inside this repo there is a `.env` file which contains the credentials. 
- If you dont use the `sailpointcodingchallenge@gmail.com` account, the script will still work, but it wont sent the email.  That is unless you update the value in the `.env` file