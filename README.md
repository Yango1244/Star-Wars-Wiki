# Project 1: Wiki Viewer

Section | Score | Reason
--------|-------|-------
_Filling Wiki_ | 10/10 | would have been nice to have Andor too :)
_Backend_ | 10/10| all methods implemented
_Home, About and Pages_
Home | 2/2|
About | 2.5/3 | code did not work as intended as there was no `./flaskr/static` directory already existing; ideally, you could return the Blob url without downloading to a `static` directory
Pages Index | 1.5/2 | the pages index showed non-pages; the index should have filtered out any non-pages to only display pages
Pages Parameterized | 3/3 |
_Sign up, Login and Logout_
Sign up | 4/4 |
Login | 5/5 |
Logout | 1/1 |
_Upload_ | 4.5/5 | code did not work as intended as there was no `./temp_files` directory already existing; ideally, on backend startup you would ensure that the directory is created first
_Navigation Bar_ | 5/5 |
_Unit Tests and Comments_ 
Unit Tests | 19/35 | Overall, tests were good, however a couple of key misses: in the Backend, `test_get_image` should have been mocked and tested for success and failure modes; missed a Backend test for a bad password signin attempt; while there were comprehensive tests for the `login`, `singup`, and `update` backend methods, there should have been tests for the `login/validate` and `signup/validate` routes and more comprehensive tests for the `upload/upload_submit` route; no test for the `pages/*`, `about`, `logout`, or for returning an image in the routes
Comments | 3/5 | did not include arguments or return comments in methods (https://google.github.io/styleguide/pyguide.html#383-functions-and-methods) or attributes of the classes (https://google.github.io/styleguide/pyguide.html#384-classes)
_Augment the Upload Route_
Display markdown | 0/5 | No transformations for markdown.
Restrict filetypes | 2/2 |
Zipped files | 3/3 |
Link Requirement | 0/10 | No code for link requirement.
Unit tests | 5/10 | No tests for markdown or link requirement.
_Penalty for Bad Style_ | -1/5 | Overall, style was fine; in `pages.py`, the variable for `Backend` was named `global_test` which doesn't really make sense -- additionally, there were multiple variables for `Backend`
__Total__ | 79.5/120 |