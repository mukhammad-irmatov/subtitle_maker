# subtitle_maker

## To run server in local, you need to do follow steps:

1) Clone the repository:
git clone https://github.com/mukhammad-irmatov/subtitle_maker.git

2) Install pipenv package and activate virtualenv
- pip install pipenv
- pipenv shell
- pipenv sync

3) check .env file to ensure the API address is correct

4) do database migration
- python manage.py makemigrations
- python manage.py migrate

5) run the program
- python manage.py runserver
