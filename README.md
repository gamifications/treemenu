We need a django web developer to build a smart "How to use" guiding system.

The system should have:
- Different user type that we can add edit remove and set password for each.
- Each user type will have its own guide

The guide should contain:
- Parent section
-- each parent should be able to hold sub parents section
--- we can created as many as nested subparent directories (like folders we can create infinite nested folder inside each folder)
Then :
- Instruction: we can put instruction in parent or any subparent or nested subparent we want
--! Instructions will look like this (
action name: (ex) how to put an article
User type: (ex:) shop (this will be seen only in shop user type not in dépôt

Action: exemple: Press F5 (F5 and any other keyboard input should look like keyboard key check the image attached) > (bread crumb design) [6] Settings [3] insert

the system should also contain a quick chatbot that we can ask him quickly (ex: how to remove an article) and it will give you the instructions based on which USER TYPE you're connected. We'd like to use NLP ai for the chatbot


questions
---------
who will create sections(menus) and Instructions? Everyone/Perticular User/Perticular Usertype