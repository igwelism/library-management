### Instructions for cloning the repository

1. #### Obtain the Repository URL:
   Ensure you have the HTTPS or SSH URL for the repository (e.g.,`https://github.com/igwelism/library-management.git`)
2. #### Open Your Terminal or Command Prompt:
    Navigate to the directory where you want to clone the repository.
3. #### Run the Clone Command:
    Use the following command, replacing <repository_url> with the actual URL:
    `git clone https://github.com/igwelism/library-management.git`
4. #### Navigate to the Cloned Repository:
    Once the cloning process is complete, change into the repository’s directory: `cd repository`
5. #### Verify the Repository:
    Optionally, you can list the files with: `ls`
    or check the repository status with: `git status`

### Steps to create docker container and install dependencies
1. Clone the repo
2. Ensure Python is installed `python --version`
3. Create a virtual environment: `python -m venv env`
4. Activate the virtual environment: `source env/bin/activate`
5. Run `docker compose build`
6. Run `docker compose up -d`

### Guidelines to see the application locally.
1. On the browser navigate to `http://localhost:8000/library/` to view list of books.
2. Use the search bar to filter by title and author name
3. Click on the "Borrow" link to borrow a book (You have to be a log in user)
4. API endpoints are also available to borrow and return books using: `http://127.0.0.1:8000/api/loan/book/` etc.

### Testing
You can call `python manage.py test` to run the tests.