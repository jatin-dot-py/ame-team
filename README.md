# ame-team Project

This repository serves as a place for each team member to work on their given projects, prior to having them added to the main project.

## Important steps:
1. Utilize Poetry for dependency management to stay consistent with the main project.
2. Confirm all new packages with Armani to ensure no conflicts with the main project.
3. Write clean code that follows the basic guidelines we have in place:
   - Keep functions and methods small and modular.
   - Create documentation for each script that explains the purpose, the various things involved, and most importantly, be detailed about the “entry” into the script.
4. Use simple and clean docstrings that tell a human reader what the function does. (It's best to write docstrings when you are done with a script so you do not accidentally leave outdated information.
5. Be careful that you do not change or move files that are in various places, such as "common" or other places that may not make sense when looking only at this code. (They serve a purpose in the bigger project)
6. If you can see room for improvement in any of the helper or utility directories, please inform Armani to make sure you have the full context and then you can proceed with your improvements.
7. While this project is not set up as a Django project, the main project is built on Django, so in some places, you may see code that is designed to mimic Django, without involving it.
   - If you see dependencies on Django, you can comment them out and create a local equivalent for it.
8. It's very important that any changes to directory structure, filenames, and function, class or method signatures are cleared through Armani to avoid potential conflicts.

Thank you for being a part of this incredible project!

## CI/CD:
This is a core concept that MUST be adhered to by everyone!
- You must push your latest code to git daily.
- Each day, you must start by getting the latest version of Main and merging it with your local code to ensure you do not "fall behind" and then cause major conflicts later or have errors by other developers go unnoticed.
- If you have things that are broken or untested, push them to a new branch, until you get them fixed. You still must push everything daily.
- Each day, if your code does not cause conflicts, it's important that we push it to the main, even if you are not done yet, as long as there are no major bugs in your code that hurt the overall project.

Thank you for following these guidelines, which are designed to help all of us. 
