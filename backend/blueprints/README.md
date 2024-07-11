# Approach

## JWT based registration
- To register a new register call the `/api/auth/registration` endpoint 
- This will
    - create a user with the `unverified` role
    - Send a `registration` type JWT token to your email
- Take this token and call the `/api/auth/verification` endpoint - this will check if this is a valid JWT `registration` token, if it is:
    - delete the `unverified` role for the user
    - add the `free` role for the user
- These token will expire after a certain amount of time
- Repeated calls to `/api/auth/registration` after initial registration:
    - If the role is `unverified` we have never successfully called the `/api/auth/verification` endpoint and we will repeatedly send emails with registration tokens
    - If the role is any other role apart from `unverified` we have successfully authenticated the user and another call to `/api/auth/verification` endpoint will result `409` error status code
NOTE: this means any of the `registration` type tokens in the emails can successfully call `/api/auth/verification`.

## JWT based password reset
- To reset a password call the `/password/reset` endpoint, 
- This will send a `password_reset` type JWT token to the user's email
    - The token encodes a substring of the hashed password in the database and then this substring is hashed again
- Take this token and call the `/api/auth/password` endpoint which will check if the partial password double-hashed value is valid:
    - If it is valid the password will be reset, otherwise it will return a `400` error
- These token will expire after a certain amount of time
- Repeated calls to the `/api/auth/password/reset` endpoint will issue multiple valid tokens for a user
NOTE: this flow means that any of the `password_reset` type tokens from the `password/reset` can successfully call `/api/auth/password` to reset the password BUT with the added feature that as soon as one of the tokens is used - all the tokens previously issued will expire because they will no longer match the partial hashes of the previous password in the database.
