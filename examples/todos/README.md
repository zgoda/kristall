# Todos example for Kristall

This is larger application example for Kristall that shows its intended usage as backend for Javascript UI.

## Backend

Backend application uses [Marshmallow](https://pypi.org/project/marshmallow/) for data serialization and [Pony ORM](https://pypi.org/project/pony/) for data access layer.

Create virtualenv with Python>=3.7 and install backend code:

```shell
/usr/bin/python3.7 -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install -U -e .[dev]
```

Then with active virtualenv you can launch it from terminal with simple comand `todos` (`setup.py` registers console endpoint). By default application runs on port 5000 and has enabled reloader. Werkzeug built-in debugger is by default turned off because application does not have its own UI, enable it with `todos --debug`. To be able to use it issue requests from web browser (tools like Postman do not render HTML). Run `todos --help` to learn other command line options.

## Frontend

Frontend application is written in Javascript using [Preact UI framework](https://preactjs.com/), with [Picnic](https://picnicss.com/) as CSS library. Change to `ui` directory and initialize application:

```shell
cd ui
npm install
```

Frontend application is configured to proxy requests from Javascript code to backend running on port 5000. Run it with `npm` in separate terminal window:

```shell
npm run dev
```

Then with backend app running on http://127.0.0.1:5000 you may access the frontend app on http://127.0.0.1:8080. Dev server runs with hot reload.

If you change port or host of your backend you will need to update frontend proxy configuration in `ui/preact.config.js`. This is also the right place if you want to change eg. frontend application port.
