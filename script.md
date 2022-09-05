# Vu1nW0r1d
A few students created a blog app. Is it secure though?

# Expected Scenario
* Attacker registers a new account.
* Discovers from the blogs, the other registered users
* Finds out the cookie forge vulnerability and exploits it to log in as Paul (Admin)
  * Decode the session cookie, find out the `username` value
  * Craft an exploit to encode the session cookie with the malicious payload
  * Bruteforce the session token
  * Send the forged cookie
* Find the /admin directory
* Login to the server